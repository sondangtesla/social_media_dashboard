import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk import FreqDist
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter
nltk.download('gutenberg')
nltk.download('genesis')
nltk.download('inaugural')
nltk.download('nps_chat')
nltk.download('webtext')
nltk.download('treebank')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.collocations import *
from nltk.util import ngrams
import pycrfsuite
from nltk.book import *
from matplotlib.pyplot import figure
from nltk.tag import CRFTagger

#library for scraping
import os
import tweepy as tw
import pandas as pd
import datetime as dtm
from pandas import json_normalize
import numpy as np

#library for network visualization
import networkx as nx
import math
import seaborn as sns

GRAFIK_LOC = 'C:/Users/ASUS/nlp_analysis/app/static/img/grafik/'

class LoadData:
    def loadData(self, loc):
        data = pd.read_csv(loc)
        return data

    def savedata(self, loc, data, file_name):
        data.to_csv(loc+file_name, index=False)
        return loc+file_name

class Data_Scrape:
    def get_data(self, search_words, date_since, date_until, numb_of_tweet):
        """Collecting data from twitter

        Parameters 
        -----------
        search_words:
                this is an input from user to search like hashtag or keywords
        date_since:
                the specified time limit for the data collected from twitter
        numb_of_tweet:
                total data the system must collect
        
                       
        Returns
        -----------
        pandas dataframe
        
        """
        consumer_key = 'vezezGSjD1a8ayKiD2f66tRfD'
        consumer_secret = 'OpCrhVSsGY2sqlko4w6bcj07Wheq9wApLRyvcYIvMTjzAnMPbv'
        access_token = '1475282070339391489-rKunMuAUHDba2RyL5lEoDFYEGc453Z'
        access_token_secret = 'BV4bF17lOeeBSflQtYBJwpYeMP1mmL3qPGOeNAjhjqM9y'

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        # Collect tweets
        tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="id",
              since=date_since, 
              until=date_until).items(numb_of_tweet)
        
        # Iterate and print tweets
        tweets_copy = []
        for tweet in tweets:
            tweets_copy.append(tweet)
        
        
        tweet_json = []
        for tweet in tweets_copy:
            tweet_json.append(tweet._json)
        
        return tweet_json

