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

    # organism_params = get_organism_image_params(organism)

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
                # img_path = save_image_locally(exp_dir, image_id, section_ct, image_params=organism_params)
                img_path = save_image_locally(exp_dir, image_id, section_ct)
                image_paths[image_id] = img_path
                section_ct += 1