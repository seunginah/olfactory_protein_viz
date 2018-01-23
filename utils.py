import pandas as pd
import numpy as np
import os

THIS_DIR = '/Users/mm40108/projects/datadays17/olfactory_protein_viz'
THIS_DIR = (
    os.path.dirname(
        os.path.realpath(__file__)))

# datatypes to read in Final_dataset.csv
# TODO: fix the bug that causes some digits like "204.342" to be exported to csv as "204.342." which makes them interpreted as strings
our_dtypes = {
    "row_index": np.int32,
    "row_id": np.int8,
    "protein": str,
    "image": str,
    "zone": str,
    "segment": str,
    "area": np.float64,
    "std_dev": np.float64,
    "std_error": np.float64,
    "avg_pix_intensity": np.float64,
    "num_pix": np.float64,
    "pix_value": np.int32,
    "pix_freq": np.int32
}

def get_segment_coords(file=os.path.join(THIS_DIR, 'segment_coord_lookup.csv')):
    """
    read in segment coords and return them in a pandas dataframe
     TODO: use image registration to populate the x, y coordinates for each image slice
     """
    return pd.read_csv(file, dtype={'segment':int,'x':int, 'y':int})


def read_full_csv(cols=None, file=os.path.join(THIS_DIR, 'Final_dataset.csv')):
    """
    read in the Final_dataset.csv file, return a pandas dataframe

    Args:
        cols - if not none, return only these columns
    """
    data = pd.read_csv(file, dtype=our_dtypes)
    # TODO: some "segments" don't have a letter and contain zones
    data = data[data['segment'].str.contains('(\d)')]
    data['image'] = data['image'].str.extract('(\d)').astype(int)
    data['segment'] = data['segment'].str.extract('(\d)').astype(int)
    if cols is not None:
        data = data[cols]
    return data.drop_duplicates()