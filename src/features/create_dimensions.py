import os
import sys
import pandas as pd
import pickle

sys.path.append(os.path.join(os.getcwd(), "src"))
from data.make_dataset import get_tweets, get_fb_posts
from features.clean_data import clean_tweets, clean_fb_posts

THIS_DIR="/Users/mm40108/projects/voice-of-consumer_v1/src/features"
THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def clean_dimension(data, needed, nonull, ifnull_correct):
    """
    given a mostly cleaned data frame, make sure it's clean so as to not cause
    errors in plotting for a particular dimension, ie datetime

    :param data: mostly cleaned data frame
    :param needed: list of columns needed in final output
    :param nonull: list of columns which can't have any nulls, and rows should be dropped
    :param ifnull_correct: dict for correcting nulls by column {'colname':'fill na value', ...}
    :return: cleaned data
    """
    # make sure no nulls in key cols
    no_nas = data.dropna(axis=0, subset=nonull)

    # if there are nulls in these columns, fill them
    if any([any(pd.isnull(no_nas[fillcol])) for fillcol in ifnull_correct.keys()]):
        print('nulls found in ', ifnull_correct, 'cleaning ... ')
        no_nas = no_nas.fillna(value=ifnull_correct)
    else:
        print(ifnull_correct.keys(), ' had no nulls')

    final_data = no_nas[needed]
    print(final_data.dtypes)
    return final_data


def aggregate_time_data(df, time_col='date'):
    # https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/

    df['stream_type'] = df['stream'].map(str) + '-' + df['type'].map(str)

    agg_dict = {
        'likes':['sum'],
        'reposts':['sum'],
        'user_id':['count']
    }

    agg_df = df.groupby([time_col, 'stream_type']).agg(agg_dict)

    rename = {
        'likes':{'sum': 'total_likes'},
        'reposts':{'sum': 'total_shares'},
        'user_id':{'count': 'unique_users'}
    }

    new_cols = [time_col, 'stream_type']
    for col, d in rename.items():
        for fxn, new_col in d.items():
            agg_df[new_col] = df.groupby([time_col, 'stream_type']).agg(agg_dict)[col][fxn]
            new_cols.append(new_col)

    agg_df.reset_index(level=[time_col, 'stream_type'], inplace=True)
    agg_df.columns = agg_df.columns.droplevel(1)

    return agg_df[new_cols]

def get_time_dim_data(streams=['twitter', 'facebook'], refresh=False):
    needed_cols = ['datetime', 'date', 'time', 'id', 'place', 'stream', 'type', 'likes', 'reposts',
                   'user_id', 'user_name', 'user_handle',
                   'raw_text', 'clean_text', 'sensitive']
    nonull_cols = ['datetime', 'id']

    filepath = os.path.join(THIS_DIR, '../', '../', 'data', 'time_dim_data.obj')
    if refresh is False:
        print('reading from ', filepath)
        with open(filepath, 'rb') as f:
            df = pickle.load(f)
            agg_df = aggregate_time_data(df)
        agg_datetime = aggregate_time_data(df, time_col='datetime')
        agg_date = aggregate_time_data(df)
        return df, agg_datetime, agg_date

    # empty df to add to
    df = pd.DataFrame(columns = needed_cols)

    ## TWITTER ##
    if 'twitter' in streams:
        data = get_tweets()
        cleaned = clean_tweets(data)
        ifnull_correct_cols = {'stream': 'twitter', 'type': 'tweet'}
        twitter_time = clean_dimension(cleaned, needed_cols, nonull_cols, ifnull_correct_cols)
        df = pd.concat([df, twitter_time]) if df.shape[0] > 0 else twitter_time

    if 'facebook' in streams:
        data = get_fb_posts()
        cleaned = clean_fb_posts(data)
        ifnull_correct_cols = {'stream': 'facebook', 'type': 'post'}
        fb_time = clean_dimension(cleaned, needed_cols, nonull_cols, ifnull_correct_cols)
        df = pd.concat([df, fb_time]) if df.shape[0] > 0 else fb_time

    print('saving all time dim data for streams', ', '.join([i for i in streams]), ' to ', filepath)
    with open(filepath, 'wb') as f:
        pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)

    agg_datetime = aggregate_time_data(df, time_col='datetime')
    agg_date = aggregate_time_data(df)
    return df, agg_datetime, agg_date




# if __name__ == '__main__':
#
    # """
    # for each data stream, create a dataset that provides data for all charts
    # where x = datetime and each row is a unique post
    # """
    # needed_cols = ['datetime', 'id', 'place', 'stream', 'type', 'likes', 'reposts']
    # nonull_cols = ['datetime', 'id']
    #
    # ## TWITTER ##
    # data = get_tweets()
    # cleaned = clean_tweets(data)
    # ifnull_correct_cols = {'stream':'twitter', 'type':'tweet'}
    #
    # twitter_time = clean_dimension(cleaned, needed_cols, nonull_cols, ifnull_correct_cols)

    # 'twitter' in set(no_nas['stream'].values)
    # set(no_nas['type'].values.tolist())



