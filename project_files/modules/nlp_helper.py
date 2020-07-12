# adding some initial comments to test git
# one more change here. Messing with git commits on local machine.

import requests
import json
import pandas as pd
import numpy as np
import time
import random
import re
import os

#NLTK

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.collocations import *
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


# stop words
stop_words = stopwords.words('english')

# bi gram and tri gram method assignment
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


def ngram_helper(tokens, bi_or_tri, freq_filter, junk_words):
    """
    Overview: Returns a sorted list of bi or tri gram scored results

    Params: 
    tokens --> word tokens
    bi_or_tri --> 'bi' or 'tri': string
    freq_filter --> frequency requirement: int
    junk_words --> list of words to filter out: list

    Returns:
    sorted list of bi or tri grams w/ score

    """
    if bi_or_tri == 'tri':
    
    
        # NLTK Bigram / Trigram finders and filters
        finder = TrigramCollocationFinder.from_words(tokens)
        # Omits junk words
        finder.apply_word_filter(lambda x: x in junk_words)
        # Frquency requirement
        finder.apply_freq_filter(freq_filter)

        scored = finder.score_ngrams(trigram_measures.raw_freq)


        return sorted(trigram for trigram, score in scored)
    
    elif bi_or_tri == 'bi':
        
        
        # NLTK Bigram / Trigram finders and filters
        finder = BigramCollocationFinder.from_words(tokens)
        # Omits junk words
        finder.apply_word_filter(lambda x: x in junk_words)
        # Frquency requirement
        finder.apply_freq_filter(freq_filter)

        scored = finder.score_ngrams(bigram_measures.raw_freq)


        return sorted(bigram for bigram, score in scored)
    
    else:
        
        return 'Error'



# initial tokenization and clean-up
def tokenize(text):
    """
    Takes a sentence, returns a cleaned and tokenized list

    Params:
    text --> string

    Returns:
    Tokenized list --> list

    """

    # tokenize 
    tokens = nltk.word_tokenize(text)
    # regex non-words
    tokens = [re.sub(pattern = r'[^\w]', repl = "", string = word ) for word in tokens]
    # remove empty strings from regex ops
    tokens = [i for i in tokens if i] 
    # remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    # lowercase
    tokens = [word.lower() for word in tokens]


    return tokens




def get_pos_tags(tokens, pos):
    """
    POS tags a tokenized list

    Params:
    tokens --> list
    pos --> part of speech: 'adjective', 'verb', 'noun'

    Returns:
    list of tokens within specified pos

    """

    # tag the words
    words = nltk.pos_tag(tokens)

    # index 0: word
    # index 1: pos tag

    noun_abv = ['NN', 'NNS', 'NNP', 'NNPS']
    verb_abv = ['VB','VBD', 'VBG', 'VBP', 'VBZ']
    adjective_abv = ['JJ', 'JJR', 'JJS']

    if pos == 'adjective':
        return [i[0] for i in words if i[1] in adjective_abv]
    elif pos == 'noun':
        return [i[0] for i in words if i[1] in noun_abv]
    elif pos == 'verb':
        return [i[0] for i in words if i[1] in verb_abv]
    else:
        return 'ERROR: pos arg not acceptable, try: adjective, noun, verb'


def vectorized_df(tokens):
    """
    Overview:
    Vectorizes and builds df for given tokens
    
    Params:
    tokens --> list of tokens
    
    Returns:
    df
    
    """
    # Design the Vocabulary
    count_vectorizer = CountVectorizer()
    # Create the Bag-of-Words Model
    wordbag = count_vectorizer.fit_transform(all_nouns)
    # Build dataframe
    feature_names = count_vectorizer.get_feature_names()
    word_df = pd.DataFrame(wordbag.toarray(), columns = feature_names)
    
    return word_df


def get_top_words(n_words, word_list):
    """
    Overview: 
    returns top n-number words by count
    
    Params:
    n_words --> # of words to return
    wordlist --> list of tokens
    
    Returns:
    List of n-words
    
    """

    # nested arrays with unique words and their counts
    unique = np.unique(all_nouns, return_counts = True)

    # words array
    words = unique[0]
    # counts array
    counts = unique[1]

    # find top n-number of counts
    sorted_counts = sorted(counts)[-1*n_words:]

    # retrieve index for sorted_counts
    index_ret = [np.where(counts == item)[0][0] for item in sorted_counts]

    # words by index
    return list(words[index_ret])



def get_top_grams(gram_list, n_grams):
    """
    Returns list of top bi/tri-grams by frequency
    
    Params:
    gram_list --> list of bi/tri-grams (nested)
    n_grams --> number of grams to return from top
    
    """
    
    # list to array
    grams = np.array(gram_list)

    # unique array elements
    unique = np.unique(grams, return_counts = True, axis = 0)

    # grams
    grams = unique[0]
    # counts
    counts = unique[1]

    sorted_counts = sorted(counts)[-1*n_grams:]

    indices = [np.argwhere(counts == count)[0][0] for count in sorted_counts]
    
    # list of grams by index
    gram_list = [list(gram) for gram in grams[indices]]
    
    # de-dupe
    ret_array = np.unique(gram_list, axis=0)
    
    # format back to list
    ret_list = [list(gram) for gram in ret_array]

    
    return ret_list


    

