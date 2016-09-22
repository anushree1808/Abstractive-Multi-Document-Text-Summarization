import docClus2
import MyLexicalChainer, MyRBM
import svcClustering1
import keyphraseExtraction
import json
from collections import defaultdict
import absSummary
import sys
import math
from nltk import word_tokenize
out_file = open("summary.json", "w")
if len(sys.argv) >=2 :
	if sys.argv[1] == "deeplearning" : 
		option = 1
	elif sys.argv[1] == "svc":
		option = 2
	else:
		option = 3
else :
	option = 2
print "Performing Doc Clustering"
clusterings = docClus2.docClus("DataCorpus3.json")
print "Clustering done"
if option == 1 :
	print "Performing Deep Learning"
	summaries = MyRBM.summarize("DataCorpus3.json", clusterings)
	i=1
	summ = {}
	summ["root"] = []
	for summary in summaries :
		keys = []
		#sentences = sent_tokenize(summary)
		#words = word_tokenize(sentences[0])
		#print words
		#words[5] = "..." 
		print "summary  :  ", summary.encode('utf-8')
		print "-----------\n\n"
		summ["root"].append({"keys" : keys, "summary":summary})
		i+=1
	json.dump(summ,out_file, indent=4) 
	out_file.close()
	absSummary.genSummary()
elif option == 2:
	print "Performing SVC"
	summaries = svcClustering1.svc("DataCorpus3.json", clusterings)
	#print summaries
	i=1
	summ = {}
	summ["root"] = []
	for summary in summaries :
		keys = keyphraseExtraction.extract_key(summary)
		print keys
		print "summary  :  ", summary.encode('utf-8')
		print "-----------\n\n"
		summ["root"].append({"key" : keys, "summary":summary})
		i+=1

	json.dump(summ,out_file, indent=4) 
	out_file.close()
	absSummary.genSummary()
else :
	print "Performing Lexical Chains"
	summaries = MyLexicalChainer.summarize("DataCorpus3.json", clusterings)
	i=1
	summ = {}
	summ["root"] = []
	for summary in summaries :
		keys = keyphraseExtraction.extract_key(summary)
		print keys
		#words = word_tokenize(summary)
		#print words
		#words[5] = "..."
		#print words[:6]
		print "summary  :  ", summary.encode('utf-8')
		print "-----------\n\n"
		summ["root"].append({"key" : keys, "summary":summary})
		i+=1
	json.dump(summ,out_file, indent=4) 
	out_file.close()
	absSummary.genSummary()