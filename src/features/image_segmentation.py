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
    neurons_x = [roi['centroid'][1] for roi in r if roi['area'] > min_neuron_pix]
    neurons_y = [roi['centroid'][0] for roi in r if roi['area'] > min_neuron_pix]

    return neurons_x, neurons_y, r


def get_pixels_for_experiment(processed_dir, get_pickled=True):
    """
    returns x, y, region properties for all images in directory

    :param processed_dir: filepath of processed directory
    :param get_pickled: True to access pre-pickled file, False to re-create pickle
    :return: {image_id: {x:[], y:[], regionprops: {}}}
    """
    img_data = {}
    if get_pickled:
        pickles = [file for file in os.listdir(processed_dir) if file.endswith('.pkl')]
        for pickle_fname in pickles:
            with open(pickle_fname, 'rb') as f:
                img_props = pickle.load(f)
            img_id = get_image_name(pickle_fname)
            img_data[img_id] = img_props
    else:
        processed_imgs = read_images_in(processed_dir) # {img_fpath:img}
        for img_fpath, img in processed_imgs.items():
            img_fpath = '/Users/mm40108/projects/datadays17/olfactory_protein_viz/data/DevMouse/Bmpr2/100042306/processed/100878706_processed.jpg'
            img = processed_imgs[img_fpath]

            # get image id
            img_id = get_image_name(img_fpath)
            print('extracting x,y coords and other image info from', img_id)
            x, y, r = get_pixels(img, min_neuron_pix=20)  ## SLOW
            img_props = {'x' : x, 'y' : y, 'regionprops' : r}

            pickle_fname = os.path.join(processed_dir, str(img_id) + '_props.pkl')
            with open(pickle_fname, 'wb') as f:
                pickle.dump(img_props, f)

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

    img_dict = read_images_in(organism, protein, experiment, 'processed')
    print(img_dict.keys())

    img_file = '/Users/mm40108/projects/datadays17/olfactory_protein_viz/data/DevMouse/Bmpr2/100042306/20_100878638.jpg'
    img = img_dict[img_file]

    # display segmenting steps
    segment_fig = plt.figure(figsize=(10,10))
    ax_orig = segment_fig.add_subplot(2, 2, 1)
    ax_orig.imshow(img, cmap='gray')

    # use ISO threshold
    chosen_threshold = 'iso'
    bw_img = apply_threshold(img, chosen_threshold)

    ax_bw = segment_fig.add_subplot(2, 2, 2)
    ax_bw.imshow(bw_img, cmap='gray')

    # get coords
    label_img = label(bw_img)
    region_metrics = regionprops(label_img)
    color_label_img = label2rgb(label_img,
                                image=bw_img,
                                alpha=0.7,
                                bg_label=0,
                                bg_color=(0, 0, 0),
                                image_alpha=1,
                                kind='overlay')

    ax_color = segment_fig.add_subplot(2, 2, 3)
    ax_color.imshow(color_label_img)

    neuron_px = 20
    neurons_x = [roi['centroid'][1] for roi in region_metrics if roi['area'] > neuron_px]
    neurons_y = [roi['centroid'][0] for roi in region_metrics if roi['area'] > neuron_px]

    ax_pix = segment_fig.add_subplot(2, 2, 4)
    ax_pix.imshow(img, cmap='gray', interpolation='nearest', origin='upper')
    ax_pix.plot(neurons_x, neurons_y, 'r.')