def topwords_by_percentile(percentile, word_list):
    """
    Takes a percentile and list of words, computes the words in that percentile for occurrence
    
    Params:
    
    Percentile: e.g. .5, .75, .10
    
    word_list: list of words to count
    
    """

    unique, counts = np.unique(all_nouns,return_counts=True)

    max_index = np.argmax(counts)
    max_word, max_count = unique[max_index], counts[max_index]

    index = np.where(counts >= percentile*max_count)
    return list(unique[index])




def keywords_by_branch(branch, df):
    """
    gets list of keywords within a specified federal branch
    
    params:
    
    df to search
    branch to filter by
    
    """
    soldf = df

    branch_df = soldf[soldf['Branch'] == f'{branch}']

    branch_words = [words for words in branch_df['Keywords']]

    branch_all = []
    for words in branch_words:
        branch_all.extend(words)

    return branch_all


def topwords_by_branch(branch, df, n_perc):
    """
    returns a list of top words in the nth percentile by frequency, by branch
    """
    soldf = df
    
    branch_words = keywords_by_branch(f'{branch}', soldf)

    # words in the top nth percentile of branch 
    freqs = keywords_frequencies(branch_words, n_perc)

    top_words = keywords_frequencies(branch_words, n_perc)[1]
    words_dict = keywords_frequencies(branch_words, n_perc)[0]
    # from np.array to list
    words_list = [word for word in top_words]
    
    return words_dict, words_list


def gram_frequencies(grams, n_perc):
    
        """
        Takes grams, returns top nth percentile frequencies
        
        Params:
        
        grams -- list
        n_perc -- words in nth percentile
        
        Returns
        dictionary and top_grams list

        """

        # Type cast to list for np.unique compatibility
        gram_lists = [list(gram) for gram in grams]
        
        keyw_arr = np.array(gram_lists)
        keyw_unique = np.unique(keyw_arr, return_counts = True)

        # get indexes
        words = keyw_unique[0]
        counts = keyw_unique[1]

        
        top_index = np.argmax(counts)
        # words[top_in] --> ['size', 'weight']
        top_count = counts[top_index]
        # returns indices for top counts
        top_indices = np.where(counts >= float(n_perc * top_count))
        # returns top words from top_indices
        top_grams = words[top_indices]
        
        # dictionary 
        d = {tuple(word) : count for word, count in zip(words, counts)}

        
        return d, top_grams


def keywords_frequencies(keywords, n_perc):
    
        """
        Takes keywords, returns top nth percentile frequencies
        
        Params:
        
        keywords -- list
        n_perc -- words in nth percentile
        
        Returns
        dictionary and top_words list

        """

        keyw_arr = np.array(keywords)
        keyw_unique = np.unique(keyw_arr, return_counts = True)

        # get indexes
        words = keyw_unique[0]
        counts = keyw_unique[1]
        
        # build dict
        d = {word : count for word, count in zip(words, counts)}
        
        top_index = np.argmax(counts)
        # words[top_in] --> ['size', 'weight']
        top_count = counts[top_index]
        # returns indices for top counts
        top_indices = np.where(counts >= float(n_perc * top_count))
        # returns top words from top_indices
        top_words = words[top_indices]
        
        return d, top_words


    
def get_topbranchkeys(n_perc, my_dict, agency):
    """
    Get top key, value pairs within nth percentile of max value of dictionary.
    Use dictionary response from topwords_by_branch or topwords_by_frequency as my_dict arg.
    
    """
    # get max key
    my_dict = my_dict[agency]
    
    maxkey = max(my_dict, key = my_dict.get)
    maxvalue = my_dict[maxkey]
    
    top_pairs = {}
    
    for key, value in my_dict.items(): 
        if value >= n_perc * maxvalue: 
            top_pairs[key] = value
        
    return top_pairs 

def get_topkeys(n_perc, my_dict):
    """
    Get top key, value pairs within nth percentile of max value of dictionary.
    Use dictionary response from topwords_by_branch or topwords_by_frequency as my_dict arg.
    
    """
    # get max key
    maxkey = max(my_dict, key = my_dict.get)
    maxvalue = my_dict[maxkey]
    
    top_pairs = {}
    
    for key, value in my_dict.items(): 
        if value >= n_perc * maxvalue: 
            top_pairs[key] = value
        
    return top_pairs 

def get_singular_root(check_word, new_word, keywords):
    """
    replaces string with a new string if == check_word
    
    """

    if check_word in keywords:
        newlist=[x for x in keywords if x != check_word]
        newlist.append(new_word)
        return newlist
    else:
        return keywords
