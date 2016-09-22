import operator
def computeScore1(feature_vectors):
	#feature_vectors - [length_score_vec[i], title_similarity_vec[i], position_score_vec[i], lead_score_vector[i]]
	score_vector = {}
	for i in range(feature_vectors.shape[0]):
		score = 0.4*feature_vectors[i][0]+ 0.3*feature_vectors[i][1]+0.2*feature_vectors[i][2]+0.1*feature_vectors[i][3]
		score_vector[i] = score
	print "score_vector  :   " , score_vector
	return score_vector

def computeScore(feature_vectors, clusSentIndices):
	score_dictionary={}
	for i in clusSentIndices.keys():
		sentence_indices = clusSentIndices[i]
		score_dic = {}
		for j in sentence_indices:
			score = 0.4*feature_vectors[j][0]+ 0.3*feature_vectors[j][1]+0.2*feature_vectors[j][2]+0.1*feature_vectors[j][3]
			score_dic[j] = score

		sorted_dic = sorted(score_dic.items(), key=operator.itemgetter(1))
		score_dictionary[i] = sorted_dic

	#print score_dictionary
	return score_dictionary
	

def generateSummary(clusSentIndices, feature_vectors,clusSentList, summary_length=6):
	#will generate extractive summary here.....
	#feature_vectors is a 2d array
	#clusSentList is list of sentences to be clustered and from which summary has to be generated
	#clusSentIndices is a dictionary mapping the cluster label and the indices of sentence which are part of it

	score_dictionary = computeScore(feature_vectors, clusSentIndices)
	#for i in clusSentIndices.keys():

	if len(clusSentList) < summary_length:
		summary_length = len(clusSentList)

	i = 0
	num_clusters = len(score_dictionary.keys())
	reached = [0 for j in range(num_clusters)]
	keys = score_dictionary.keys()

	summary = ""
	summi = []
	'''
	for j in range(summary_length):
		try : 
			index = score_dictionary[keys[i]][reached[i]][0]
			summi.append(index)
			summary += clusSentList[index]
			reached[i]+=1
			i+=1
			if(i==num_clusters):
				i=0
		except:
			i+=1
			if(i==num_clusters):
				i=0
	'''
	j=0
	while(j<summary_length):
		try : 
			index = score_dictionary[keys[i]][reached[i]][0]
			summi.append(index)
			summary += clusSentList[index]
			summary += " "
			reached[i]+=1
			i+=1
			if(i==num_clusters):
				i=0
			j+=1
		except:
			i+=1
			if(i==num_clusters):
				i=0

	#print summi
	#print summary
	return summary