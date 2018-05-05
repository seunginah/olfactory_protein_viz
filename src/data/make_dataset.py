import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.getcwd(), "src"))
from ecallen.ecallen import images as ecimg
from data.ABA_utils import get_genes, get_genes_from_aliases, get_experiments_and_images
from data.ABA_image_utils import get_image, get_organism_image_params, save_image_locally

THIS_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/src/data"
DATA_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/data"

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '../', '../', 'data')


# get the affine map for the 2D transformation
section_image_id = 308604373
tform_2d = ecimg.get_affine_2d(section_image_id)

# get the affine map for the 3D transformation
section_dataset_id = 308604125
tform_3d = ecimg.get_affine_3d(section_dataset_id)

print("t_form2d: ", tform_2d)
print("t_form3d: ", tform_3d)

section_image_id = 308604373
section_dataset_id = 308604125

# generate some random (x,y) pairs
x_test_pix = np.random.randint(3000, 5000, 100)
y_test_pix = np.random.randint(3000, 5000, 100)

# retrieve + save all images belonging to a section data set (an experiment)
section_data_set_id = 531477700
all_image_ids = ecimg.get_all_section_image_ids(section_data_set_id)
ecimg.save_section_image(section_image_id, 'sample_image.jpg')



# calculate the PIR coordinates using ecallen
pir_from_ecallen = ecimg.xy_to_pir(x_test_pix, y_test_pix, section_dataset_id,
                                   section_image_id)

img = imread('sample_image.jpg')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.imshow(img)
plt.show()


if __name__ == '__main__':
    # organism, or ABA 'product', of interest
    organism = 'DevMouse'
    organism_genes = get_genes(organism)

    # our genes of interest
    gene_aliases = ['AA408225', ' 2600013A04Rik  ', 'AL117858']
    genes_of_interest = get_genes_from_aliases(gene_aliases, organism_genes)

    # get pandas df of experiments, df of image data, from list of gene acronyms/aliases, given organism
    exp_data, img_data = get_experiments_and_images(genes_of_interest, organism=organism)
    img_ids = img_data.id.values.tolist()

    # for each image, pull the raw image and save the file location in the image df
    organism_dir = os.path.join(DATA_DIR, organism)
    organism_params = get_organism_image_params(organism)

    # for each gene of interest
    image_paths = {image_id:None for image_id in img_ids}
    for gene_alias, gene_dict in genes_of_interest.items():
        print('getting experiments for gene with alias:', gene_alias, '\t acronym:', gene_dict['gene_acronym'])
        gene_id = gene_dict['gene_id']
        gene_name = gene_dict['gene_acronym']
        # get the directory for this gene
        gene_dir = os.path.join(organism_dir, gene_name)
        if not os.path.exists(gene_dir):
            print('\ndirectory ', gene_dir, ' doesnt exist yet, creating it .. ')
            os.mkdir(gene_dir)
        exp_ids = exp_data[exp_data['gene_id']==gene_id]['experiment_id']
        # for each experiment in this gene
        for exp_id in exp_ids:
            print('getting images for SectionDataSet: ', str(exp_id))
            # get the directory for the experiment
            exp_dir = os.path.join(gene_dir, str(exp_id))
            if not os.path.exists(exp_dir):
                print('\ndirectory ', exp_dir, ' doesnt exist yet, creating it .. ')
                os.mkdir(exp_dir)
            # get the images to save into the directory
            exp_imgs = img_data[img_data['experiment_id'] == exp_id]['id'].values.tolist()
            section_ct = 1
            for image_id in exp_imgs:
                # get image with params
                img_path = save_image_locally(exp_dir, image_id, section_ct, image_params=organism_params)
                image_paths[image_id] = img_path
                section_ct += 1