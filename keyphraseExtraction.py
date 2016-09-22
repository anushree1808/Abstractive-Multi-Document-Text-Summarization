''''
	input - the summary as a string
	output - list of keywords
'''

import rake
import operator

# path to file containing list of stop words
stoppath = "SmartStoplist.txt"

# Initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)

def extract_key(text) :
	#text = "The index had gained 68.22 points in the previous session on Thursday.Nifty acted very range bound facing a strong resistance at 8750 level and found immediate support at 8680 level which we mentioned earlier.Nifty still holds the immediate support placed at 8680 level.Prominent losers among the 30 sensex stocks were TCS, Axis Bank, Bharti Airtel, BHEL, GAIL, HDFC, HDFC Bank, Hero MotoCorp, Infosys, M&M, Maruti Suzuki, NTPC, ONGC, SBI, Sesa Sterlite, Sun Pharma and Tata Motors.These payments amount to around Rs 26 crore, the company said in a release here.Dabur India Ltd: The Burman Family Office, the investment arm of the Burman family, promoters of fast-moving consumer group conglomerate Dabur India, is in the final stages of negotiations to invest an undisclosed amount in online insurance policy aggregator EasyPolicy.com."

	# Split text into sentences
	sentenceList = rake.split_sentences(text)

	# generate candidate keywords
	stopwordpattern = rake.build_stop_word_regex(stoppath)
	phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)

	# calculate individual word scores
	wordscores = rake.calculate_word_scores(phraseList)

	# generate candidate keyword scores
	keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)

	# sort candidates by score to determine top-scoring keywords
	sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
	totalKeywords = len(sortedKeywords)

	return_words = []
	# take the top four as the final keywords
	for keyword in sortedKeywords[0:4]:
	    return_words.append(keyword[0])

	return return_words

#Example call
#print extract_key("The index had gained 68.22 points in the previous session on Thursday.Nifty acted very range bound facing a strong resistance at 8750 level and found immediate support at 8680 level which we mentioned earlier.Nifty still holds the immediate support placed at 8680 level.Prominent losers among the 30 sensex stocks were TCS, Axis Bank, Bharti Airtel, BHEL, GAIL, HDFC, HDFC Bank, Hero MotoCorp, Infosys, M&M, Maruti Suzuki, NTPC, ONGC, SBI, Sesa Sterlite, Sun Pharma and Tata Motors.These payments amount to around Rs 26 crore, the company said in a release here.Dabur India Ltd: The Burman Family Office, the investment arm of the Burman family, promoters of fast-moving consumer group conglomerate Dabur India, is in the final stages of negotiations to invest an undisclosed amount in online insurance policy aggregator EasyPolicy.com.")