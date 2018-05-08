import sys
import os
import pandas as pd
import requests

sys.path.append(os.path.join(os.getcwd(), "src"))

#
# resources
#

# RMA: http://help.brain-map.org/pages/viewpage.action?pageId=5308449#RESTfulModelAccess(RMA)-Criteria
# RMA query builder: http://api.brain-map.org/examples/rma_builder/rma_builder.html
# example queries: http://help.brain-map.org/display/api/Example+Queries+for+Experiment+Metadata

#
# GLOBAL VARIABLES
#

all_data_base = "http://api.brain-map.org/api/v2/data/query.json"

# criteria
model_c_base = "criteria=model::"
c_base = "rma::criteria"

# rows
all_rows = "num_rows=all"


def get_organisms():
    all_products_query = "http://api.brain-map.org/api/v2/data/Organism/query.json"
    r = requests.get(all_products_query).json()
    # put the results into a pandas dataframe
    return pd.DataFrame(r['msg'])


def get_products(atlases_only=True):
    all_products_query = "http://api.brain-map.org/api/v2/data/Product/query.json"
    r = requests.get(all_products_query).json()
    # put the results into a pandas dataframe
    df = pd.DataFrame(r['msg'])
    if atlases_only:
        return df[df['resource'].str.contains('Atlas')]
    else:
        return df


def get_genes(organism='DevMouse', by='abbreviation'):
    u = "\nusage: get_genes(organism) \norganism = 'all' | <organism abbreviation name> "
    # model
    genes_base = "http://api.brain-map.org/api/v2/data/Gene/query.json"
    # model criteria
    genes_model_c = model_c_base + "Gene"

    # modify the query as needed
    if organism == 'all':
        # all genes in Allen Brain Atlas
        # only return the first 50 rows of the query
        q = genes_base
    else:
        organism_c = "products[" + by + "$eq'" + organism + "']"
        criteria = ",".join([genes_model_c, c_base, organism_c])
        rows =  "&" + all_rows
        q = genes_base + "?" + criteria + rows

    # get the response, put into pandas df
    print('\tattempting query:', q)
    r = requests.get(q).json()
    df = pd.DataFrame(r['msg']).rename(index=str, columns={'id': 'gene_id'})
    print('\tresponse:', df.shape, '\n\t', df.columns)
    return df


def search_col_list(col1, col2, col3, id_col, search_for):
    """
    search thru 3 diff columns to see if aliases match, return id of matching genes

    :param col1: column to search thru, which may be a space delimited list
    :param col2: column to search thru, which may be a space delimited list
    :param col3: column to search thru, which may be a space delimited list
    :param id_col: id column, return if id belongs to a gene searched for
    :param search_for: list of genes to search this row for
    :return:
    """
    t1 = col1.split() if col1 else []
    t2 = col2.split() if col2 else []
    t3 = col3.split() if col3 else []
    tokens = t1 + t2 + t3
    found_gene = False
    for gene in search_for:
        if gene.strip() in tokens:
            print(tokens)
            print('found ', gene, ' has id ', id_col)
            return gene, id_col
    if not found_gene:
        return None


def get_gene_ids(gene_aliases, organism_genes):
    """
    given a list of genes (and possibly their aliases), and a pandas df of gene data to search through

    :param gene_aliases: list of correctly spelled gene acronyms, original symbols, or aliases, which may have whitespace
    :param organism_genes: a pandas dataframe of genes to search through
    :return: dict {searched gene alias: gene id}
    """
    gene_ids = (organism_genes
                .apply(lambda row: search_col_list(row['acronym'], row['alias_tags'], row['original_symbol'], row['gene_id'], search_for=gene_aliases), axis=1)
                .dropna()
                .tolist())

    gene_dict = {tup[0]:tup[1] for tup in gene_ids}
    print('\nresults of searching for ', gene_aliases, '\n\t', gene_dict)
    return gene_dict


