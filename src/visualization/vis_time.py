import os
import sys
import holoviews as hv

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.layouts import layout

from bokeh.models import Slider, Button

from holoviews.streams import Pipe, Buffer, BoundsX
from holoviews.plotting.bokeh.element import (line_properties, fill_properties,
                                              text_properties)


sys.path.append(os.path.join(os.getcwd(), "src"))
from src.features.create_dimensions import get_time_dim_data

THIS_DIR="/Users/mm40108/projects/voice-of-consumer_v1/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

hv.extension('bokeh')

""" 
the definitions in this module return holoviews components (ie hv.Curve) 
http://holoviews.org/reference/index.html 
out of a single data source which is only called once
"""
# datasets = ['twitter', 'facebook']
# data, agg_data = get_time_dim_data(streams=datasets)
# print('\n\n time vis datasets:', datasets, data.shape, data.dtypes)

# trying to figure out how to view locally...
# from bokeh.server.server import Server
# renderer = hv.renderer('bokeh')
# app = renderer.app(hvtable)
# server = Server({'/': app}, port=5006)
# renderer.app(hvtable, show=True, websocket_origin='localhost:5006')

def get_hvtable(cols=[]):
    # make a holoviews table from pandas df
    # http://holoviews.org/user_guide/Tabular_Datasets.html
    df = data[cols] if len(cols) > 0 else data
    hvtable = hv.Table(df)
    print('\n\n hv.Table:', hvtable.columns())
    return hvtable, df

def time_curve(df, y = 'likes', color = 'stream', x = 'datetime'):
    """
    a simple line graph where x = datetime (could be any continuous)

    plot counts of interactions by data stream
    :param x:
    :param y:
    :param color:
    :return:
    """
    # data should be a list of tuples [(x, y),...] , or hv table
    curve = hv.Curve(df, x, y, group="time curve")
    spikes = hv.Spikes(df, x, vdims=[])

    def make_from_boundsx(boundsx):
        sub = df.set_index(x).loc[boundsx[0]:boundsx[1]]
        return hv.Table(sub.describe().reset_index().values)

    # dates = df['datetime'].tolist()
    #
    # + hv.DynamicMap(make_from_boundsx, streams=[
    #     BoundsX(source=curve, boundsx=(min(dates), max(dates)))])

    return curve, spikes



def time_scatter(y='likes', color='user_id', x='datetime'):
    # http://holoviews.org/reference/elements/matplotlib/Points.html#matplotlib-gallery-points
    # scatterplot - pass a list of lists, where the lists are coords
    # points = [data['timestamp'], data['text']]
    # scatter = hv.Points(points, group="plot counts of interactions, by data streams")
    _, data = get_hvtable()
    points = hv.Points((data[x], data[y]), group="time curve")
    return points



def time_layout():
    hvdata, df = get_hvtable(cols=['datetime', 'likes', 'user_id', 'raw_text', 'user_name', 'user_handle'])
    curve, spikes = time_curve(df)
    curve = curve.opts(plot=dict(width=800))
    spikes = spikes.opts(plot=dict(width=800, height=100))
    # tbl = hvdata

    scatter = time_scatter().opts(plot=dict(width=800))

    layout = (curve + spikes + scatter).cols(1)

    renderer = hv.renderer('bokeh').instance(mode='server')
    rendered_layout = renderer.get_plot(layout)
    # t1 = renderer.get_plot(get_hvtable())

    # hv.DynamicMap(t1, streams=[Buffer(sdf.x, length=10)]) + hv.DynamicMap(
    #     partial(hv.BoxWhisker, kdims=[], vdims='x'),
    #     streams=[Buffer(sdf.x, length=100)])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           '''')
    return hv.renderer('bokeh').server_doc(rendered_layout)

# def streams_over_time(x="time", y="count", color="stream"):
#     """
#     plot counts of interactions by data stream
#     :param x:
#     :param y:
#     :param color:
#     :return:
#     """
#     data = get_tweets()
#     time_col = 'timestamp'
#     text_col = 'text'
#
#     # remove rows with nulls in these columns
#     no_nulls = [text_col, time_col]
#     data = data.dropna(axis=0, subset=no_nulls)
#
#     # scatterplot - pass a list of lists, where the lists are coords
#     points = [data['timestamp'], data['text']]
#     scatter = hv.Points(points, group="plot counts of interactions, by data "
#                                       "streams").opts(plot=dict(height=500,width=800))
#
#     # final_layout = renderer.get_plot(scatter)
#     # return hv.renderer('bokeh').server_doc(final_layout)
#     return renderer.get_plot(points)