class Preprocessing:
    figure(figsize=(20, 20), dpi=80)#default plot size 

    def openandtoken(self, file_path):
        """Open and tokenizes txt file

        Parameters 
        -----------
        file_path:
                This is file path of the txt document
        Returns
        -----------
        nltk.Text /List 
            This is an nltk.Text type which are a list of tokenized words that can be 
            used for further analysis. Please refer to nltk documentation for further
            information https://www.nltk.org/_modules/nltk/text.html
        
        """
        f = open(file_path, "rb")
        raw = f.read().decode(errors='replace')
        tokens = word_tokenize(raw) #tokenize
        text = nltk.Text(tokens)
        return text
    
    def stopwords_cleaner(self, text, add_stopwords):
        """Use this to clean text. Please define list of stopwords first. 
        You can use nltk.corpus.stopwords.words('language of interest') or refer to NLTK for list.

        Parameters 
        -----------
        text : nltk.Text.text / list
                This is a list of tokenized words
        Returns
        -----------
        cleaned tokens : A list that has removed tokens that are in the list of stopwords and non alphabetical words

        """
        ## add words to stopwords
        stopwords = nltk.corpus.stopwords.words('indonesian')
        new_stopwords = ['aku','yg','aja','nya','si','dgn','d',
                        'gk','tdk','sih','yg','tp','ya','om',
                        'habib','gak','orang','ga','org','dg',
                        'lg','bang','semoga','rt','jg','https',
                        'hny','krn','pd','sbg','bnyk','dudung',
                        'abdurachman','ksad','jenderal','tni',
                        'angkatan','darat','pt','kepala','staf',
                        'jendral','jd','persero','badan','usaha',
                        'milik','negara','perusahaan','erickthohir',
                        'bumn','utama']
        new_stopwords2 = [item for item in add_stopwords.split()]
        final_stopwords = new_stopwords + new_stopwords2
        stopwords.extend(final_stopwords)
        
        """
        converts all the words to lower case and before checking if 
        they are in list of stopwords and also removes non alphabetical tokens
        """
        cleaned_tokens = [w for w in text if w.lower() not in stopwords and w.isalpha()] 
        return cleaned_tokens
    
   
    def wordcloud(self, cleaned_tokens):
        """Produces a word cloud from our list of tokenized words

        Parameters
        -----------
        cleaned_tokens : List of tokenized words that has stopwords removed.

        Returns
        ----------
        wordcloud : A vizualization of words that have their size corresponding to the word frequency

        """
        word_cloud_dict = Counter(cleaned_tokens) # get counter of each token

        # creates word cloud. Size of word correponds to frequency of token
        wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_cloud_dict) 
        
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "word_cloud" + self.t + '.png'
        wordcloud.to_file(GRAFIK_LOC+self.nm)
        
        return self.nm
    
    
    def unigrams(self, cleaned_text, unigram_threshold):
        """Creates a bargraph based on frequency of individual tokens 

        Parameters
        -----------
        cleaned_tokens : List of tokenized words that has stopwords removed.

        Returns
        ----------
        Sorted plot of unigrams based on frequency
        """
        
        unigrams_count = Counter(cleaned_text) #gets frequency of tokens
        min_threshold = unigram_threshold #removes words below this threshold. Defaults to 100 
        bar = {x: count for x, count in unigrams_count.items() if count >= min_threshold} #removes words below this threshold
        word_bar = dict(sorted(bar.items(), key = lambda x: x[1], reverse = True))  #sorts the bar based on frequency
        plt.figure(figsize=(25,8))
        plt.bar(word_bar.keys(), word_bar.values())
        plt.xticks(fontsize=15, color='black')
        plt.yticks(fontsize=15, color='black')

        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "unigrams" + self.t + '.png'
        plt.savefig(GRAFIK_LOC+self.nm)

        return self.nm

    def bigrams(self, cleaned_text, bigram_threshold):
        """Creates a bargraph based on frequency of two tokens occuring together

        Parameters
        -----------
        cleaned_tokens : List of tokenized words that has stopwords removed.
        threshold : excludes words below this threshold. 

        Returns
        ----------
        Sorted plot of bigrams based on frequency
        """
        bigrams = ngrams(cleaned_text,2) #select number of n grams
        bigrams_count = Counter(bigrams) # count number of 4
        bigrams_count = {x: count for x, count in bigrams_count.items() if count >= bigram_threshold} # get count => 4
        bigrams_bar = dict(sorted(bigrams_count.items(), key = lambda x: x[1], reverse = True))    
        names = list(bigrams_bar.keys())   #make this sorted later
        actual_name = []

        for n in names:
            actual_name.append(n[0] + '_' +n[1]) #append two words together. Example red wine = red_wine

        values = list(bigrams_bar.values())
        plt.figure(figsize=(35,10))
        plt.bar(range(len(bigrams_bar)), values, tick_label = actual_name)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "bigrams" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm

    def trigrams(self, cleaned_text, trigram_threshold):
        """Creates a bargraph based on frequency of three tokens occuring together

        Parameters
        -----------
        cleaned_tokens : List of tokenized words that has stopwords removed.

        Returns
        ----------
        Sorted plot of trigrams based on frequency
        """
        trigrams = ngrams(cleaned_text, 3) #select number of n grams
        trigrams_count = Counter(trigrams) # count number of 
        trigrams_count = {x: count for x, count in trigrams_count.items() if count >= trigram_threshold} # get count => 4
        trigrams_bar = dict(sorted(trigrams_count.items(), key = lambda x: x[1], reverse = True))    
        names = list(trigrams_bar.keys())   #make this sorted later
        actual_name = []

        for n in names:
            actual_name.append(n[0] + '_' + n[1] + '_' + n[2])   #append three words together. Example big red dog = big_red_dog

        values = list(trigrams_bar.values())
        plt.figure(figsize = (44,8))
        plt.bar(range(len(trigrams_bar)), values, tick_label = actual_name)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "trigrams" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm
    
     

    def pos_tagger(self, cleaned_tokens, model_path):
        """Tags words based on their Part of Speech (POS)
        Please install package sklearn-pycrfsuite and import pycrfsuite before usage

        Parameters
        -----------
        cleaned_tokens : List of tokenized words that has stopwords removed.
        model_path : Path of model that has been trained to detect which POS a token belongs to


        Returns
        ----------
        result : Words tagged with the POS
        """
        
        ct = CRFTagger()
        ct.set_model_file(model_path)
        result = ct.tag(cleaned_tokens)
        return result
    
    def verb_counter(self, result, verb_threshold):
        """Returns all verb in list of tokens and creates a bar graph based on their frequency

        Parameters
        -----------
        tagged_tokens : tokens that have been tagged according to their POS
        threshold : excludes words below this threshold. 

        Returns
        ----------
        result : Words tagged with the POS
        """
        verbs = []
        for w in result:
            if 'VB' in w:
                verbs.append(w[0])
        
        verb_counter = Counter(verbs)
        verb_count = {x: count for x, count in verb_counter.items() if count >= verb_threshold} # remove verb below threshold
        verb_bar = dict(sorted(verb_count.items(), key = lambda x: x[1], reverse = True))
        names = list(verb_bar.keys())  
        values = list(verb_bar.values())
        plt.figure(figsize=(40,8))
        plt.bar(range(len(verb_bar)), values, tick_label=names)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "verb_counter" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm
    
    def adjective_counter(self, result, adjective_threshold):
        """Returns all adjectives in list of tokens and creates a bar graph based on their frequency

        Parameters
        -----------
        tagged_tokens : tokens that have been tagged according to their POS
        threshold : excludes words below this threshold. 

        Returns
        ----------
        result : Words tagged with the POS
        """
        adj = []
        for a in result:
            if 'JJ' in a:
                adj.append(a[0])

        adj_counter = Counter(adj)
        adj_count = {x: count for x, count in adj_counter.items() if count >= adjective_threshold} # remove verb below threshold
        adj_bar = dict(sorted(adj_count.items(), key = lambda x: x[1], reverse = True))
        names = list(adj_bar.keys())  
        values = list(adj_bar.values())
        plt.figure(figsize=(40,20))
        plt.bar(range(len(adj_bar)), values, tick_label=names)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "adjective_counter" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm
    

    def adverb_counter(self, result, adverb_threshold):
        """Returns all adverb in list of tokens and creates a bar graph based on their frequency

        Parameters
        -----------
        tagged_tokens : tokens that have been tagged according to their POS
        threshold : excludes words below this threshold. 

        Returns
        ----------
        result : Words tagged with the POS
        """
        
        adv = []
        for av in result:
            if 'RB' in av:
                adv.append(av[0])

        adv_counter = Counter(adv)
        adv_count = {x: count for x, count in adv_counter.items() if count >= adverb_threshold} # remove verb below threshold
        adv_bar = dict(sorted(adv_count.items(), key = lambda x: x[1], reverse = True))
        names = list(adv_bar.keys())  
        values = list(adv_bar.values())
        plt.figure(figsize=(40,8))
        plt.bar(range(len(adv_bar)), values, tick_label = names)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "adverb_counter" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm
    
    def noun_counter(self, result, noun_threshold):

        """Returns all nouns in list of tokens and creates a bar graph based on their frequency

            Parameters
            -----------
            tagged_tokens : tokens that have been tagged according to their POS
            threshold : excludes words below this threshold. 

            Returns
            ----------
            result : Words tagged with the POS
        """
        noun = []
        for n in result:
            if 'NN' or 'NNP' in n:
                noun.append(n[0])

        noun_counter = Counter(noun)
        noun_count = {x: count for x, count in noun_counter.items() if count >= noun_threshold} # remove verb below threshold
        noun_bar = dict(sorted(noun_count.items(), key = lambda x: x[1], reverse = True))
        names = list( noun_bar.keys())  
        values = list(noun_bar.values())
        plt.figure(figsize=(40,8))
        plt.bar(range(len(noun_bar)), values, tick_label=names)
        plt.xticks(fontsize=20, color='black')
        plt.yticks(fontsize=20, color='black')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "noun_counter" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)

        return self.nm
    
    
    
    def flatten_tweets(self, tweets):
        """ Flattens out tweet dictionaries so relevant JSON is 
        in a top-level dictionary. """
    
        tweets_list = []
        
        # Iterate through each tweet
        for tweet_obj in tweets:
        
            ''' User info'''
            # Store the user screen name in 'user-screen_name'
            tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
            
            # Store the user location
            tweet_obj['user-location'] = tweet_obj['user']['location']
        
            ''' Text info'''
            # Check if this is a 140+ character tweet
            if 'extended_tweet' in tweet_obj:
                # Store the extended tweet text in 'extended_tweet-full_text'
                tweet_obj['extended_tweet-full_text'] = \
                                        tweet_obj['extended_tweet']['full_text']
        
            if 'retweeted_status' in tweet_obj:
                # Store the retweet user screen name in 
                # 'retweeted_status-user-screen_name'
                tweet_obj['retweeted_status_screen_name'] = \
                            tweet_obj['retweeted_status']['user']['screen_name']

                # Store the retweet text in 'retweeted_status-text'
                tweet_obj['retweeted_status-text'] = \
                                            tweet_obj['retweeted_status']['text']
        
                if 'extended_tweet' in tweet_obj['retweeted_status']:
                    # Store the extended retweet text in 
                    #'retweeted_status-extended_tweet-full_text'
                    tweet_obj['retweeted_status-extended_tweet-full_text'] = \
                    tweet_obj['retweeted_status']['extended_tweet']['full_text']
                    
            if 'quoted_status' in tweet_obj:
                # Store the retweet user screen name in 
                #'retweeted_status-user-screen_name'
                tweet_obj['quoted_status-user-screen_name'] = \
                                tweet_obj['quoted_status']['user']['screen_name']

                # Store the retweet text in 'retweeted_status-text'
                tweet_obj['quoted_status-text'] = \
                                                tweet_obj['quoted_status']['text']
        
                if 'extended_tweet' in tweet_obj['quoted_status']:
                    # Store the extended retweet text in 
                    #'retweeted_status-extended_tweet-full_text'
                    tweet_obj['quoted_status-extended_tweet-full_text'] = \
                        tweet_obj['quoted_status']['extended_tweet']['full_text']
            
            
            ''' Place info'''
            if 'place' in tweet_obj:
                # Store the country code in 'place-country_code'
                try:
                    tweet_obj['place-country'] = \
                                                tweet_obj['place']['country']
                    
                    tweet_obj['place-country_code'] = \
                                                tweet_obj['place']['country_code']
                    
                    tweet_obj['location-coordinates'] = \
                                tweet_obj['place']['bounding_box']['coordinates']
                except: pass
            
            tweets_list.append(tweet_obj)
            
        return tweets_list

