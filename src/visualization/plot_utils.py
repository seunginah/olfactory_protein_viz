import os
import sys
import numpy as np
import holoviews as hv

# Bokeh
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.layouts import layout
from bokeh.models import Slider, Button
#
# from holoviews.plotting.bokeh.element import (line_properties, fill_properties,
#                                               text_properties)

sys.path.append(os.path.join(os.getcwd(), "src"))


THIS_DIR="/Users/mm40108/projects/voice-of-consumer_v1/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

# renderer = hv.renderer('bokeh').instance(mode='server')

#
# def get_properties():
#     print("""
#     Line properties: %s\n
#     Fill properties: %s\n
#     Text properties: %s
#     """ % (line_properties, fill_properties, text_properties))



def sine(phase):
    xs = np.linspace(0, np.pi * 4)
    return hv.Curve((xs, np.sin(xs + phase))).opts(plot=dict(width=800))

stream = hv.streams.Stream.define('Phase', phase=0.)()
sine_dmap = hv.DynamicMap(sine, streams=[stream])

def sine_example():
    renderer = hv.renderer('bokeh').instance(mode='server')
    # Create HoloViews plot and attach the document
    hvplot = renderer.get_plot(sine_dmap)

    # Create a slider and play buttons
    def animate_update():
        year = slider.value + 0.2
        if year > end:
            year = start
        slider.value = year

    def slider_update(attrname, old, new):
        # Notify the HoloViews stream of the slider update
        stream.event(phase=new)

    start, end = 0, np.pi * 2
    slider = Slider(start=start, end=end, value=start, step=0.2, title="Phase")
    slider.on_change('value', slider_update)

    # Combine the holoviews plot and widgets in a layout
    plot = layout([[hvplot.state], [slider]], sizing_mode='fixed')
    return plot

def scatter_plot():
    xs = [0.1* i for i in range(100)]
    scatter = hv.Scatter((xs[::5], np.linspace(0, 1, 20)))
    return scatter

def curve_plot():
    xs = [0.1* i for i in range(100)]
    curve =  hv.Curve((xs, [np.sin(x) for x in xs]))
    return curve

def tsne_plot(source, df_name, tools, title):
    plot_tsne = figure(plot_width=700,
                       plot_height=700,
                       tools=tools,
                       title=title)
    plot_tsne.circle('x',
                     'y',
                     size='size',
                     fill_color='colors',
                     alpha='alpha',
                     line_alpha=0,
                     line_width=0.01,
                     source=source,
                     name=df_name)

    return plot_tsne

def slider_over_year(source, min, max, default=2018, slider_title=''):


    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['y']
        colors = data['colors']
        alpha = data['alpha']
        title = data['title']
        year = data['year']
        size = data['size']
        for (i = 0; i < x.length; i++) {
            if (year[i] <= f) {
                alpha[i] = 0.9
                size[i] = 7
            } else {
                alpha[i] = 0.05
                size[i] = 4
            }
        }
        source.trigger('change');
    """)

    slider = Slider(start=min, end=max, value=default, step=1, title=slider_title)
    slider.js_on_change('value', callback)
    return slider