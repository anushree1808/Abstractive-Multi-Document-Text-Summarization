import os
os.environ['JAVAHOME'] = "C:/Program Files/Java/jdk1.8.0_31/bin"
#print os.environ['JAVAHOME']

from nltk.tag.stanford import NERTagger
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

#nltk.internals.config_java(options='-xmx2G')
st = NERTagger('stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','stanford-ner-2014-06-16/stanford-ner.jar', encoding='utf-8')


def replacePronoun(sentences_string):
	#sentences_string = "John has refused the offer from Facebook. He will work for that. They will offer him Rs.20 lakhs. Google also want him. They will offer him 30 lakhs."
	#sentences_string = "Biswajit Baruah, ET Bureau Mar 28, 2015, 04.07AM IST(Reflecting the mood, analysts\u2026) MUMBAI: Shares of telecom companies such as Bharti Airtel, Idea Cellular and Reliance Communications (RCOM) dropped more than 5% on Friday on fears of aggressive bidding for airwaves, a development that may exert pressure on companies' balance sheets and cash flow, and restrict their expansion plans. Reflecting the mood, analysts maintained a cautious outlook on the sector, saying fresh buyers should stay away from this space in the near-term. On Friday, the department of telecommunications (DoT) released details of bidders at the recently concluded airwaves auction, where the government mopped up Rs 1.1 lakh crore from the spectrum put up for auction. The prices for the spectrum were considerably higher than the reserve price, said analysts. \"Bharti Airtel and Idea Cellular have paid a little more for the spectrum than what the markets were expecting,\" said Mayuresh Joshi, VP, (institutional) Angel Broking. \"Going forward, Reliance Jio's pricing for its services would be closely watched. However, investors should note that the overhang on telecom stocks over spectrum is probably over.\" Telecom stocks came under intense selling pressure on Friday \u2014 Bharti Airtel fell 5.64% to Rs 376. Idea Cellular dropped 4.96% to Rs 171 after touching new 52-week high of Rs 187 in early trade. RCOM touched a new 52-week low of Rs 56.90 before closing at Rs 58.25, down 3.56%, while Tata Teleservices (Maharashtra) ended 1.54% lower at Rs 7.68. Shares of some telecom companies \u2014 Bharti Airtel, Idea Cellular \u2014 have had a good run in the past one year, gaining 21% and 23%, respectively, while Reliance Communications dropped 53%; all these stocks have underperformed the ET 100 Index which gained nearly 27% over the same period. \"We reiterate our cautious view on the telecom sector, given the stretched balance sheets, rising capital expenditure, regulatory pushback, Reliance Jio's launch overhang, and expensive valuations,\" said Vinay Jaising, analyst at Morgan Stanley. They are also sceptical of Indian telecom companies due to a number of structural issues such as cannibalisation of voice by data, rapid expansion and network operational cost to deliver data, pricing impact from the imminent entry of Reliance Jio, and stretched balance sheets due to spectrum prices. \"Telcos will further bloat their balance sheet with debt, which is already under severe strain. We maintain 'hold' rating for Bharti Airtel and Idea Cellular with a price target of Rs 399 and Rs 167\/share, respectively,\" said Amar Mourya, research analyst at IndiaNivesh. Most telecom companies may report negative free cash flow in 2015 as they are required to pay a quarter of the committed amount in the spectrum auction upfront, and the rest will be paid in installments over 10 years from 2017."
	#sentences_string = "John and Aayush Agarwal for Google. They earn a lot. Shyam works for Cisco. They will pay him less."
	#sentences_string = "John works for Google. He is enjoying in that company a lot."
	
	sentences = sent_tokenize(sentences_string)
	#print sentences
	#print ".................."*3
	person = []
	person_pos = ""
	organisation = []
	organisation_pos = ""
	mark = -9999999999

	for i in range(len(sentences)):
		print type(sentences[i])
		print type(sentences[i].encode('utf-8'))
		words = word_tokenize(sentences[i])
		return
		pos_tags = nltk.pos_tag(words)
		words = word_tokenize(sentences[i])
		ner_tags = st.tag(words)
		#print pos_tags
		#print ner_tags

		for j in range(len(pos_tags)):
			if(pos_tags[j][1]=='PRP'):
				tag = pos_tags[j][0]
				if len(person)!=0 and tag.lower() in ["he", "she"]:
					#print tag, person
					pos_tags[j] = (person[0], person_pos)
				elif (len(organisation)!=0) and (tag.lower() in ["they"]) and len(person)<=1:
					#print tag, organisation
					pos_tags[j] = (", ".join(organisation),organisation_pos)
				elif len(person)!=0 and len(organisation)==0 and tag.lower() in ["they"]:
					pos_tags[j] = (", ".join(person), person_pos)
			
			elif(pos_tags[j][0].lower() in ["company", "organisation"]):
				#print "hi" , pos_tags[j][0]
				if(j>0) and pos_tags[j-1][0].lower() in ["this", "that"] and len(organisation)!=0:
					#print "hillo"
					pos_tags[j] = (", ".join(organisation),organisation_pos)
					mark = j-1		

		if(mark > -1):
			del pos_tags[mark]
			mark = -99999999
		words = [tupl[0] for tupl in pos_tags]
		sentence = " ".join(words)
		sentences[i] = sentence
		#print "\n", sentences[i]
		temp_person = []
		temp_organisation = []
		for k in range(len(ner_tags)):
			if(ner_tags[k][1]=="PERSON"):
				temp_person.append(ner_tags[k][0])
			elif(ner_tags[k][1]=="ORGANIZATION"):
				temp_organisation.append(ner_tags[k][0])

		if len(temp_organisation)>0:
			organisation = temp_organisation
		if len(temp_person) > 0:
			person = temp_person
		#print person, organisation

		#print "ner_tags : ", ner_tags
		#print "pos_tag : ", pos_tags
		#print "``````````````````" * 3

	final_text = (" ").join(sentences)
	print final_text
	return final_text

