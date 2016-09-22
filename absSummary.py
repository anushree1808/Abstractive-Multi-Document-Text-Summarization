import json
import nltk
import re

def genSummary():
	out_file = open("summary.json", "r")
	root_node = json.load(out_file)
	roots = root_node["root"]
	mode_root_node = {}
	mode_root_node["root"] = []
	print "\n\n\n\n\n\n\n\n"
	print "From abs summary :- \n\n"
	notwords = ["also", "hence","furthermore","moreover","therefore", "so", "however", "but", "further", "u", "&", "13", "#", ";"]
	#roots=[{"summary" : "\"However, this is not going to happen\". So, he is good. So, that is not good so good. So, no. "}]
	for root in roots:
		summary = root["summary"]
		#summary = "Therefore, I am going to say that he also will not speak"
		#print summary
		#print "\n"
		#1.check if they are in the beginning of sentence. 2.clean the sentences(like comma and all in wrong places, 3.pronoun to noun conversion
		
		summ = {}
		summ["key"] = root["key"]

		sentences = nltk.sent_tokenize(summary)
		#print sentences
		finalSentences = []
		marks = []
		for sentence in sentences:
			words = nltk.word_tokenize(sentence)
			#print words
			finalSummary = ""
			for i in range(len(words)):
				if words[i].lower() in notwords:
					marks.append(words[i])
				elif words[i].lower() == "n't":
					words[i] = "not"
				elif words[i].lower() == "'s":
					words[i] = "is"
			for mark in marks:
				words.remove(mark)
			marks = []
			finalSentence = (" ").join(words).rstrip()
			#print finalSentence.decode('utf-8')
			finalSentences.append(finalSentence)
		
		finalSummary = (" ").join(finalSentences)
		#print finalSummary
		#finalSummary = re.sub(("(\. )[,!?;]+ "), ". ", finalSummary)
		#finalSummary = re.sub(' +[.,?!]+','', finalSummary)
		#finalSummary = re.sub(("&#13"),"", finalSummary)
		finalSummary = re.sub(("(\. )+[,!?]+ "), ". ", finalSummary)
		#finalSummary = re.sub(' +[.,?!]+','', finalSummary)
		finalSummary = re.sub(("&#13"),"", finalSummary)

		#print finalSummary

		if(finalSummary[0:2] in [" ,", " !", " ?"]):
			finalSummary = finalSummary[4:]
		elif (finalSummary[0:4] in ["\" ," , "\" ?" , "\" !", "`` ," , "`` ?" , "`` !"]):
			finalSummary1 = '\"'
			finalSummary1 += finalSummary[5:]
			finalSummary = finalSummary1
		'''elif(finalSummary[0:4] in ["'' ,", "'' ?", "'' !"]):
			finalSummary1 = "\""
			finalSummary1+= finalSummary[5:] 
			finalSummary = finalSummary1'''

		'''k = 0
		while k< len(finalSummary):
			flag = k
			j = k
			while(finalSummary[k] in [" ", ",", ":"]):
				j+=1
			if (flag != j):
				finalSummary[k+1]
			k+=1'''
		#print finalSummary.encode('utf-8')
		#print "******************************************************************************" * 2
		summ["summary"] = finalSummary
		mode_root_node["root"].append(summ)

	#print finalSummary
	#print mode_root_node
	out_file = open("modified_summary.json", "w")
	json.dump(mode_root_node, out_file, indent=4)
	out_file.close()
	print "\n\n\n\n\n\n\n\n"

#genSummary()