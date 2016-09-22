import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

#sentence length
def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = stem_tokens(tokens,stemmer)
	return stems

tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')

#feature funct not used now
def compute_avg_length(clusSentList):
	total = len(clusSentList)
	sumWords = 0
	for sentence in clusSentList:
		sumWords += len(nltk.word_tokenize(sentence))

	avg = float(sumWords) / total
	return avg

#feature function used to compute length score
def length_score(clusSentList):
	#avg = compute_avg_length(clusSentList)
	lengths = [len(nltk.word_tokenize(i)) for i in clusSentList]
	sumWords = sum(lengths)
	avg = float(sumWords)/len(clusSentList)
	#return avg
	for i in range(len(lengths)):
		if(lengths[i]<7):
			lengths[i] = 0
	len_score = [float(lengths[i])/avg for i in range(len(clusSentList))]
	return len_score

#feature function used to compute position score of the sentence in document 
def position_score(sentence_tokenize_list):
	total = len(sentence_tokenize_list)
	position_score = [float(i)/total for i in range(total)]
	return position_score

#feature function used to compute the document-title similarity score
def title_similarity_score(title, sentence_tokenize_list):
	
	cosine_vector = []
	for sentence in sentence_tokenize_list:
		tfs = tfidf.fit_transform((title,sentence))
		#print tfidf.get_feature_names()
		#print tfs
		cos_theta = cosine_similarity(tfs[0:1], tfs[1:])[0][0]
		#print cos_theta
		cosine_vector.append(cos_theta)
	#print cosine_vector
	return cosine_vector

#feature function used to compute the similarity of first sentence with rest of the sentences score in the document
def first_sentence_score(sentence_tokenize_list):
	if(len(sentence_tokenize_list) > 0):
		first_sentence = sentence_tokenize_list[0]
		lead_sent_vector = []
		for sentence in sentence_tokenize_list:
			tfs = tfidf.fit_transform((first_sentence,sentence))
			#print tfidf.get_feature_names()
			#print tfs
			cos_theta = cosine_similarity(tfs[0:1], tfs[1:])[0][0]
			#print cos_theta
			lead_sent_vector.append(cos_theta)
		#print cosine_vector
		#print "len of lead_sent_vector  :   ", lead_sent_vector
	else:
		lead_sent_vector = []
	return lead_sent_vector


#print length_score(["I love you", "I hate you a lot", "what is happening here"])
#print position_score(["I love you", "I hate you a lot", "what is happening here"])
#title_similarity_score("india wins", ["India has won the match against australia in semis", "australia lose their match", "India won and Australia lose match", "Australia win againt India in a dream run"])
#first_sentence_score(["India has won the match against australia in semis", "australia lose their match", "India won and Australia lose match", "Australia win againt India in a dream run"])