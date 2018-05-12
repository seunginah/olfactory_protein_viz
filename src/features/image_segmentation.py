import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from skimage import filters as skfilt
from skimage.measure import label
from skimage.measure import regionprops
from skimage.color import label2rgb

sys.path.append('/Users/mm40108/projects/datadays17/olfactory_protein_viz/src/')
from data.ABA_image_utils import get_image_name
from features.image_processing import read_images_in
from visualization.make_plots import plot_expanding_rows, plot_channels

DATA_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/data"
METADATA_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/metadata"



def save_as_pickled_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])



def try_to_load_as_pickled_object_or_None(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    try:
        input_size = os.path.getsize(filepath)
        bytes_in = bytearray(0)
        with open(filepath, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        obj = pickle.loads(bytes_in)
    except:
        return None
    return obj


def get_thresholds(img, threshold=None):
    thresholds = {"yen": skfilt.threshold_yen(img),
        "otsu": skfilt.threshold_otsu(img),
        "li": skfilt.threshold_li(img),
        "iso": skfilt.threshold_isodata(img)}
    if threshold is None:
        return thresholds
    else:
        return thresholds[threshold]

def apply_threshold(img, threshold):
    threshold = get_thresholds(img, threshold)
    return img > threshold


def try_thresholds(img, threshold_fig):
    thresholds = get_thresholds(img)
    print(thresholds)
    # threshold_fig = plt.figure(figsize=(10, 10))
    for i, thresh_type in enumerate(thresholds.keys()):
        thresh_val = thresholds[thresh_type]
        ax = threshold_fig.add_subplot(2, 2, i + 1)
        ax.imshow(img > thresh_val, interpolation='nearest', cmap='gray')
        ax.set_title(thresh_type + ": {}".format(np.round(thresholds[thresh_type])))
    return threshold_fig


def get_pixels(img, min_neuron_pix=20):
    """
    regionprops: ['area',  'bbox',  'centroid',  'convex_area',
    'convex_image',  'coords',  'eccentricity',  'equivalent_diameter',  'euler_number',
    'extent',  'filled_area',  'filled_image',  'image',  'inertia_tensor',  'inertia_tensor_eigvals',
    'intensity_image',  'label',  'local_centroid',  'major_axis_length',  'max_intensity',
    'mean_intensity',  'min_intensity',  'minor_axis_length',  'moments',  'moments_central',
    'moments_hu',  'moments_normalized',  'orientation',  'perimeter',  'solidity',
    'weighted_centroid',  'weighted_local_centroid',  'weighted_moments',
    'weighted_moments_central',  'weighted_moments_hu',  'weighted_moments_normalized']

    """
    # label neurons numerically
    label_img = label(img)
    # get region properties
    r = regionprops(label_img)
    # label each neuron with a color
    color_label_img = label2rgb(label_img, image=img, alpha=0.7, bg_label=0,
                                bg_color=(0, 0, 0), image_alpha=1, kind='overlay')
    # get x, y coords
    all_rprops = list()
    for roi in r:
        rprops = {}
        if roi['area'] > min_neuron_pix:
            rprops['neurons_x'] = roi['centroid'][1]
            rprops['neurons_y'] = roi['centroid'][0]
            rprops['area'] = roi['area']
            rprops['orientation'] = roi['orientation']
            rprops['bbox'] = roi['bbox']
            all_rprops.append(rprops)

    print(len(all_rprops))
    return all_rprops


def get_pixels_for_experiment(processed_dir, metadata_dir, get_pickled=True):
    """
    returns x, y, region properties for all images in directory

    :param processed_dir: filepath of processed directory
    :param get_pickled: True to access pre-pickled file, False to re-create pickle
    :return: {image_id: {x:[], y:[], regionprops: {}}}
    """
    img_data = {}
    if get_pickled:
        pickles = [file for file in os.listdir(metadata_dir) if file.endswith('.pkl')]
        for pickle_fname in pickles:
            pickle_fpath = os.path.join(metadata_dir, pickle_fname)
            img_id = pickle_fname.split('_rprops.pkl')[0]
            img_data[img_id] = try_to_load_as_pickled_object_or_None(pickle_fpath)
    else:
        print('reading images in ', processed_dir)
        processed_imgs = read_images_in(processed_dir) # {img_fpath:img}
        for img_fpath, img in processed_imgs.items():
            # get image id
            img_id = get_image_name(img_fpath)
            print('extracting x,y coords and other image info from', img_id)
            img_props = get_pixels(img, min_neuron_pix=20)  ## SLOW

            # save as pickle in location under 'metadata dir' that is
            # analogous to the image slice it comes from
            if not os.path.exists(metadata_dir):
                os.mkdir(metadata_dir)
            pickle_fname = os.path.join(metadata_dir, str(img_id) + '_rprops.pkl')
            save_as_pickled_object(img_props, pickle_fname)
            # with open(pickle_fname, 'wb') as f:
            #     #pickle.dump(img_props, f)
            #     np.save(f, img_props)
            img_data[img_id] = img_props
    return img_data


def validate_experiment_images(exp_pix):
    if exp_pix is None:
        return {}
    tmp = exp_pix
    for img_id in exp_pix.keys():
        try:
            int(img_id)
        except ValueError as e:
            tmp.pop(img_id)
    return exp_pix[tmp.keys()]


def register_experiment(exp_dir, rprops_dir, get_pickled):
    # get processed images
    exp_pix = get_pixels_for_experiment(exp_dir, rprops_dir, get_pickled=get_pickled)
    exp_df = None
    for img_id, img_props in exp_pix.items():
        print('registering image', img_id)
        # read image pixels
        tmp = pd.DataFrame(img_props)
        tmp['image_id'] = img_id
        if exp_df is None:
            exp_df = tmp
        else:
            exp_df = pd.concat([exp_df, tmp])
    return validate_experiment_images(exp_df)



def check_existing_pkl(fpath):
    if any([True for f in os.listdir(fpath) if f.endswith('.pkl')]):
        print('looks like there are already pickles here.. skipping')
        return True, fpath
    else:
        return False, None



def get_pixels_for_gene(gene_dir, rprops_dir, get_pickled=True, skip_already_pickled=True):
    exp_dirs = [os.path.join(gene_dir, f, 'processed') for f in os.listdir(gene_dir)
                 if not f.startswith('.')]
    rprops_dirs = [os.path.join(rprops_dir, f, 'processed') for f in os.listdir(rprops_dir)
                 if not f.startswith('.')]
    gene_df = None
    for exp_dir, rprops_dir in zip(exp_dirs, rprops_dirs):
        print('\texperiment: ', exp_dir, '\n\timage properties:', rprops_dir)
        # some experiments may already have pickles, so don't do them
        already_exists, pkl_fpath = check_existing_pkl(rprops_dir)
        if skip_already_pickled:
            if already_exists:
                tmp = register_experiment(exp_dir, rprops_dir, get_pickled=True)
            else:
                print('registering experiment', exp_dir)
                tmp = register_experiment(exp_dir, rprops_dir, get_pickled=False)
        else:
            print('registering experiment', exp_dir)
            tmp = register_experiment(exp_dir, rprops_dir, get_pickled)
        # read image pixels
        tmp['experiment_id'] = exp_dir.split('/')[exp_dir.split('/').index('processed')-1]
        if gene_df is None:
            gene_df = tmp
        else:
            gene_df = pd.concat([gene_df, tmp])
    return gene_df


if __name__ == '__main__':
    product = 'DevMouse'
    # gene = 'Bmpr2'
    # gene_dir = os.path.join(DATA_DIR, product, gene)
    # rprops_dir = os.path.join(METADATA_DIR, product, gene)
    # bmpr2 = get_pixels_for_gene(gene_dir, rprops_dir, get_pickled=False, skip_already_pickled=True)
    # pickle_fname = os.path.join(rprops_dir, 'Bmpr2_rprops.pkl')
    # save_as_pickled_object(bmpr2, pickle_fname)

    ## DONE
    # gene = 'Cdh5'
    # gene_dir = os.path.join(DATA_DIR, product, gene)
    # rprops_dir = os.path.join(METADATA_DIR, product, gene)
    # cdh5 = get_pixels_for_gene(gene_dir, rprops_dir, get_pickled=False, skip_already_pickled=True)

    ## PARTIAL
    gene = 'Robo2'
    gene_dir = os.path.join(DATA_DIR, product, gene)
    rprops_dir = os.path.join(METADATA_DIR, product, gene)
    robo2 = get_pixels_for_gene(gene_dir, rprops_dir, get_pickled=False, skip_already_pickled=True)
    pickle_fname = os.path.join(rprops_dir, 'Robo2_rprops.pkl')
    save_as_pickled_object(robo2, pickle_fname)


    # # lets process images from one experiment
    # experiment = '100042306'
    # processed_dir = os.path.join(DATA_DIR, product, gene, experiment, 'processed')
    # rprops_dir = os.path.join(METADATA_DIR, product, gene, experiment, 'processed')

    # # write
    # img_props = get_pixels_for_experiment(processed_dir, rprops_dir, get_pickled=False)
    # # read
    # img_props = get_pixels_for_experiment(processed_dir, rprops_dir, get_pickled=True)
    #
    # # img_dict = read_images_in(processed_dir)
    #
    # img_file = '/Users/mm40108/projects/datadays17/olfactory_protein_viz/data/DevMouse/Bmpr2/100042306/processed/100878706_processed.jpg'
    # img = img_dict[img_file]
    #
    # # display segmenting steps
    # segment_fig = plt.figure(figsize=(10,10))
    # ax_orig = segment_fig.add_subplot(2, 2, 1)
    # ax_orig.imshow(img, cmap='gray')
    #
    # # use ISO threshold
    # chosen_threshold = 'iso'
    # bw_img = apply_threshold(img, chosen_threshold)
    #
    # ax_bw = segment_fig.add_subplot(2, 2, 2)
    # ax_bw.imshow(bw_img, cmap='gray')
    #
    # # get coords
    # label_img = label(bw_img)
    # region_metrics = regionprops(label_img)
    # color_label_img = label2rgb(label_img,
    #                             image=bw_img,
    #                             alpha=0.7,
    #                             bg_label=0,
    #                             bg_color=(0, 0, 0),
    #                             image_alpha=1,
    #                             kind='overlay')
    #
    # ax_color = segment_fig.add_subplot(2, 2, 3)
    # ax_color.imshow(color_label_img)
    #
    # neuron_px = 20
    # neurons_x = [roi['centroid'][1] for roi in region_metrics if roi['area'] > neuron_px]
    # neurons_y = [roi['centroid'][0] for roi in region_metrics if roi['area'] > neuron_px]
    #
    # ax_pix = segment_fig.add_subplot(2, 2, 4)
    # ax_pix.imshow(img, cmap='gray', interpolation='nearest', origin='upper')
    # ax_pix.plot(neurons_x, neurons_y, 'r.')