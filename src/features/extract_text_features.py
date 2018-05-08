import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))
THIS_DIR = os.path.dirname(os.path.realpath(__file__))



def clean_sentence(doc):
    if doc is None:
        return None
    """ returns a cleaned document (sentence) """
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


if __name__ == '__main__':
