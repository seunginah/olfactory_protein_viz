import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave

sys.path.append('/Users/mm40108/projects/datadays17/olfactory_protein_viz/src/')
from data.ABA_image_utils import get_image_name
from ecallen.ecallen import images as ecimg
from visualization.make_plots import plot_expanding_rows, plot_channels

DATA_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/data"


def get_image_segment(img, **kwargs):
    for k,v in kwargs.items():
        print(k, v)
    print(img.shape)
    h = img.shape[0]
    w = img.shape[1]
    c = img.shape[2] if len(img.shape) > 2 else 1

    # defaults to half the image
    x_from = 0
    y_from = 0
    x_to = int(np.ceil(w/2))
    y_to = int(np.ceil(h/2))

    # user args
    if 'x_from' in kwargs.keys():
        x_from = kwargs['x_from']
    if 'x_to' in kwargs.keys():
        x_to = kwargs['x_to']
    if 'y_from' in kwargs.keys():
        y_from = kwargs['y_from']
    if 'y_to' in kwargs.keys():
        y_to = kwargs['y_to']

    # 2D or 3D+
    if c == 1:
        cropped_img = img[x_from:x_to, y_from:y_to]
    else:
        cropped_img = img[x_from:x_to, y_from:y_to, :]
    return cropped_img


def monochrome_image(img, exp_params):
    # since all 3 color channels have "none"
    red_c = exp_params['red_channel']
    green_c = exp_params['green_channel']
    blue_c = exp_params['blue_channel']

    if any([True for c in [red_c, green_c, blue_c] if c is not None]):
        print('pay attention to channels')
        special_channels = [red_c, green_c]
        correct_channels_img = img[:, :, special_channels]
    else:
        print('no special channels')
        special_channels = None
        correct_channels_img = img

    # make into 2D, select maximum pix intensity across the appropriate channels
    return np.max(correct_channels_img, axis=2)


def invert_image(img):
    """ invert image where pixel intensity is between 0-255 """
    # TODO: get max pixel of img
    return 255 - img


def read_images_in(exp_dir):
    # get all valid section images in the section data set
    # imread is slow!!
    img_files = [os.path.join(exp_dir, file) for file in os.listdir(exp_dir) if
                 not file.startswith('.') and file.endswith('.jpg')]
    print('read_images_in(', exp_dir, '):', '\n\t'.join(img_files))
    # TODO check for valid image files
    return {img_file: imread(img_file) for img_file in img_files}


def process_raw_image(img, exp_params, crop=None):
    # crop mode
    if crop is None:
        cropped_img = img
    elif crop == 'default':
        cropped_img = get_image_segment(img)
    elif crop == 'OB':
        cropped_img = get_image_segment(img, x_from=2000, x_to=7000, y_to=5000)

    # invert image
    inverted_img = invert_image(cropped_img)

    # make image monochrome
    monochromatic_img = monochrome_image(inverted_img, exp_params)
    return cropped_img, inverted_img, monochromatic_img


def save_processed_images(exp_dir, img_dict, exp_subdir='processed'):
    """
    save images in an experiment directory
    :param exp_dir: file path of experiment directory
    :param img_dict: {filename: processed image}
    :return:
    """
    # save them into a directory called "processed"
    processed_dir = os.path.join(exp_dir, exp_subdir)
    if not os.path.exists(processed_dir):
        print('\ndirectory ', processed_dir, ' doesnt exist yet, creating it .. ')
        os.mkdir(processed_dir)

    processed_files = {fname:None for fname in img_dict.keys()}
    for img_id, img in img_dict.items():
        img_fname = os.path.join(processed_dir, str(img_id) + '_processed.jpg')
        processed_files[img_id] = img_fname
        print('saving to: ',img_fname)
        imsave(img_fname, img)
    return


