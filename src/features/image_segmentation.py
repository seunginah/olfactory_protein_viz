import os
import sys
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
            img_data[pickle_fname] = try_to_load_as_pickled_object_or_None(pickle_fname)
    else:
        processed_imgs = read_images_in(processed_dir) # {img_fpath:img}
        for img_fpath, img in processed_imgs.items():
            #img_fpath = '/Users/mm40108/projects/datadays17/olfactory_protein_viz/data/DevMouse/Bmpr2/100042306/processed/100878706_processed.jpg'
            #img = processed_imgs[img_fpath]

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

#
# def register_experiment(exp_dir, exp_subdir='processed'):
#     # get processed images
#     exp_pix = get_pixels_for_experiment(os.path.join(exp_dir, exp_subdir))
#
#     for img_id, img_props in exp_pix.items():
#





if __name__ == '__main__':
    # lets process images from one experiment
    organism = 'DevMouse'
    protein = 'Bmpr2'
    experiment = '100042306'
    processed_dir = os.path.join(DATA_DIR, organism, protein, experiment, 'processed')
    rprops_dir = os.path.join(METADATA_DIR, organism, protein, experiment, 'processed')

    # write
    img_props = get_pixels_for_experiment(processed_dir, rprops_dir, get_pickled=False)
    # read
    img_props = get_pixels_for_experiment(processed_dir, rprops_dir, get_pickled=False)

    # img_dict = read_images_in(processed_dir)
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