class Network:
    def RT_nodes_edges(self, ds_tweets):
        G_rt = nx.from_pandas_edgelist(
        ds_tweets,
        source = 'user-screen_name',
        target = 'retweeted_status_screen_name',
        create_using = nx.DiGraph())
    
        # Print the number of nodes
        print('Nodes in RT network:', len(G_rt.nodes()))

        # Print the number of edges
        print('Edges in RT network:', len(G_rt.edges()))
        
        return G_rt

    def reply_nodes_edges(self, ds_tweets):
        G_reply = nx.from_pandas_edgelist(
                    ds_tweets,
                    source = 'user-screen_name',
                    target = 'in_reply_to_screen_name',
                    create_using = nx.DiGraph())
        
        # Print the number of nodes
        print('Nodes in reply network:', len(G_reply.nodes()))

        # Print the number of edges
        print('Edges in reply network:', len(G_reply.edges()))

        return G_reply

    def viz_network(self, G_rt):
        figure(figsize=(20, 20), dpi=80)

        # Create random layout positions
        pos = nx.spring_layout(G_rt,k=5/math.sqrt(G_rt.order()))

        pos2 = nx.spectral_layout(G_rt)
        # Create size list
        sizes = [x[1]*50 for x in G_rt.degree()]

        # Draw the network
        nx.draw_networkx(G_rt, pos=pos, 
            with_labels = True, 
            node_size = sizes,
            font_size =  6,
            width = 0.1, alpha = 0.7,
            arrowsize = 2, linewidths = 0)

        # Turn axis off and show
        plt.axis('off')
        self.t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.nm = "Network" + self.t + '.png'
        plt.savefig(GRAFIK_LOC + self.nm)
        # plt.show()

        return self.nm
    
    def indegree_centrality(self, G_rt, G_reply):
        # Generate in-degree centrality for retweets 
        column_names = ['screen_name', 'degree']
        rt_centrality = nx.in_degree_centrality(G_rt)

        # Generate in-degree centrality for replies 
        reply_centrality = nx.in_degree_centrality(G_reply)

        # Store centralities in DataFrame
        rt = pd.DataFrame(list(rt_centrality.items()), columns = column_names)
        reply = pd.DataFrame(list(reply_centrality.items()), columns = column_names)
        
        top_rt = rt.sort_values('degree', ascending = False).head()
        top_reply = reply.sort_values('degree', ascending = False).head()
        
        return top_rt, top_reply
    
    def betweeness_centrality(self, G_rt, G_reply):
        column_names = ['screen_name', 'degree']
        # Generate betweenness centrality for retweets 
        rt_centrality = nx.betweenness_centrality(G_rt)

        # Generate betweenness centrality for replies 
        reply_centrality = nx.betweenness_centrality(G_reply)

        # Store centralities in data frames
        rt = pd.DataFrame(list(rt_centrality.items()), columns = column_names)
        reply = pd.DataFrame(list(reply_centrality.items()), columns = column_names)

        
        betweeness_rt = rt.sort_values('degree', ascending = False).head()
        betweeness_reply = reply.sort_values('degree', ascending = False).head()
        
        return betweeness_rt, betweeness_reply
    
    def ratio(self, G_rt, G_reply):
        column_names = ['screen_name', 'degree']
        # Calculate in-degrees and store in DataFrame
        degree_rt = pd.DataFrame(list(G_rt.in_degree()), columns = column_names)
        degree_reply = pd.DataFrame(list(G_reply.in_degree()), columns = column_names)

        # Merge the two DataFrames on screen name
        ratio = degree_rt.merge(degree_reply, on = 'screen_name', suffixes = ('_rt', '_reply'))

        # Calculate the ratio
        ratio['ratio'] = ratio['degree_reply'] / ratio['degree_rt']

        # Exclude any tweets with less than 5 retweets
        ratio = ratio[ratio['degree_rt'] >= 5]

        # Print out first five with highest ratio
        ratio_df = ratio.sort_values('ratio', ascending = False).head()

        return ratio_df

