import docClus2
import json
import numpy as np
import random
import feature_functions
import extSummary
from sklearn import svm
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict 
from scipy.spatial.distance import euclidean

titles_dict = {}
contents_dict = {}

def readCorpus(file_name):
	json_data = open(file_name)
	root_node = json.load(json_data)
	json_data.close()
	#print root_node["root"][0]["title"]
	global titles_dict
	global contents_dict
	articles = root_node["root"]
	for article in articles:
		titles_dict[article["id"]] = article["title"]
		contents_dict[article["id"]] = article["content"]

#print contents_dict.keys()

#to split into sentence, append to list and then apply clustering...
#working fine for jst one basic cluster
from nltk.tokenize import sent_tokenize

#creates a list of all sentences from all documents that belong to same cluster... currently hard-coded for first cluster at second level.
def clusteredSentenceGen(clusterings) :
	sentences = []
	position_score_vec = []
	title_similarity_vec= []
	lead_score_vector = []
	indices = clusterings
	#print indices
	for index in indices:
		#print titles_dict[index]
		text_content = contents_dict[index]
		#print type(text_content)
		#print "\n ***************************\n"
		sent_tokenize_list = sent_tokenize(text_content)
		#print len(sent_tokenize_list)
		cosVec = feature_functions.title_similarity_score(titles_dict[index], sent_tokenize_list)
		title_similarity_vec += cosVec
		sentences = sentences+(sent_tokenize_list)
		pos_score_vec = feature_functions.position_score(sent_tokenize_list)
		position_score_vec += pos_score_vec
		lead_vec = feature_functions.first_sentence_score(sent_tokenize_list)
		lead_score_vector += lead_vec

	length_score_vec = feature_functions.length_score(sentences)
	#print "*****************\n\n"
	#print "position_score_vec  :  ", position_score_vec
	#print title_similarity_vec
	#print "lead score vector   :   ", lead_score_vector
	#print len(length_score_vec), len(position_score_vec), len(title_similarity_vec), len(lead_score_vector)
	#print "*************************************************************\n\n"
	
	feature_vectors = []
	for i in range(len(sentences)):
		feature_vectors.append([length_score_vec[i], title_similarity_vec[i], position_score_vec[i], lead_score_vector[i]])

	return (sentences, feature_vectors)

def clusSentenceKmeans (clusSentList, n_clusters=5):
	sent_labels = docClus2.kmeansCluster_docs(clusSentList, n_clusters)
	#print "-----------------------------------------------****************---------------------------------------"
	#print "kmLabels : "
	#print sent_labels

	sent_clustered = defaultdict(list)
	for i in range(len(sent_labels)):
		sent_clustered[sent_labels[i]].append(clusSentList[i])

	''' need to add sentence and cluster scoring logic / algorithm
		currently selecting first sentence according to order from each cluster
	'''

	for key in sent_clustered.keys():
		#print key
		print sent_clustered[key][0]

def generateClass_B(class_A, rows, cols):
	class_B = []
	'''
	#Vectors with all values 0 :
	for i in range(rows):
		eachRow = []
		for j in range(cols):
			eachRow.append(0)
		class_B.append(eachRow)
	#print class_B
	class_B = np.asarray(class_B)'''

	#generate class B by computing mid-points of the points:
	for i in range(rows):
		midpoint = []
		if i < rows-1:
			point1 = class_A[i]
			point2 = class_A[i+1]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)
	for i in range(rows):
		midpoint = []
		if i < rows-2:
			point1 = class_A[i]
			point2 = class_A[i+2]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)
	for i in range(rows):
		midpoint = []
		if i < rows-3:
			point1 = class_A[i]
			point2 = class_A[i+3]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)

	for i in range(rows):
		midpoint = []
		if i < rows-4:
			point1 = class_A[i]
			point2 = class_A[i+4]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)

	for i in range(rows):
		midpoint = []
		if i < rows-5:
			point1 = class_A[i]
			point2 = class_A[i+5]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)

	for i in range(rows):
		midpoint = []
		if i < rows-6:
			point1 = class_A[i]
			point2 = class_A[i+6]
		else:
			point1 = class_A[i]
			point2 = class_A[0]
		for j in range(cols):
			mid = (point1[j]+point2[j])/2
			midpoint.append(mid)
		class_B.append(midpoint)

	#class_B = np.asarray(class_B)

	indices = random.sample(range(1, len(class_B)), rows)
	class_B_ret = []
	for i in indices:
		class_B_ret.append(class_B[i])

	class_B_ret = np.asarray(class_B_ret)
	return class_B_ret

