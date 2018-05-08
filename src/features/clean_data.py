import os
import sys
import re
import numbers
import numpy as np
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.getcwd(), "src"))
THIS_DIR = os.path.dirname(os.path.realpath(__file__))


# dates and times
def parse_date(x, time_or_date, try_format='%a %b %d %H:%M:%S %z %Y'):
    try:
        dt = datetime.strptime(x, try_format)
    except ValueError:
        print('parse_date(): error parsing ', str(x), ' as date')
        return None

    if time_or_date == 'date':
        return datetime.date(dt)
    elif time_or_date == 'time':
        return datetime.time(dt)
    else:
        return dt


def remove_nontype(x, keep_type='numeric'):
    # if its not a number try converting
    if keep_type == 'numeric':
        if not isinstance(x, (int, numbers.Number)):
            try:
                x = float(x)
            except ValueError:
                print('remove_nontype(): couldnt convert ', str(x), 'to', keep_type)
                x = None
            return x
        else:
            return x
    #
    if keep_type == 'str':
        try:
            x = str(x)
        except ValueError:
            print('remove_nontype(): couldnt convert to', keep_type)
            x = None
        return x



def remove_urls(raw_text, remove_urls):
    """
    given raw_text, remove all puncutation and special chars
    :param raw_text:
    :return:
    """
    # remove brackets, split into list of urls
    if type(remove_urls) is str:
        remove_urls = re.sub('[\\[\\]]', '', remove_urls).split(',')
        for url in remove_urls:
            raw_text = re.sub(url, '', raw_text)
    # remove not alphanumeric chars
    return clean_text(raw_text)


def clean_text(raw_text):
    """
    given raw_text, remove all puncutation and special chars
    :param raw_text:
    :return:
    """
    # remove not alphanumeric chars
    if type(raw_text) is str:
        clean_text = re.sub('[^A-Za-z0-9 ]+', '', raw_text)
    else:
        clean_text = None
    return clean_text


def clean_tweets(tweets):
    """
    :param tweets: dataframe of tweets with twitter columns
    :return: dataframe of cleaned tweets with standard columns
    """
    output_cols = ['id', 'date', 'time', 'datetime', 'stream', 'type',
                   'user_id', 'user_handle', 'user_name', 'place',
                   'city', 'state', 'centroid_x', 'centroid_y',
                   'raw_text', 'clean_text', 'sensitive', 'likes', 'reposts']

    rename_cols = {'id':'id', 'user_id':'user_id', 'screen_name':'user_handle', 'name':'user_name',
                   'text':'raw_text', 'possibly_sensitive':'sensitive', 'place_name':'place',
                   'favorite_count':'likes', 'retweet_count':'reposts'}

    # some columns don't need processing and can just be renamed
    tweets = tweets.rename(columns=rename_cols)

    # denote the stream and type of text
    tweets['stream'] = 'twitter'
    tweets['type'] = 'tweet'


    # dates, times, datetime
    tweets['datetime'] = tweets['created_at'].apply(parse_date, time_or_date='datetime')
    tweets['date'] = tweets['created_at'].apply(parse_date, time_or_date='date')
    tweets['time'] = tweets['created_at'].apply(parse_date, time_or_date='time')

    # location, get place centroid coords where possible
    place_ids = list(set(tweets['place_id'].values))
    place_ids = [i for i in place_ids if type(i) is not float]
    # USES OAUTH
    places = get_place_centroids(place_ids)

    # lookup the x and y coordinates for all available places
    def lookup_place(place_id, x_or_y):
        if type(place_id) is float:
            return None
        if x_or_y == 'x':
            return places[place_id][0]
        elif x_or_y == 'y':
            return places[place_id][1]
        else:
            return places[place_id]

    tweets['centroid_x'] = tweets['place_id'].apply(lookup_place, x_or_y='x')
    tweets['centroid_y'] = tweets['place_id'].apply(lookup_place, x_or_y='y')
    # todo: fix this
    tweets['city'] = tweets['state']
    tweets['state'] = None

    # make sure all numerics are numeric
    num_cols = ['centroid_x', 'centroid_y', 'reposts', 'likes']
    for num_col in num_cols:
        tweets[num_col] = tweets[num_col].apply(remove_nontype, keep_type='numeric')


    # make sure all strings are strings
    str_cols = ['id', 'user_id', 'user_handle', 'user_name']
    for str_col in str_cols:
        tweets[str_col] = tweets[str_col].apply(remove_nontype, keep_type='str')

    # finally, clean text
    tweets['clean_text'] = tweets.apply(lambda row: remove_urls(row['raw_text'], row['urls']), axis=1)
    print(tweets[output_cols].dtypes)
    return tweets[output_cols]


