import os
import sys
from flask_table import Table, Col
from wtforms import Form, Field, SelectField, BooleanField, TextField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets.core import HTMLString, html_params, escape, TextInput

sys.path.append(os.path.join(os.getcwd(), "src"))
from data.ABA_utils import get_products, get_organisms, get_genes, \
    get_genes_from_aliases, get_experiment_data, get_experiments_and_images


class ProductTable(Table):
    acronym = Col('acronym')
    alias_tags = Col('alias_tags')
    chromosome_id = Col('chromosome_id')
    ensembl_id = Col('ensembl_id')
    entrez_id = Col('entrez_id')
    genomic_reference_update_id = Col('genomic_reference_update_id')
    homologene_id = Col('homologene_id')
    gene_id = Col('gene_id')
    legacy_ensembl_gene_id = Col('legacy_ensembl_gene_id')
    name = Col('name')
    organism_id = Col('organism_id')
    original_name = Col('original_name')
    original_symbol = Col('original_symbol')
    reference_genome_id = Col('reference_genome_id')
    sphinx_id = Col('sphinx_id')
    version_status = Col('version_status')

class GeneTable(Table):
    blue_channel = Col('blue_channel')
    delegate = Col('delegate')
    expression = Col('expression')
    failed = Col('failed')
    failed_facet = Col('failed_facet')
    green_channel = Col('green_channel')
    id = Col('id')
    name = Col('name')
    plane_of_section_id = Col('plane_of_section_id')
    qc_date = Col('qc_date')
    red_channel = Col('red_channel')
    reference_space_id = Col('reference_space_id')
    rnaseq_design_id = Col('rnaseq_design_id')
    section_thickness = Col('section_thickness')
    specimen_id = Col('specimen_id')
    sphinx_id = Col('sphinx_id')
    storage_directory = Col('storage_directory')
    weight = Col('weight')


class Product(object):
    def __init__(self, acronym, alias_tags, chromosome_id, ensembl_id,
                 entrez_id, genomic_reference_update_id, homologene_id,
                 gene_id, legacy_ensembl_gene_id, name, organism_id,
                 original_name, original_symbol, reference_genome_id,
                 sphinx_id, version_status):
        self.acronym = acronym
        self.alias_tags = alias_tags
        self.chromosome_id = chromosome_id
        self.ensembl_id = ensembl_id
        self.entrez_id = entrez_id
        self.genomic_reference_update_id = genomic_reference_update_id
        self.homologene_id = homologene_id
        self.gene_id = gene_id
        self.legacy_ensembl_gene_id = legacy_ensembl_gene_id
        self.name = name
        self.organism_id = organism_id
        self.original_name = original_name
        self.original_symbol = original_symbol
        self.reference_genome_id = reference_genome_id
        self.sphinx_id = sphinx_id
        self.version_status = version_status

class Gene(object):
    def __init__(self, blue_channel, delegate, expression, failed, failed_facet,
                 green_channel, id, name, plane_of_section_id, qc_date, red_channel,
                 reference_space_id, rnaseq_design_id, section_thickness, specimen_id,
                 sphinx_id, storage_directory, weight):
        self.blue_channel = blue_channel
        self.delegate = delegate
        self.expression = expression
        self.failed = failed
        self.failed_facet = failed_facet
        self.green_channel = green_channel
        self.id = id
        self.name = name
        self.plane_of_section_id = plane_of_section_id
        self.qc_date = qc_date
        self.red_channel = red_channel
        self.reference_space_id = reference_space_id
        self.rnaseq_design_id = rnaseq_design_id
        self.section_thickness = section_thickness
        self.specimen_id = specimen_id
        self.sphinx_id = sphinx_id
        self.storage_directory = storage_directory
        self.weight = weight