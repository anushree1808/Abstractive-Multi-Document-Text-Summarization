from nltk.corpus import wordnet as wn
from nltk import sent_tokenize, word_tokenize, pos_tag
import json
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from lexicalchain import LexGraph, GalleyMcKeownChainer



class LexicalChain:

	def __init__(self):
		"""
			Initiliase the class variables here
		"""
		self.np_list = []
		return 

	def GetCandidateWords(self,sentences):
		"""
			Simple nouns are selected as candiate words.

		"""
		i = 0
		for sentence in sentences:
			for word in sentence:
				if word[1] == "NN":
					self.np_list.append([word[0], sentence])
			i += 1	
		#print self.np_list
	def Preprocessing(self,data):
		for news in data:
			sentences = sent_tokenize(news["content"])
			tagged_sentences = []
			for sentence in sentences:
				try:
					words = word_tokenize(sentence)
					tagged_words = pos_tag(words)
					tagged_sentences.append(tagged_words)
				except NameError:
					continue	
				except UnicodeEncodeError:
					continue
		return tagged_sentences

	def buildLexicalChain(self):
		for word in self.np_list:
			print wn.synsets(word[0], pos='n')

	def Processing(self, input):
		input = input.replace("-\n","")
		input = sent_tokenize(input)
		input = [[pos_tag(word_tokenize(sent)) for sent in input]]
		mc = GalleyMcKeownChainer(data=input)
		chains = mc.computeChains()
		return chains


def preProcessing(data, article_ids):
	content = ""
	for news in data:
		if news["id"] not in article_ids:
			continue
		return news["content"]	
		content += news["content"].encode('utf-8')
	return content	

def getSentenceId(lexical_chains):
	sentence_ids = set()
	for chain in lexical_chains:
		metachain = chain[0]
		lex_nodes_list = metachain.getAdjacentNodes()
		i = 0
		for lex_node_tuple  in lex_nodes_list:
			if i == 0 and len(sentence_ids) <= 5:
				sentence_ids.update(lex_node_tuple[0].getPos())				
			i+=1 	  	
	return sentence_ids	

def extractSentence(data, sentence_ids):
	data = data.replace("-\n","")
	data = sent_tokenize(data)
	id_list = list(sentence_ids)
	extracted_sentences = []
	for id in id_list:
		extracted_sentences.append(data[id-1])
	return extracted_sentences

def generateSummary(data, article_ids):
	data = preProcessing(data, article_ids)
	#data = json.loads(open('DataCorpus.json').read())['root'][10]["content"]
	l = LexicalChain()
	lexical_chains = l.Processing(data)
	sentence_ids = getSentenceId(lexical_chains)
	print sentence_ids	
	content	= (" ").join(extractSentence(data, sentence_ids))
	return content

def generateSummaryForClusters (data, clusterings):
	num = 0
	flag = False
	summaries = []
	keys1 = clusterings.keys()
	for i in keys1:
		keys2 = clusterings[i].keys()
		for j in keys2:
			num+=1
			article_ids = clusterings[i][j]
			summary = generateSummary(data, article_ids)
			summaries.append(summary)
			if num >= 20:
				flag = True
				break
		if flag:
			break	
	return summaries


def summarize(json_file, clusterings):
	data = json.loads(open(json_file).read())['root']
	summaries = generateSummaryForClusters(data, clusterings)
	#print type(summaries[0])
	return summaries


'''		
if __name__ == "__main__":

	json_file = r"DataCorpus2.json"
	data = json.loads(open(json_file).read())['root'][30]["content"]
	#print data
	print "\n Lexical chains generated : \n" 
	l = LexicalChain()
	lexical_chains = l.Processing(data)
	sentence_ids = getSentenceId(lexical_chains)	
	content	= extractSentence(data, sentence_ids)
	print content
'''