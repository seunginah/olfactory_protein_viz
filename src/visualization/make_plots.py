import sys
import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "src"))

THIS_DIR = "/Users/mm40108/projects/datadays17/olfactory_protein_viz/src/visualization"
# THIS_DIR = (os.path.dirname(os.path.realpath(__file__)))

def plot_expanding_rows(imgs, ncol=5):
    """

    :param imgs:
    :param ncol:
    :return:
    """
    # plot all the images into a figure with 10 columns and expanding rows
    fig = plt.figure()
    rowct = 1
    colct = 1
    for image_file, img in imgs.items():
        ax = fig.add_subplot(rowct, ncol, colct)
        ax.imshow(img)
        ax.set_aspect('equal')
        if colct < ncol:
            colct += 1
        else:
            rowct += 1
            colct = 1
    return fig


def plot_channels(img, fig, red=0, green=1, blue=2, start_subplot=1):
    red = 0
    green = 1
    blue = 2
    channels = [red, green, blue]

    # plot each channel using nearest neighbs interpolation
    for c in channels:
        ax = fig.add_subplot(start_subplot, 3, c + 1)
        img_c = np.zeros_like(img)
        img_c[:, :, c] = img[:, :, c]
        ax.imshow(img_c, interpolation='Nearest')
    return fig


def vis_vader(X, y, pos=1, neg=0, neutral=None, title="VADER sentiment vs actual sentiment"):
    """ given data X and labels y, visualize acuity of the sentiment neuron

    Args:
        X - n x 1 ndarry containing sentiment value
        y - n x 1 ndarray of labels
        pos - indicate the value for positive label
        neg - indicate the value for negative label
        sentiment_unit - idx corresponding to sentiment unit of the encoder
    """
    plt.hist(X[y==neg], bins=25, alpha=0.5, label='neg')
    plt.hist(X[y==pos], bins=25, alpha=0.5, label='pos')
    if neutral is not None:
        plt.hist(X[y == neutral], bins=25, alpha=0.5, label='neutral')
    plt.legend()

    plt.xlabel('Value given by VADER')
    plt.ylabel('Number of analyzed comments')
    plt.title(title)

    return plt



def vis_sentiment(X, y, pos=1, neg=0, neutral=None, sentiment_unit=2388, \
                                                         title="Sentiment unit vs actual sentiment"):
    """ given data X and labels y, visualize acuity of the sentiment neuron

    Args:
        X - n x 4096 ndarray, where n is number of rows in data
        y - n x 1 ndarray of labels
        pos - indicate the value for positive label
        neg - indicate the value for negative label
        sentiment_unit - idx corresponding to sentiment unit of the encoder
    """
    sentiment_unit = X[:, sentiment_unit]
    plt.hist(sentiment_unit[y==neg], bins=25, alpha=0.5, label='neg')
    plt.hist(sentiment_unit[y==pos], bins=25, alpha=0.5, label='pos')
    if neutral is not None:
        plt.hist(sentiment_unit[y == neutral], bins=25, alpha=0.5, label='neutral')
    plt.legend()

    plt.xlabel('Value of sentiment neuron')
    plt.ylabel('Number of analyzed comments')
    plt.title(title)

    return plt


def print_examples(comments, sentiment_values, sentiment_labels,
                   neutral=False, n=20):
    """ print the top n positive, neutral, and negative labels """
    df = pd.DataFrame({'text': comments, 'score': sentiment_values, 'label': sentiment_labels})
    top_neg = df.sort_values('score')[1:n]
    top_pos = df.sort_values('score', ascending=False)[1:n]
    if neutral:
        top_neutral = df[abs(0-df.score) < 0.01].sort_values('score')[1:n]
        top = {'positive': top_pos, 'negative': top_neg, 'neutral': top_neutral}
    else:
        top = {'positive': top_pos, 'negative': top_neg}
    for k, df in top.items():
        print('\n\ntop ', n, ' ', k, ' values')
        print(df)
    return top