def computeEuclidean(sent_tfidf, R, R_indices):
	minimum = euclidean(sent_tfidf, R[0])
	minimum_index = R_indices[0]
	#print minimum, minimum_index
	for i in range(len(R)):
		dist = euclidean(sent_tfidf, R[i])
		if(dist<minimum):
			minimum = dist
			minimum_index = R_indices[i]

		#print minimum, minimum_index
	return minimum_index

def computeCosine(sent_tfidf, R, R_indices):
	maximum = cosine_similarity(sent_tfidf, R[0])
	max_index = R_indices[0]
	#print minimum, minimum_index
	for i in range(len(R)):
		dist = cosine_similarity(sent_tfidf, R[i])
		if(dist>maximum):
			maximum = dist
			max_index = R_indices[i]

		#print minimum, minimum_index
	return max_index


def svClustering(clusSentList, feature_vectors):
	preprocessed_list = docClus2.docPreprocess(clusSentList) #preprocess sentences
	tfs_tuple = docClus2.tfidfCompute(preprocessed_list)#compute vector model of each sentence (forms data space)
	#print "/////////////////////////////////////////////////////////////////////"

	class_A = tfs_tuple[0].toarray()
	#print type(class_A)
	#print class_A.shape[0], class_A.shape[1]
	rows = class_A.shape[0]
	cols = class_A.shape[1]
	toBeClustered = class_A
	#print class_A

	class_B = generateClass_B(class_A, rows, cols)
	
	#print class_B.shape[0], class_B.shape[1]
	#print class_B

	#print type(class_B)
	R = []
	C_0 = 8 #need to experiment
	sigma = 0.1 #need to experiment
	iters = 1

	#step-2
	for niter in range(iters) :
		input_X = np.concatenate ([class_A,class_B])
		input_labels = []
		label0 = [0 for i in range(class_A.shape[0])]
		label1 = [1 for i in range(class_B.shape[0])]
		input_labels = input_labels + label0 + label1
		#print input_labels
		#print input_X.shape[0], len(input_labels)

		clf = svm.SVC(C=C_0, gamma=sigma, kernel='rbf' )
		clf.fit(input_X,input_labels)
		#print rows, len(clf.support_)
		#print clf.support_  #gives indices of bound support vectors for each class
		#print clf.n_support_ #gives no of bound support vectors for each class
		#print clf.dual_coef_
		#print len(clf.dual_coef_[0])

		lag_coeff = clf.dual_coef_[0]
		lag_coeff_A = lag_coeff[:class_A.shape[0]]
		#print len(lag_coeff_A)

		#count = 0 ... counts # of non-bound support vectors in cluster A
		#2A
		non_bound_sv_A = []
		non_bound_sv_A_indices = []
		R_indices = []
		for i in range(class_A.shape[0]):
			try :
				if(lag_coeff_A[i] < C_0):
					#count+=1
					non_bound_sv_A.append(input_X[clf.support_[i]])
					non_bound_sv_A_indices.append(i)
			except:
				pass

		Cl_A = non_bound_sv_A
		if len(Cl_A) > len(R):
			R = Cl_A 
			R_indices = non_bound_sv_A_indices

		#print count, len(non_bound_sv_A)

		#2B
		no_support_A = clf.n_support_[0]
		index_support_A = [] #indices of bound support vectors of class A
		SV_A = []
		for i in range(no_support_A):
			index_support_A.append(clf.support_[i])
			SV_A.append(input_X[clf.support_[i]])

		#print index_support_A
		#print len(SV_A)

		class_B = SV_A
		index_non_bound_A = []
		for i in range(class_A.shape[0]):
			if i not in index_support_A:
				index_non_bound_A.append(i)

		#print index_non_bound_A
		Cl_A = []
		for i in index_non_bound_A:
			Cl_A.append(input_X[i])

		#print Cl_A

		class_A = Cl_A

		class_A = np.asarray(class_A)
		class_B = np.asarray(class_B)

		rows = class_A.shape[0]
		#cols = class_A.shape[1]
		#print rows
		#print "iter : ", niter
		#print "********************\n\n\n"


	#Step : 3
	#print R_indices
	#print toBeClustered
	rows = toBeClustered.shape[0]
	#print rows
	unclustered = []
	unclustered_indices = []
	for i in range(rows):
		if i not in R_indices:
			unclustered.append(toBeClustered[i])
			unclustered_indices.append(i)

	#print rows, len(R_indices), len(unclustered)
	clusteringSentences = {}
	clusSentIndices = {}
	for i in R_indices:
		clusteringSentences[i] = []
		clusSentIndices[i] = []
		clusteringSentences[i].append(clusSentList[i])
		clusSentIndices[i].append(i)

	#print "unclustered_indices : ", unclustered_indices
	#print clusteringSentences
	#print len(unclustered)
	#print "################################\n\n"

	if(len(R)>0):
		for i in range(len(unclustered_indices)):
			index = unclustered_indices[i]
			cluster_label = computeCosine(unclustered[i], R, R_indices)
			clusteringSentences[cluster_label].append(clusSentList[index])
			clusSentIndices[cluster_label].append(index)
	else :
		clusteringSentences[0] = []
		clusSentIndices[0] = []
		for i in unclustered_indices:
			clusteringSentences[0].append(clusSentList[i])  
			clusSentIndices[0].append(i)

	#print clusteringSentences
	#clusSentence indices start from zero and even unclustered_indices
	#print clusSentIndices
	summary = extSummary.generateSummary(clusSentIndices, feature_vectors,clusSentList)
	return summary


