from flask import Flask, request, render_template, redirect, url_for
import random
import requests
import ipdb
import pickle
import re
import pandas as pd
import numpy as np

# Initialize your app and load your pickled models.
#================================================
app = Flask(__name__)

def return_tweet():
    '''return the text content tweet that we had
    indexed and also deletes it from the database'''

    data = pd.read_pickle('data/tweetdata.pkl')
    index = np.random.randint(1,len(data))

    '''needs to be fixed for items that aren't contained in axis'''

    target_data = data.iloc[index]
    data = data.drop(index)

    '''drop the data before sending it back'''

    data.to_pickle('data/tweetdata.pkl')
    return target_data

def filter_text(string):
    '''removes any user mentions'''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",string).split())
# Homepage with form on it.
#================================================
@app.route('/')
def index():
    return render_template('read_more.html')


@app.route('/first_tweet',methods=['POST','GET'])
def next():
    for i in range(3):
        if request.method =='POST':
            tweet = return_tweet()
            text = tweet['text']
            content = {'text':filter_text(text)}
            return render_template('user_answer2.html', content=content)
        if request.method =='GET':
            return str(0)

@app.route('/display_tweet', methods=['POST','GET'])
def display_tweet():

    '''ajax requests need fixing'''

    if request.method =='GET':
        tweet = return_tweet()
        text = tweet['text']
        content = {'text': filter_text(text)}
        return render_template('user_answer2.html', content=content)
    if request.method =='POST':
        return str(0)

@app.route('/stop',methods=['POST','GET'])
def stop():

    '''thanks user and gives them option to read more'''

    return render_template('stop.html')

@app.route('/read_more',methods=['POST','GET'])
def read_more():

    '''this page should have a lot of d3 vis on suicide statistics'''

    return render_template('text_about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
