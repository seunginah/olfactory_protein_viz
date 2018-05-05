import os
import sys
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.io import curdoc
import holoviews as hv

sys.path.append(os.path.join(os.getcwd(), "src"))

THIS_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz" \
           "/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

# Creates an instance of a flask application
app = Flask(__name__)

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


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/testing')
def test_plot():
    plot = time_layout()
    script, div = components(plot)
    return render_template("testing.html", script=script, div=div)

@app.route('/basic_overview').
def basic_overview_dashboard():
    plot = basic_overview_layout()
    script, div = components(plot)
    return render_template("basic_overview.html", script=script, div=div)


# # testing? use this ..
# # route /, and /index to a test function
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

# # testing? use this ..
# # route /, and /index to a test holoviews plot
# @app.route('/')
# @app.route('/index')
# def index():
#     plot = sine_example()
#     script, div = components(plot)
#     return render_template("testing.html", script=script, div=div)

# # testing? use this ..
# # route /, and /index to a test holoviews layout document
# @app.route('/')
# @app.route('/index')
# def index():
#     doc = twitter_layout()
#     script, div = components(doc)
#     return render_template("testing.html", script=script, div=div)

if __name__ == "__main__":
    app.run(port=5000, debug=True)