#clusterings - dict(layer1 clustering) of dict(layer2 clustering) of list(index of documents that fall under the layer 2 cluster)
def svc (data, clusterings):
	#clusterings = docClus2.docClus("corpus.json")
	#print clusterings
	readCorpus(data)

	'''
	(clusSentList, feature_vectors) = clusteredSentenceGen(clusterings[0][0])
	#print clusSentList
	#print type(clusSentList[0])
	#clusSentenceKmeans(clusSentList)
	feature_vectors = np.asarray(feature_vectors)
	#print "feature vectors   :    ", feature_vectors[0][0]

	svClustering(clusSentList, feature_vectors)
	'''
	num = 0
	flag = False
	summaries = []
	keys1 = clusterings.keys()
	for i in keys1:
		keys2 = clusterings[i].keys()
		for j in keys2:
			num+=1
			cluster = clusterings[i][j]
			if len(cluster)>6:
				num-=1
				continue
			(clusSentList, feature_vectors) = clusteredSentenceGen(cluster)
			#print clusSentList
			#print type(clusSentList[0])
			#clusSentenceKmeans(clusSentList)
			feature_vectors = np.asarray(feature_vectors)
			#print "feature vectors   :    ", feature_vectors[0][0]

			summaryi = svClustering(clusSentList, feature_vectors)
			summaries.append(summaryi)

			#print "$$$$$$$$$$$$$$$$$$************************************************$$$$$$$$$$$$$$$$"

			if num==40 :
				flag = True
				break

		if flag :
			break

	return summaries