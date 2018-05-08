import os
import sys
from flask import Markup
from wtforms import Form, Field, SelectField, SelectMultipleField, TextField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets.core import HTMLString, html_params, escape, TextInput

sys.path.append(os.path.join(os.getcwd(), "src"))
from data.ABA_utils import get_products, get_organisms, get_genes, \
    get_genes_from_aliases, get_experiment_data, get_experiments_and_images


class InlineButtonWidget(object):
    html_params = staticmethod(html_params)

    def __init__(self, input_type='submit', text=''):
        self.input_type = input_type
        self.text = text

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return Markup('<button type="submit" %s><span>%s</span></button>'
                      % (self.html_params(name=field.name, **kwargs), field.text))


class InlineButton(Field):
  widget = InlineButtonWidget()

  def __init__(self, label=None, validators=None, text='Save', **kwargs):
    super(InlineButton, self).__init__(label, validators, **kwargs)
    self.text = text

  def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''


class OrganismForm(Form):
    # get organism choices
    all_organisms = get_organisms()
    choices = [(i[0], i[1]) for i in all_organisms[['name', 'tags']].values.tolist()]
    organism = SelectField('Field name', choices=choices, validators=[DataRequired()])


class Select2DImageForm(Form):
    choices = []
    experiments = SelectField('Select from available experiments: ', choices=choices)


class Select3DImageForm(Form):
    choices = []
    experiments = SelectField('Select from available experiments: ', choices=choices)


class IngestionForm(Form):
    print('\nIngestionForm')
    # 1. get product choices
    products = SelectField('Product', validators = [DataRequired()])
    # 2. get genes in that product
    genes = SelectMultipleField('Gene', validators = [DataRequired()])

    def __init__(self, *args, **kwargs):
        super(IngestionForm, self).__init__(*args, **kwargs)
        all_products = get_products(atlases_only=True)
        self.products.choices = [(i[0], i[1]) for i in all_products[['abbreviation', 'name']].values.tolist()]
        self.genes.choices = [('Bmpr2', 'Bmpr2 2610024H22Rik AL117858 AW546137 BB189135 BMP-2 BMPR-2 BMPRII BMPR-II BRK-3 Gm20272')]

    def set_genes(self, choices):
        print('setting genets')
        self.genes.choices = choices

class ProcessingForm(Form):
    print('\nProcessingForm')
    # 1. get product choices
    gene = SelectField('Gene', validators = [DataRequired()])
    # 2. get genes in that product
    experiment = SelectField('Experiment', validators = [DataRequired()])
    # 2. get genes in that product
    image = SelectField('Image', validators=[DataRequired()])


    def __init__(self, gene_choices, experiment_choices, image_choices):
        super(ProcessingForm, self).__init__(*args, **kwargs)
        self.gene.choices = gene_choices
        self.experiment.choices = experiment_choices
        self.image.choices = image_choices

    def set_genes(self, choices):
        print('setting gene')
        self.gene.choices = choices

    def set_experiments(self, choices):
        print('setting experiment')
        self.experiment.choices = choices

    def set_images(self, choices):
        print('setting images')
        self.image.choices = choices
