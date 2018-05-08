import os
import sys
from flask import Flask, render_template, flash, request, make_response
from bokeh.embed import components
import holoviews as hv

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

sys.path.append(os.path.join(os.getcwd(), "src"))
from data.ABA_utils import get_genes, get_genes_from_aliases, get_experiment_data, \
    get_experiments_and_images
from features.image_processing import get_all_processed_experiments
from visualization.plot_utils import sine_example
# from app.app_forms import IngestionForm
# from app.app_tables import ProductTable, GeneTable
from app_forms import IngestionForm, ProcessingForm
from app_tables import ProductTable, GeneTable

THIS_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

# Creates an instance of a flask application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'

# specify holoview to be served by bokeh
hv.extension('bokeh')

"""  The routes are the different URLs that the application implements. In
Flask, handlers for the application routes are written as Python functions,
called view functions. View functions are mapped to one or more route URLs so
that Flask knows what logic to execute when a client requests a given URL.

use decorators (ie @app.route) to modify the fxn immediately after it. here, 
we use @app.route to associate the URL it was passed with the fxn following 
it, so that when a web browser seeks the URL(s) passed, Flask invokes the fxn
"""

ingestion_choices = {'product':'DevMouse', 'genes':[]}
processing_choices = {'gene':None, 'gene_exp_data':None, 'gene_img_data':None, 'experiment':None, 'image':None}


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/ingestion', methods=['GET', 'POST'])
def ingest_data():
    print('ingest_data()')
    form = IngestionForm(request.form)
    table = {}
    print
    form.errors
    if request.method == 'POST':
        print('keys ', request.form.keys())
        if 'products' in request.form.keys():
            print('products in request form keys')
            # first select organism
            product = request.form['products']
            print('\n\nproduct selected:', product)
            genes = get_genes(product)
            gene_choices = genes[['acronym', 'alias_tags']].sort_values(by='acronym')
            gene_choices = [(i[0], str(i[0]) + ' ' + str(i[1])) for i in gene_choices.values.tolist()]
            print('\n\ngene choices:', gene_choices[1:5])
            table = genes.to_dict()
            ingestion_choices['product'] = product
            form.set_genes(gene_choices)
        if 'genes' in request.form.keys():
            print('genes in request form keys')
            genes = get_genes(ingestion_choices['product'])
            gene = form.genes.data
            print('\n\ngene selected:', gene, type(gene))
            gene_ids = get_genes_from_aliases(gene, genes)
            print('\ngene ids:', gene_ids)
            gene_data = get_experiments_and_images(gene, organism='DevMouse')[0]
            ingestion_choices['genes'] = gene_ids
            print('gen_ids:', gene_ids)
            table = gene_data.to_dict()
            print(table)
    return render_template('ingestion_form.html', form=form, table=table)


@app.route('/image_processing')
def processing_dashboard():
    print(ingestion_choices['genes'])
    gene_choices = [(gene_name, gene_name) for gene_name in ingestion_choices['genes']]
    print('gene choices: ', gene_choices[1:5])
    exp_data, img_data = get_experiments_and_images(ingestion_choices['genes'], ingestion_choices['product'])
    exp_choices = [(exp_id, exp_id) for exp_id in
                   exp_data.experiment_id.values.tolist()]
    print('experiment choices:', exp_choices[1:5])
    img_choices = [(img_id, img_id) for img_id in img_data]
    print('image choices:', img_choices[1:5])
    form = ProcessingForm(request.form, gene_choices)
    form.set_genes(gene_choices)
    print
    form.errors
    if request.method == 'POST':
        print('keys ', request.form.keys())
        if 'gene' in request.form.keys():
            print('gene in request form keys')
            # first select organism
            gene = request.form['gene']
            print('\n\ngene selected:', gene)
            exp_data, img_data = get_experiments_and_images([gene], ingestion_choices['product'])
            table = exp_data.to_dict()
            processing_choices['gene'] = gene
            processing_choices['gene_exp_data'] = exp_data
            processing_choices['gene_img_data'] = img_data
            # update the experiment options
            exp_choices = [(exp_id, exp_id) for exp_id in exp_data.experiment_id.values.tolist()]
            form.set_experiments(exp_choices)
        if 'experiment' in request.form.keys():
            print('experiment in request form keys')
            exp_id = request.form['experiment']
            print('chosen experiemtn: ', exp_id)
            # update the image options
            img_data = processing_choices['gene_img_data']
            selected_img_data = img_data[img_data.experiment_id == exp_id]['id'].values.tolist()
            img_choices = [(img_id, img_id) for img_id in selected_img_data]
            form.set_images(img_choices)
        if 'image' in request.form.keys():
            print('image in request form keys')
            img_id = request.form['image']
            print('chosen image: ', img_id)


    # get_experiment_data(ingestion_choices['genes'])
    plot = sine_example()
    script, div = components(plot)
    return render_template("image_processing.html", script=script, div=div, form=form)


@app.route('/image_registration')
def registration_dashboard():
    plot = sine_example()
    script, div = components(plot)
    return render_template("image_registration.html", script=script, div=div)


@app.route('/image_analysis')
def analysis_dashboard():
    plot = sine_example()
    script, div = components(plot)
    return render_template("image_analysis.html", script=script, div=div)

@app.route('/viz')
def viz_dashboard():
    plot = sine_example()
    script, div = components(plot)
    return render_template("viz.html", script=script, div=div)

# # testing? use this ..
# # route /, and /index to a test function
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)