#sent = "Biswajit Baruah, ET Bureau Mar 28, 2015, 04.07AM IST(Reflecting the mood, analysts\u2026)MUMBAI: Shares of telecom companies such as Bharti Airtel, Idea Cellular and Reliance Communications (RCOM) dropped more than 5% on Friday on fears of aggressive bidding for airwaves, a development that may exert pressure on companies' balance sheets and cash flow, and restrict their expansion plans. Reflecting the mood, analysts maintained a cautious outlook on the sector, saying fresh buyers should stay away from this space in the near-term. On Friday, the department of telecommunications (DoT) released details of bidders at the recently concluded airwaves auction, where the government mopped up Rs 1.1 lakh crore from the spectrum put up for auction. The prices for the spectrum were considerably higher than the reserve price, said analysts. \"Bharti Airtel and Idea Cellular have paid a little more for the spectrum than what the markets were expecting,\" said Mayuresh Joshi, VP, (institutional) Angel Broking. \"Going forward, Reliance Jio's pricing for its services would be closely watched.came under intense selling pressure on Friday \u2014 Bharti Airtel fell 5.64% to Rs 376. Idea Cellular dropped 4.96% to Rs 171 after touching new 52-week high of Rs 187 in early trade. RCOM touched a new 52-week low of Rs 56.90 before closing at Rs 58.25, down 3.56%, while Tata Teleservices (Maharashtra) ended 1.54% lower at Rs 7.68. Shares of some telecom companies \u2014 Bharti Airtel, Idea Cellular \u2014 have had a good run in the past one year, gaining 21% and 23%, respectively, while Reliance Communications dropped 53%; all these stocks have underperformed the ET 100 Index which gained nearly 27% over the same period. \"We reiterate our cautious view on the telecom sector, given the stretched balance sheets, rising capital expenditure, regulatory pushback, Reliance Jio's launch overhang, and expensive valuations,\" said Vinay Jaising, analyst at Morgan Stanley. They are also sceptical of Indian telecom companies due to a number of structural issues such as cannibalisation of voice by data, rapid expansion and network operational cost to deliver data, pricing impact from the imminent entry of Reliance Jio, and stretched balance sheets due to spectrum prices. \"Telcos will further bloat their balance sheet with debt, which is already under severe strain. We maintain 'hold' rating for Bharti Airtel and Idea Cellular with a price target of Rs 399 and Rs 167/share, respectively,\" said Amar Mourya, research analyst at IndiaNivesh. Most telecom companies may report negative free cash flow in 2015 as they are required to pay a quarter of the committed amount in the spectrum auction upfront, and the rest will be paid in installments over 10 years from 2017."
#print type(sent)
#print type(sent.encode('utf-8'))
#replacePronoun("Biswajit Baruah, ET Bureau Mar 28, 2015, 04.07AM IST(Reflecting the mood, analysts\u2026)MUMBAI: Shares of telecom companies such as Bharti Airtel, Idea Cellular and Reliance Communications (RCOM) dropped more than 5% on Friday on fears of aggressive bidding for airwaves, a development that may exert pressure on companies' balance sheets and cash flow, and restrict their expansion plans. Reflecting the mood, analysts maintained a cautious outlook on the sector, saying fresh buyers should stay away from this space in the near-term. On Friday, the department of telecommunications (DoT) released details of bidders at the recently concluded airwaves auction, where the government mopped up Rs 1.1 lakh crore from the spectrum put up for auction. The prices for the spectrum were considerably higher than the reserve price, said analysts. \"Bharti Airtel and Idea Cellular have paid a little more for the spectrum than what the markets were expecting,\" said Mayuresh Joshi, VP, (institutional) Angel Broking. \"Going forward, Reliance Jio's pricing for its services would be closely watched.came under intense selling pressure on Friday \u2014 Bharti Airtel fell 5.64% to Rs 376. Idea Cellular dropped 4.96% to Rs 171 after touching new 52-week high of Rs 187 in early trade. RCOM touched a new 52-week low of Rs 56.90 before closing at Rs 58.25, down 3.56%, while Tata Teleservices (Maharashtra) ended 1.54% lower at Rs 7.68. Shares of some telecom companies \u2014 Bharti Airtel, Idea Cellular \u2014 have had a good run in the past one year, gaining 21% and 23%, respectively, while Reliance Communications dropped 53%; all these stocks have underperformed the ET 100 Index which gained nearly 27% over the same period. \"We reiterate our cautious view on the telecom sector, given the stretched balance sheets, rising capital expenditure, regulatory pushback, Reliance Jio's launch overhang, and expensive valuations,\" said Vinay Jaising, analyst at Morgan Stanley. They are also sceptical of Indian telecom companies due to a number of structural issues such as cannibalisation of voice by data, rapid expansion and network operational cost to deliver data, pricing impact from the imminent entry of Reliance Jio, and stretched balance sheets due to spectrum prices. \"Telcos will further bloat their balance sheet with debt, which is already under severe strain. We maintain 'hold' rating for Bharti Airtel and Idea Cellular with a price target of Rs 399 and Rs 167/share, respectively,\" said Amar Mourya, research analyst at IndiaNivesh. Most telecom companies may report negative free cash flow in 2015 as they are required to pay a quarter of the committed amount in the spectrum auction upfront, and the rest will be paid in installments over 10 years from 2017.".encode('utf-8'))