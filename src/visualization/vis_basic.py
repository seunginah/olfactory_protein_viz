import os
import sys
import holoviews as hv
from bokeh.layouts import layout

sys.path.append(os.path.join(os.getcwd(), "src"))
from data.ABA_utils import get_organisms, get_genes, get_genes_from_aliases, get_experiment_data, get_experiments_and_images

THIS_DIR="/Users/mm40108/projects/voice-of-consumer_v1/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

hv.extension('bokeh')
#renderer = hv.renderer('bokeh').instance(mode='server')
# renderer = hv.renderer('bokeh')


def


#
#
# def time_line_chart(x="time", y="count", color="stream"):
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
#     scatter = hv.Points(points, group="plot counts of interactions, by data streams")
#
#     final_layout = renderer.get_plot(scatter)
#     return hv.renderer('bokeh').server_doc(final_layout)
#
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
#
#
#
# def streams_over_location(x="x", y="y", time="time", color="stream"):
#     """
#     plot interactions by data stream onto a map,
#
#     :param x:
#     :param y:
#     :param time:
#     :param color:
#     :return:
#     """
#     tmp = scatter_plot()
#     return tmp
#
#
# def line_chart1():
#     # get data
#     tweets = get_tweets()
#     # clean data
#     data = tweets[tweets['comment_date'].isnull()==False]
#     data = data[data['sentiment_value'].isnull()==False]
#
#     # print(any(data.))
#
#     # make chart
#     title = 'chart title'
#     x_name = 'comment_date'
#     y_name = 'sentiment_value'
#     return None
#
#
# def basic_overview_layout():
#     x = curve_plot().relabel(group="Counting interactions, by stream").opts(plot=dict(height=500,width=800))
#     y = streams_over_location().relabel(group="Localizing interactions").opts(plot=dict(height=500,width=800))
#     layout = x + y
#
#     return hv.renderer('bokeh').server_doc(layout)
#
#
# ##### TEST
# def dummy_layout_simple():
#     x = scatter_plot().relabel(group="DUMMY PLOT 3")
#     return hv.renderer('bokeh').server_doc(x)
#
# def dummy_layout():
#     x = scatter_plot().relabel(group="DUMMY PLOT 1")
#     y = curve_plot().relabel(group="DUMMY PLOT 2")
#     layout = x + y
#     return hv.renderer('bokeh').server_doc(layout)