class Timeseries:
    def check_word_in_tweet(word, data):
        """Checks if a word is in a Twitter dataset's text. 
        Checks text and extended tweet (140+ character tweets) for tweets,
        retweets and quoted tweets.
        Returns a logical pandas Series.
        """
        contains_column = data['text'].str.contains(word, case = False)
        contains_column |= data['extended_tweet-full_text'].str.contains(word, case = False)
        contains_column |= data['quoted_status-text'].str.contains(word, case = False)
        contains_column |= data['quoted_status-extended_tweet-full_text'].str.contains(word, case = False)
        contains_column |= data['retweeted_status-text'].str.contains(word, case = False)
        contains_column |= data['retweeted_status-extended_tweet-full_text'].str.contains(word, case = False)
        
        return contains_column
    
        
    
    def get_timeseries_plot(self, ds_tweets, word1, word2):
        ds_tweets[word1] = Timeseries.check_word_in_tweet(word1, ds_tweets)
        ds_tweets[word2] = Timeseries.check_word_in_tweet(word2, ds_tweets)

        mean1 = ds_tweets[word1].resample('1 min').mean()
        mean2 = ds_tweets[word2].resample('1 min').mean()
        
        sns.lineplot(data=mean1.sort_index())
        sns.lineplot(data=mean2.sort_index())
        plt.xlabel('Minute'); plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.title('Tweet mentions over time')
        plt.legend((word1, word2))
        t = dtm.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        nm = "timeseries" + t + '.png'
        plt.savefig(GRAFIK_LOC + nm)
        print(nm)
        return nm