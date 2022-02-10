from app import app
from app import server as ml
from flask import render_template, json, request, jsonify
import tweepy as tw
import csv
import pandas as pd
from werkzeug.utils import secure_filename
import os
from nltk.util import ngrams
import matplotlib.pyplot as plt

load = ml.LoadData()
collect = ml.Data_Scrape()
prepro = ml.Preprocessing()
net = ml.Network()
tm = ml.Timeseries()

RAW_DATA_LOC = 'app/static/file/collected/'
model_path = 'app/all_indo_man_tag_corpus_model.crf.tagger'
filter_path = RAW_DATA_LOC + 'Filter_tweet.csv'
ALLOWED_EXTENSIONS = {'csv', '','file'}

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def stopwords():
    if request.method == "POST":
        stopwords_df = load.loadData(filter_path)
        locHStopwords = load.savedata(RAW_DATA_LOC, stopwords_df['text'], "tweet_text.txt")
    return locHStopwords

def token():
    locHStopwords = stopwords()
    add_stopwords = request.form.get("stopwords")
    tweet_token = prepro.openandtoken(locHStopwords)
    tweet_clean_stopwords = prepro.stopwords_cleaner(tweet_token, add_stopwords)

    return tweet_clean_stopwords


@app.route("/twitter_data", methods=["GET", "POST"])
def gets_data():
    if request.method == "POST":
       search_words = request.form.get("search")
       date_since = request.form.get("since")
       date_until = request.form.get("until")
       numb_of_tweet = int(request.form.get("numb"))
       print(search_words)
       
       tweets = collect.get_data(search_words, date_since, date_until, numb_of_tweet)
       tweets_flat = prepro.flatten_tweets(tweets)
       ds_tweets = pd.DataFrame(tweets_flat)
       ds_tweets.drop(['entities','metadata','user','retweeted_status','source'], axis=1, inplace=True)
       print(ds_tweets)
       lochScrape = load.savedata(RAW_DATA_LOC, ds_tweets, "tweet2.csv")
       hasil = {
           "hScrape": {lochScrape} 
           }
       res = json.dumps(hasil, default=set_default), 200
       return res
    return render_template("index.html")

@app.route("/filter_out", methods=["GET", "POST"])
def filter_data():
    if request.method == "POST":
        filter_words = []
        filter = request.form.get("filter-out")
        filter_words = [item for item in filter.split()]
        
        path = RAW_DATA_LOC + 'tweet.csv'
        filter_df = load.loadData(path)
        
        new_filter_df = filter_df[~filter_df.retweeted_status_screen_name.isin(filter_words)]
        print(new_filter_df)

    
        locHFilter = load.savedata(RAW_DATA_LOC, new_filter_df, "Filter_tweet.csv")
        hasil = {
           "hFilter": {locHFilter}
           }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("filter.html")


@app.route("/exist_twitter", methods=["GET", "POST"])
def exist_twitter():
    if request.method == "POST":

        file = request.files["testDataset"]
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(RAW_DATA_LOC, filename))
        else:
            return jsonify(message='error'), 500

        loc_test = os.path.join(RAW_DATA_LOC, filename)
        exist_df = load.loadData(loc_test)

        hasil = {"prediction": {loc_test}
                 }

        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")


@app.route("/graph", methods=["GET", "POST"])
def graph():
    
    word1 = "#GarongKorupsiBerjamaah"
    word2 = "BPJS"

    ds_tweets = pd.read_csv('C:/Users/ASUS/nlp_analysis/app/static/file/collected/tweet.csv')
    ds_tweets = ds_tweets.sort_values(['created_at'], ascending=[True])
    ds_tweets['created_at'] = pd.to_datetime(ds_tweets['created_at'])
    ds_tweets = ds_tweets.set_index('created_at')

    timeseries_image = tm.get_timeseries_plot(ds_tweets, word1, word2)

    hasil = {
           "timeseries" : {timeseries_image}
           }
    res = json.dumps(hasil, default=set_default), 200
    return res



@app.route("/timeseries", methods=["GET", "POST"])
def timeseries_plot():
    if request.method == "POST":
        # word1 = request.form.get("word1")
        # word2 = request.form.get("word2")

        word1 = "#GarongKorupsiBerjamaah"
        word2 = "BPJS"

        ds_tweets = pd.read_csv('C:/Users/ASUS/nlp_analysis/app/static/file/collected/tweet.csv')
        ds_tweets = ds_tweets.sort_values(['created_at'], ascending=[True])
        ds_tweets['created_at'] = pd.to_datetime(ds_tweets['created_at'])
        ds_tweets = ds_tweets.set_index('created_at')
        

        
        timeseries_image = tm.get_timeseries_plot(ds_tweets, word1, word2)

        hasil = {
           "timeseries" : {timeseries_image}
           }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/stopwords", methods=["GET", "POST"])
