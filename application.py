from flask import Flask, jsonify

application = Flask(__name__)

from newsapi import NewsApiClient
import json

#api key: 4f21ac7443de4fb2b3e79c98d712f78f
newsapi = NewsApiClient(api_key='ad78a7bd081a48a4b779ea9990699212')


f = open('stopwords_en.txt')
stopwords = f.readlines()
f.close()
stopwordsList = []

for item in stopwords:
	stopwordsList.append(item.strip())


#print(stopwordsList)

def removeStopwords(wordlist, stopwords):
	return [w for w in wordlist if w not in stopwords]

@application.route('/') 
def homepage():
	return application.send_static_file("index.html")

@application.route('/hello')
def get_index():
	return("hello world")

@application.route('/headline')
def get_headline():
	top_headlines = newsapi.get_top_headlines(language='en',country='us')
	return top_headlines

@application.route('/CNN_headline')
def get_CNN():
	CNN = newsapi.get_top_headlines(sources='CNN',language='en')
	return CNN


@application.route('/FOX_headline')
def get_FOX():
	FOX = newsapi.get_top_headlines(sources='fox-news',language='en')
	return FOX

@application.route('/word_cloud')
def word_cloud():
	top_headlines = newsapi.get_top_headlines(page_size = 100, language='en',country='us')
	
	frequency = []
	words = "";
	for item in top_headlines['articles']:
		words += (item['title'].lower()+" ")

	wordslist = words.split();
	wordslist = removeStopwords(wordslist, stopwordsList)

	wordslist = ["".join(list(filter(str.isalnum, word))) for word in wordslist]
	
	for w in wordslist:
		frequency.append(wordslist.count(w));

	wordfreq = dict(list(zip(wordslist, frequency)))
	
	return wordfreq

@application.route('/Source/<category>')
def get_source(category):
	if(category == "all"):
		source = newsapi.get_sources()
	else:
		source = newsapi.get_sources(category = category)
	return source

@application.route('/Search/<keyword>/<source>/<start>/<to>')
def search_news(keyword, source, start, to):
	print("haha")
	try: 
		if(source == "all"):
			everything = newsapi.get_everything(q=keyword, language='en', from_param=start, to=to, page_size = 100)
		else:
			everything = newsapi.get_everything(q=keyword, sources=source, language='en', from_param=start, to=to, page_size = 100)
		return everything
	except Exception as error:
		print(error.get_message())
		message = {"message":error.get_message()}
		return message


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

















	