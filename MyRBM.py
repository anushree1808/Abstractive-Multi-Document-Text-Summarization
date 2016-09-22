from nltk import sent_tokenize, word_tokenize, pos_tag
import nltk
import numpy
import re
import json
import math
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import RBMachine
import os
import gzip, cPickle
import theano
from theano.tensor.shared_randomstreams import RandomStreams
import theano.tensor as T
import sys
class FeatureFunctions(object):
    def __init__(self):
        self.wmap = {}
        '''self.flist = [] 
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist.append(v)       
        '''
        return

    def set_wmap(self, wmap): # given a list of words sets wmap
        self.wmap=wmap
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0   

    def evaluate(self, title, sentence_index, article_index, sentence_len, wcount, article_count, total_words, sentences):
        '''for f in self.flist:
            feats.append(f(self, title, sentence))
        '''

        feats = [self.f_titleSimilarity(title, sentences[sentence_index]), self.f_positionFeature(sentence_index, sentence_len), self.f_tfIdf(sentence_index, article_index, wcount, article_count, total_words, sentences), self.f_conceptFeature(sentences), self.f_lengthFeature(sentences[sentence_index])]
        return feats
    
    # feature functions
    def f_titleSimilarity(self, title, sentence):
    	ilist = list(set(title) & set(sentence))
    	return float(len(ilist)) / len(title)

    def f_positionFeature(self, postion, sentence_len):
    	position_score = (postion +1 ) / float(sentence_len)
    	return position_score
    	     
    def f_tfIdf(self, sentence_index, article_index, wcount, article_count, total_words, sentences):
    	di = 0
    	for word in sentences[sentence_index]:
  			n = float(wcount[article_index][word]) / total_words
  			count = 0
  			for c in range(article_count):
  				if wcount[article_index][word] > 0 :
  					count += 1	
  			m = math.log(float(article_count) / count)		
  			if m < 1:
  				m = 1
  			tfidf = n * m
  			di += tfidf
    	return di

    def f_conceptFeature(self, sentence):
    	return 0      

    def f_lengthFeature(self, sentence):
    	alpha = len(sentence) - self.avg_length_var / float(self.standard_deviation)
    	length_feature = (1 - math.exp(-alpha)) / (1 + math.exp(-alpha))
    	return length_feature

    def special_score(self, sentence):
    	pass
    def avg_special_score(self, sentences):
    	pass
    def standard_deviation_special_score(self, sentences):
    	pass
    def avg_length(self, sentences):
    	self.avg_length_var = 0
    	for sentence in sentences:
    		self.avg_length_var += len(sentence)   		
    	self.avg_length_var = float(self.avg_length_var) / len(sentences)	

    def standard_deviation_length(self, sentences):
    	self.standard_deviation = 0
    	for sentence in sentences:			
        	self.standard_deviation = math.pow(len(sentence)-self.avg_length_var, 2)
        #print self.standard_deviation, len(sentences)
        try :
        	self.standard_deviation = math.sqrt(self.standard_deviation / len(sentences) - 1) 	
        except ValueError:
        	self.standard_deviation = 0.1	
   	    
def Preprocessing(data, stop, myStemmer, article_ids):
	newsData = []
	count = 0
	words_map = {}
	word_count = []
	index = 0
	all_sentences = []
	for news in data:
		if news["id"] not in article_ids:
			continue
		article = {}
		article["title"] = word_tokenize(news["title"])
		content = news["content"]
		article["pubdate"] = news['pubdate']
		sentences = sent_tokenize(content)
		word_list = []
		item = {}
		total_words = 0
		for sentence in sentences:
			all_sentences.append(sentence)
			# Word tekenization
			words = word_tokenize(sentence)
			total_words += len(words)
			word_list.append(words)
			#POS tagging
			taggedwords = pos_tag(words)
			#print taggedwords
			#Stop Word Removal
			important_words = []
			for word in words:
				item[word] = item.setdefault(word, 0) + 1
				if word not in stop:
					important_words.append(word)
			#Stemming
			root_words = []
			for i in range(len(important_words)) : 
				root_words.append(myStemmer.stem(important_words[i]))
			#print important_words , root_words	
			words_map[count] = {'words': root_words, 'pos_tags': taggedwords, "sentence" : sentence}
			count += 1
		word_count.append(item) 	
		article["sentences"] = word_list	
		article["sentence_len"] = len(sentences)	
		article["total_words"] = total_words
		newsData.append(article)
	return (newsData, words_map, word_count, all_sentences)

