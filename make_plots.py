import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.io import show

from surface3d import Surface3d
from utils import read_full_csv, get_segment_coords


if __name__ == '__main__':
    """ Let's use the data from Final_dataset.csv and some toy segment coords to practice plotting 3d surface """

    # pull + join pixel intensities and coordinates
    cols = ["protein", "image", "zone", "segment", "avg_pix_intensity"]
    full_dataset = read_full_csv(cols)
    coords = get_segment_coords()

    # let's just look at the bmpr2 slices
    bmpr2 = (full_dataset[full_dataset['protein']=='Bmpr2']
             .join(coords.set_index('segment'), on='segment', how='left')
             .dropna(how='any'))

    # use color to distinguish the zones
    bmpr2['z'] = bmpr2['image'] * 100
    bmpr2['color'] = bmpr2['avg_pix_intensity']
    bmpr2 = bmpr2[['x','y','z','color']].drop_duplicates()
    surface = Surface3d(x="x", y="y", z="z", color="color", data_source=ColumnDataSource(data=bmpr2))

    show(surface)



x = np.arange(0, 300, 10)
y = np.arange(0, 300, 10)
xx, yy = np.meshgrid(x, y)
xx = xx.ravel()
yy = yy.ravel()
value = np.sin(xx/50) * np.cos(yy/50) * 50 + 50

source = ColumnDataSource(data=dict(x=xx, y=yy, z=value, color=value))

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

show(surface)