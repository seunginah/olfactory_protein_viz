import os
import sys
import holoviews as hv

sys.path.append(os.path.join(os.getcwd(), "src"))
from visualization.plot_utils import scatter_plot, curve_plot, lda_example
from data.make_dataset import get_tweets

THIS_DIR="/Users/mm40108/projects/voice-of-consumer_v1/src/app"
THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

hv.extension('bokeh')
renderer = hv.renderer('bokeh').instance(mode='server')

#
# data stuff
#
def twitter_layout():
    x = scatter_plot()
    y = lda_example()
    z = curve_plot()


    final_layout = renderer.get_plot(x + y + z)
    return hv.renderer('bokeh').server_doc(final_layout)




def line_chart1():
    # get data
    tweets = get_tweets()
    # clean data
    data = surveys[surveys['comment_date'].isnull()==False]
    data = data[data['sentiment_value'].isnull()==False]

    # print(any(data.))

    # make chart
    title = 'chart title'
    x_name = 'comment_date'
    y_name = 'sentiment_value'


    return None