def buildMatrix(newsData, wmap, wcount, all_sentences, func_obj):
	article_count = len(newsData)
	sentence_matrix = []
	class_label = []
	func_obj.avg_length(all_sentences)
	func_obj.standard_deviation_length(all_sentences)
	for article_index in range(len(newsData)):
		article = newsData[article_index]
		for i in range(article["sentence_len"]):
			sentence_matrix.append(func_obj.evaluate(article["title"], i, article_index, article["sentence_len"], wcount, article_count, article["total_words"], article["sentences"]))
			class_label.append(0)
	return sentence_matrix, class_label

def generateSummary(data, article_ids):
	stop = stopwords.words('english')
	myStemmer = PorterStemmer()
	(newsData, wmap, wcount, all_sentences) = Preprocessing(data, stop, myStemmer, article_ids)
	func_obj = FeatureFunctions()
	func_obj.set_wmap(wmap)
	# construct the sentence_matrix
	sentence_matrix, class_label = buildMatrix(newsData, wmap, wcount, all_sentences, func_obj)
	#print " Feature Matrix : "
	#for f in sentence_matrix:
	#	print f
	sentence_matrix = numpy.array(sentence_matrix, dtype=float)
	train_set = sentence_matrix, class_label
	val_set = sentence_matrix, class_label
	test_set = sentence_matrix, class_label
	dataset = [train_set, val_set, test_set]
	pickle_file = gzip.open('sentence_matrix.pkl.gz', 'wb')
	cPickle.dump(dataset, pickle_file, protocol=2)
	pickle_file.close()
	result = RBMachine.test_rbm('sentence_matrix.pkl.gz')
	print result
	#print "\n Optimal feature vector set : "
	#print result
	tr_a_1 = 0.7
	tr_a_2 = 0.5
	tr_b_1 = 0.7
	tr_b_2 = 0.5
	tr_c_1 = 0.7
	tr_c_2 = 0.5
	num = 0
	#print "\n \nSummary : "
	extracted_sentences = []
	for i in range(len(result)):
		#if num > 6 :
		#	break	
		try:
			if result[i][0] > tr_a_1 :
				sys.stdout.write(wmap[i]["sentence"])
				num += 1
				extracted_sentences.append(wmap[i]["sentence"])
			elif result[i][1] > tr_b_1 : 
				sys.stdout.write(wmap[i]["sentence"])
				num += 1
				extracted_sentences.append(wmap[i]["sentence"])
			elif result[i][1] > tr_c_1 :
				sys.stdout.write(wmap[i]["sentence"])
				num += 1		
				extracted_sentences.append(wmap[i]["sentence"])
			elif result[i][0] >	tr_a_2 and result[i][1] > tr_b_2:
				sys.stdout.write(wmap[i]["sentence"])
				num += 1	
				extracted_sentences.append(wmap[i]["sentence"])
		except :
			pass		
			
	#print ("\n")			
	#print "Length of input data : ", len(wmap)		
	#print "Summary Length : ", num
	return (" ").join(extracted_sentences)

def generateSummaryForClusters (data, clusterings):
	num = 0
	count = 0
	flag = False
	summaries = []
	keys1 = clusterings.keys()
	print keys1
	for i in keys1:
		keys2 = clusterings[i].keys()
		print keys2
		for j in keys2:
			#if count > 20 :
			#	return summaries
			num+=1
			article_ids = clusterings[i][j]
			try:
				summaries.append(generateSummary(data, article_ids))
				count += 1
			except :
				continue
	return summaries		


def summarize(json_file, clusterings):
	data = json.loads(open(json_file).read())['root']
	summaries = generateSummaryForClusters(data, clusterings)
	return summaries