def process_raw_images_in(organism, protein, experiment, **kwargs):
    crop = None if 'crop' not in kwargs.keys() else kwargs['crop']
    print('crop: ', crop)

    # get experiment parameters
    exp_params = ecimg.get_imaging_params(experiment)
    print('\nprocessing raw images for experiment:\n\t', exp_params)

    # read images
    exp_dir = os.path.join(DATA_DIR, organism, protein, experiment)
    exp_imgs = read_images_in(exp_dir)  # slow!!

    # process them
    processed_imgs = {}
    for img_file, img in exp_imgs.items():
        cropped_img, inverted_img, monochromatic_img = process_raw_image(img, exp_params, crop=crop)
        img_dict = {'raw': img, 'cropped': cropped_img, 'inverted' : inverted_img, 'monochrome' : monochromatic_img}
        processed_imgs[img_file] = img_dict

    # save the monochrome ones
    img_dict = {get_image_name(img_file):img_dict['monochrome'] for img_file, img_dict in processed_imgs.items()}
    processed_fnames = save_processed_images(exp_dir, img_dict)

    return processed_imgs



def get_all_processed_experiments(organism):
    organism_dir = os.path.join(DATA_DIR, organism)
    genes = [file for file in os.listdir(organism_dir) if not file.startswith('.')]

    for gene in genes:
        gene_dir = os.path.join(organism_dir, gene)
        experiments = [file for file in os.listdir(gene_dir) if not file.startswith('.')]
        for exp in experiments:
            process_raw_images_in(organism, gene, exp, crop='OB')

    return None



if __name__ == '__main__':
    # lets process one image from one experiment
    organism = 'DevMouse'
    protein = 'Bmpr2'
    experiment = '100042306'
    exp_dir = os.path.join(DATA_DIR, organism, protein, experiment)
    exp_imgs = read_images_in(exp_dir) # slow!!
    # get experiment parameters
    exp_params = ecimg.get_imaging_params(experiment)
    print(exp_params)

    img_file = '/Users/mm40108/projects/datadays17/olfactory_protein_viz/data/DevMouse/Bmpr2/100042306/13_100878599.jpg'
    img = exp_imgs[img_file]

    # get small img
    default_crop = get_image_segment(img)
    plt.imshow(default_crop)

    olf_crop = get_image_segment(img, x_from=2000, x_to=7000, y_to=5000)
    plt.imshow(olf_crop)

    # basic processing figure
    basic_fig = plt.figure(figsize=(1, 4))
    ax_orig = basic_fig.add_subplot(1, 4, 1)
    ax_orig.imshow(img)
    ax_crop = basic_fig.add_subplot(1, 4, 2)
    ax_crop.imshow(olf_crop)

    # show channels
    channels_fig = plt.figure(figsize=(2, 3))
    channels_fig = plot_channels(olf_crop, channels_fig, start_subplot=1)

    # invert image
    inverted_img = invert_image(olf_crop)

    # show inverted image, channels
    ax_inv = basic_fig.add_subplot(1, 4, 3)
    ax_inv.imshow(inverted_img)
    channels_fig = plot_channels(inverted_img, channels_fig, start_subplot=2)

    # make image monochrome
    monochrome_img = monochrome_image(inverted_img, exp_params)

    # show monochrome image
    ax_bw = basic_fig.add_subplot(1, 4, 4)
    ax_bw.imshow(monochrome_img, cmap='gray')


    ##  let's process all experiments
    organism = 'DevMouse'
    organism_dir = os.path.join(DATA_DIR, organism)
    genes = [file for file in os.listdir(organism_dir) if not file.startswith('.')]

    for gene in genes:
        gene_dir = os.path.join(organism_dir, gene)
        experiments = [file for file in os.listdir(gene_dir) if not file.startswith('.')]
        for exp in experiments:
            process_raw_images_in(organism, gene, exp, crop='OB')

    # # robo2
    # gene_dir = os.path.join(organism_dir, 'Robo2')
    # experiments = [file for file in os.listdir(gene_dir) if not file.startswith('.')]
    # for exp in experiments:
    #     process_raw_images_in(organism, gene, exp, crop='OB')
    #
    #
    # gene = 'Cdh5'
    # gene_dir = os.path.join(organism_dir, gene)
    # experiments = ['100058480', '100058500', '100072907', '100078477', '100082796', '100084794', '77931975']
    # for exp in experiments:
    #     process_raw_images_in(organism, gene, exp, crop='OB')
    #