def get_genes_from_aliases(gene_aliases, organism_genes):
    alias_to_id = get_gene_ids(gene_aliases, organism_genes)
    gene_dict = {gene_alias:{'gene_id':gene_id, 'gene_acronym':None} for gene_alias, gene_id in alias_to_id.items()}
    for gene_alias, gene_id in alias_to_id.items():
        gene_acronym = organism_genes[organism_genes['gene_id']==gene_id]['acronym'].values.tolist()[0]
        gene_dict[gene_alias]['gene_acronym'] = gene_acronym
    return gene_dict


def get_experiment_data(gene_id, organism='DevMouse'):
    """
    get all experiments available for a gene for the given organism
    add the gene id as a column "gene_id" in result

    :param gene: int - gene id
    :param organism: str - organism abbreviation
    :return: pandas df of all experiments (section data sets)
    """
    print('getting all experiments for gene_id', str(gene_id))
    # model, model criteria
    experiment_base = all_data_base
    experiment_model_c = model_c_base + "SectionDataSet"

    # modify the query as needed
    organism_c = "products[abbreviation$eq'" + organism + "']"
    slice_c = "plane_of_section[name$eq'sagittal']"
    genes_c = "genes[id$eq'" + str(gene_id) + "']"
    criteria = ",".join([experiment_model_c, c_base, organism_c, slice_c, genes_c])
    rows = "&" + all_rows

    # assemble query
    q = experiment_base + "?" + criteria + rows

    # get the response, put into pandas df
    print('\tattempting query:', q)
    r = requests.get(q).json()
    df = pd.DataFrame(r['msg'])
    print('\tresponse:', df.shape, '\n\t', df.columns)
    return df


def get_image_data(experiment_id, organism='DevMouse'):
    print('getting all images for experiment_id', str(experiment_id))
    # model, model criteria
    image_base = all_data_base
    image_model_c = model_c_base + "SectionImage"

    # given id, format experiment criteria
    image_c_by_id = lambda id: "[data_set_id$eq" + str(id) + "]"

    criteria = ",".join([image_model_c, c_base, image_c_by_id(experiment_id)])
    rows = "&" + all_rows

    # assemble query
    q = image_base + "?" + criteria + rows

    # get the response, put into pandas df
    print('\tattempting query:', q)
    r = requests.get(q).json()
    df = pd.DataFrame(r['msg'])
    print('\tresponse:', df.shape, '\n\t', df.columns)
    return df


def get_experiments_and_images(gene_aliases, organism='DevMouse'):
    # get a pandas df of all genes in the organism
    organism_genes = get_genes(organism)
    gene_aliases_to_ids = get_gene_ids(gene_aliases, organism_genes)

    # collect all the experiment data pertaining to the 3 proteins into a pandas df
    all_experiments = None
    for gene_alias, gene_id in gene_aliases_to_ids.items():
        print(gene_alias)
        gene_experiments = get_experiment_data(gene_id, organism=organism)
        gene_experiments['gene_id'] = gene_id
        if all_experiments is None:
            all_experiments = gene_experiments
        else:
            all_experiments = pd.concat([all_experiments, gene_experiments])
    if all_experiments is not None:
        all_experiments = all_experiments.rename(index=str, columns={'id': 'experiment_id'})

    # collect all the image data for all experiments pertaining to the 3 proteins
    experiment_ids = all_experiments.experiment_id.values.tolist()
    all_images = None
    for experiment_id in experiment_ids:
        image_df = get_image_data(experiment_id, organism=organism)
        image_df['experiment_id'] = experiment_id
        if all_images is None:
            all_images = image_df
        else:
            all_images = pd.concat([all_images, image_df])

    return all_experiments, all_images


if __name__ == '__main__':
    # test aliases for Cdh5, Robo2, Bmpr2 respectively
    gene_aliases = ['AA408225', ' 2600013A04Rik  ', 'AL117858']
    organism = 'DevMouse'

    # get pandas df of experiments, df of image data, from list of gene acronyms/aliases, given organism
    exp_data, img_data = get_experiments_and_images(gene_aliases, organism=organism)

    # save df under the organiam