#
# def clean_dict():
#     {'clean_text': dtype('O'),
#      'datetime': datetime64[ns, UTC + 00:00],
#
#      'id': dtype('float64'),
#      'likes': dtype('float64'),
#      'place': dtype('O'),
#      'raw_text': dtype('O'),
#
#      'reposts': dtype('float64'),
#      'sensitive': dtype('O'), 'stream': dtype('O'), 'type': dtype('O'),
#
#      'user_handle': dtype('O'),
#      'user_id': dtype('float64'),
#      'user_name': dtype('O')}



def clean_place(city, state, country):
    if type(city) is not float and type(state) is not float:
        city = city.strip()
        state = state.strip()
        return city + ', ' + state
    elif type(city) is not float and type(country) is not float:
        city = city.strip()
        country = country.strip()
        return city + ', ' + country
    elif type(city) is not float:
        return city.strip()
    elif type(state) is not float:
        return state.strip()
    elif type(country) is not float:
        return country.strip()
    else:
        return None

def combine_message(message, message2):
    if type(message) is not float and type(message2) is not float:
        return message.strip() + ', ' + message2.strip()
    elif type(message) is not float:
        return message.strip()
    elif type(message2) is not float:
        return message2.strip()
    else:
        return None


def clean_fb_posts(fb_posts):
    """
    :param tweets: dataframe of tweets with twitter columns
    :return: dataframe of cleaned tweets with standard columns
    """
    output_cols = ['id', 'date', 'time', 'datetime', 'stream', 'type',
                   'user_id', 'user_handle', 'user_name',
                   'place', 'city', 'state', 'centroid_x', 'centroid_y',
                   'raw_text', 'clean_text', 'sensitive', 'likes', 'reposts']

    # dates, times, datetime
    dt_str_format = '%Y-%m-%dT%H:%M:%S%z'
    fb_posts['datetime'] = fb_posts['created_time'].apply(parse_date, time_or_date='datetime', try_format=dt_str_format)
    fb_posts['date'] = fb_posts['created_time'].apply(parse_date, time_or_date='date', try_format=dt_str_format)
    fb_posts['time'] = fb_posts['created_time'].apply(parse_date, time_or_date='time', try_format=dt_str_format)

    # place
    fb_posts['place'] = fb_posts.apply(lambda row: clean_place(row['city'], row['state'], row['country']), axis=1)
    fb_posts['centroid_x'] = fb_posts['longitude']
    fb_posts['centroid_y'] = fb_posts['latitude']

    # likes and reposts
    fb_posts['reposts'] = fb_posts['shares']

    # user stuff
    fb_posts['user_handle'] = fb_posts['user_name']

    # make sure all numerics are numeric
    num_cols = ['centroid_x', 'centroid_y', 'reposts', 'likes']
    for num_col in num_cols:
        fb_posts[num_col] = fb_posts[num_col].apply(remove_nontype, keep_type='numeric')

    # finally, clean text
    fb_posts['raw_text'] = fb_posts.apply(lambda row: combine_message(row['message'], row['description']), axis=1)
    fb_posts['clean_text'] = fb_posts['raw_text'].apply(clean_text)

    fb_posts['sensitive'] = 'False'


    # make sure all strings are strings
    str_cols = ['id', 'user_id', 'user_handle', 'user_name']
    for str_col in str_cols:
        fb_posts[str_col] = fb_posts[str_col].apply(remove_nontype, keep_type='str')

    print(fb_posts[output_cols].dtypes)
    return fb_posts[output_cols]



def get_social_media():
    tweets = clean_tweets(get_tweets())
    fb = clean_fb_posts(get_fb_posts())
    social_media = pd.concat([tweets, fb])
    return social_media



# if __name__ == '__main__':
#     # tweets = get_tweets()
#     # cleaned_tweets = clean_tweets(tweets)