def stopwords_custom():
    
    if request.method == "POST":
        
        unigram_threshold = 200
        bigram_threshold = 150
        trigram_threshold = 170
        verb_threshold = 30
        adjective_threshold = 10
        adverb_threshold = 2
        noun_threshold = 200
        
        locHStopwords = stopwords()
        
        tweet_clean_stopwords = token()

        wordcloud_image = prepro.wordcloud(tweet_clean_stopwords)
        unigrams_image = prepro.unigrams(tweet_clean_stopwords, unigram_threshold)
        bigrams_image = prepro.bigrams(tweet_clean_stopwords, bigram_threshold)
        trigrams_image = prepro.trigrams(tweet_clean_stopwords, trigram_threshold)

        
        result = prepro.pos_tagger(tweet_clean_stopwords, model_path)
        verbCounter = prepro.verb_counter(result, verb_threshold)
        adjectiveCounter = prepro.adjective_counter(result, adjective_threshold)
        adverbCounter = prepro.adverb_counter(result, adverb_threshold)
        nounCounter = prepro.noun_counter(result, noun_threshold)

        path = RAW_DATA_LOC + 'tweet.csv'
        ds_tweets = load.loadData(path)
        G_rt = net.RT_nodes_edges(ds_tweets)
        G_reply = net.reply_nodes_edges(ds_tweets)
        network_image = net.viz_network(G_rt)
        
        top_rt, top_reply = net.indegree_centrality(G_reply, G_rt)
        lochRT_indegree = load.savedata(RAW_DATA_LOC, top_rt, "RT_indegree.csv")
        lochReply_indegree = load.savedata(RAW_DATA_LOC, top_reply, "reply_indegree.csv")

        betweeness_rt, betweeness_reply = net.betweeness_centrality(G_rt, G_reply)
        lochRT_betweeness = load.savedata(RAW_DATA_LOC, betweeness_rt, "RT_betweeness.csv")
        lochReply_betweeness = load.savedata(RAW_DATA_LOC, betweeness_reply, "reply_betweeness.csv")

        ratio_df = net.ratio(G_rt, G_reply)
        lochRatio = load.savedata(RAW_DATA_LOC, ratio_df, "ratio.csv") 

        hasil = {
           "hStopwords": {locHStopwords},
           "hRT_indegree": {lochRT_indegree},
            "hreply_indegree": {lochReply_indegree},
            "hRT_betweeness": {lochRT_betweeness},
            "hReply_betweeness": {lochReply_betweeness},
            "hRatio": {lochRatio},  
           "wordcloud": {wordcloud_image},
           "network": {network_image},
           "unigram": {unigrams_image},
           "bigram": {bigrams_image},
           "trigram": {trigrams_image},
           "verb": {verbCounter},
           "adjective": {adjectiveCounter},
           "adverb": {adverbCounter},
           "noun": {nounCounter}
           }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hUnigram", methods=["GET", "POST"])
def unigram():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        unigram_threshold = int(request.form.get("unigram_threshold"))
        unigrams_image = prepro.unigrams(tweet_clean_stopwords, unigram_threshold)

        hasil = {
            "unigram": {unigrams_image}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hBigram", methods=["GET", "POST"])
def bigram():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        bigram_threshold = int(request.form.get("bigram_threshold"))
        bigrams_image = prepro.bigrams(tweet_clean_stopwords, bigram_threshold)

        hasil = {
            "bigram": {bigrams_image}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hTrigram", methods=["GET", "POST"])
def trigram():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        trigram_threshold = int(request.form.get("trigram_threshold"))
        trigrams_image = prepro.trigrams(tweet_clean_stopwords, trigram_threshold)

        hasil = {
            "trigram": {trigrams_image}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")


@app.route("/hVerb", methods=["GET", "POST"])
def verb():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        result = prepro.pos_tagger(tweet_clean_stopwords, model_path)
        verb_threshold = int(request.form.get("verb_threshold"))
        verbCounter = prepro.verb_counter(result, verb_threshold)

        hasil = {
            "verb": {verbCounter}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hAdjective", methods=["GET", "POST"])
def adjective():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        result = prepro.pos_tagger(tweet_clean_stopwords, model_path)
        adjective_threshold = int(request.form.get("adjective_threshold"))
        adjectiveCounter = prepro.adjective_counter(result, adjective_threshold)

        hasil = {
            "adjective": {adjectiveCounter}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hAdverb", methods=["GET", "POST"])
def adverb():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        result = prepro.pos_tagger(tweet_clean_stopwords, model_path)
        adverb_threshold = int(request.form.get("adverb_threshold"))
        adverbCounter = prepro.adverb_counter(result, adverb_threshold)

        hasil = {
            "adverb": {adverbCounter}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")

@app.route("/hNoun", methods=["GET", "POST"])
def noun():
    if request.method == "POST":
        tweet_clean_stopwords = token()
        result = prepro.pos_tagger(tweet_clean_stopwords, model_path)
        noun_threshold = int(request.form.get("noun_threshold"))
        nounCounter = prepro.noun_counter(result, noun_threshold)

        hasil = {
            "noun": {nounCounter}
            }
        res = json.dumps(hasil, default=set_default), 200
        return res
    return render_template("index.html")


@app.route("/hScraping", methods=["GET"])
def tampil():
    data = []
    
    with open(RAW_DATA_LOC + 'tweet2.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile)
        print(data_csv )
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hpResult", methods=["GET"])
def tampilResult():
    data = []

    with open(RAW_DATA_LOC + 'tweet.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    print(type(data))
    return jsonify(data)

@app.route("/hFilter", methods=["GET"])
def tampilFilter():
    data = []

    with open(RAW_DATA_LOC + 'Filter_tweet.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hRT_indegree", methods=["GET"])
def tampilRT_indgeree():
    data = []

    with open(RAW_DATA_LOC + 'RT_indegree.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hReply_indegree", methods=["GET"])
def tampilReply_indgeree():
    data = []

    with open(RAW_DATA_LOC + 'reply_indegree.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hRT_betweeness", methods=["GET"])
def tampilRT_betweeness():
    data = []

    with open(RAW_DATA_LOC + 'RT_betweeness.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hReply_betweeness", methods=["GET"])
def tampilReply_betweeness():
    data = []

    with open(RAW_DATA_LOC + 'reply_betweeness.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)

@app.route("/hRatio", methods=["GET"])
def tampilRatio():
    data = []

    with open(RAW_DATA_LOC + 'ratio.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)