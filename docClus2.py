import nltk
import string
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, ward_tree, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
import matplotlib.pyplot as plt
import json
from collections import defaultdict

#text = []
stemmer = PorterStemmer()

def translate_non_alphanumerics(to_translate, translate_to=u'_'):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)

def docPreprocess(articles):
	text = []
	#print type(articles)
	for eachText in articles:
		#print type(eachText)
		#lowers = eachText.lower()
		processedText = eachText.lower()
		#processedText = lowers.encode('utf-8').translate(None, string.punctuation).decode('utf-8')
		#processedText = translate_non_alphanumerics(lowers)
		text.append(processedText)
		#print text
		#print "\n-----------------\n"
	return text

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = stem_tokens(tokens,stemmer)
	return stems

def tfidfCompute(text):
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	tfs = tfidf.fit_transform(text)
	#print tfidf.get_feature_names()
	return (tfs, tfs.shape)

def kmeansCluster_titles(text):
	tfs_tuple = tfidfCompute(text)
	km = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1,
                verbose=False)
	km.fit(tfs_tuple[0])
	return km.labels_

def kmeansCluster_docs(text, n_clusters=1):
	text = docPreprocess(text)
	tfs_tuple = tfidfCompute(text)
	if len(text) > n_clusters :
		km = KMeans(n_clusters, init='k-means++', max_iter=100, n_init=1,
                verbose=False)
	else:
		km = KMeans(n_clusters=len(text), init='k-means++', max_iter=100, n_init=1,
                verbose=False)
	km.fit(tfs_tuple[0])
	return km.labels_

#SciPy implementation of ward agglomerative clustering
def hierarchicalCluster1(text):
	tfs_tuple = tfidfCompute(text)
	dist = 1 - cosine_similarity(tfs_tuple[0])
	#print dist
	linkage_matrix = ward(dist)
	print linkage_matrix
	fig, ax = plt.subplots(figsize=(15, 20))
	ax = dendrogram(linkage_matrix,p=3, truncate_mode='level',  orientation="right")
	print ax
	plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
	plt.tight_layout() #show plot with tight layout
	plt.savefig('ward_clusters1.png', dpi=200) #save figure as ward_clusters
	plt.close()
	clusters = fcluster(linkage_matrix, 20, depth=2)
	print clusters

#Scikit-Learn implemetation of agglomerative clustering
def hierarchicalCluster(text):
	tfs_tuple = tfidfCompute(text)
	print tfs_tuple[0].shape[0]
	#wardCluster = ward_tree(tfs_tuple[0])
	ahc = AgglomerativeClustering(3, affinity='cosine', linkage="complete")
	wardCluster = ahc.fit_predict(tfs_tuple[0].toarray())
	print wardCluster
	#print ahc.children_
	#print wardCluster.children

#docPreprocess(["NEW DELHI: The S&P BSE Sensex is trading cautiously in the face of a muted trend seen in other Asian markets. Jet Airways rallied over 6 per cent in intraday trade today.Tracking the momentum, the 50-share Nifty index is above its psychological level of 8700, supported by gains in auto, realty, IT and consumer durable stocks.Markets @ 10:25Sensex at 28,714.13; up 4.26 points. Nifty at 8,715.65; up 3.60 points.Top gainers on Sensex: WIPRO (2.1%), HUL (1.4%), INFOSYS (1.3%), M&M (1.2%), GAIL (1.1%)Top losers: SUN PHARMA (-1.3%), CIL (-1.2%), HINDALCO (-1.1%), ONGC (-1.0%), CIPLA (-0.9%). Here is a list of seven stocks which are in focus today:Infrastructure, housing companies will be in focus after the Lok Sabha late on Tuesday passed the contentious Land Acquisition Bill. L&T Ltd: Infrastructure major Larsen and Toubro's Metallurgical and material handling arm has bagged orders worth Rs 1,242 crore during the current quarter. Adani Power Ltd: Success of coal block auctions seems to be fuelling deal flow in the power sector. Gautam Adani's Adani Power is on the prowl and is in advanced talks with Adhunik Group to buy Adhunik Power, sources with direct knowledge said. Financial Technologies Ltd: Financial Technologies' (FTIL's) shareholders, creditors and employees have objected to the proposed amalgamation of its scam-hit subsidiary, National Spot Exchange Ltd (NSEL), with it, said media reports. Asian Paints Ltd: Leading domestic player Asian Paints will set up a manufacturing facility in Andhra Pradesh at an investment of Rs 1,750 crore, spread over 12 years. Maruti Suzuki India Ltd: Maruti Suzuki is recalling over 33,000 units of the Alto to fix a problem with the right-hand door. The potential issue has been noticed in Alto 800 and Alto K10 variants, and the vehicles affected are manufactured between December 8 last year and February 18 this year. NMDC Ltd: State-owned mining giant NMDC Limited, which has been directed by a Supreme Court panel to shut down its famous Panna diamond mines in Madhya Pradesh by June 2016 due to ecological concerns, is now gearing up to approach the apex court again to seek extension of the mining period by four years to 2020.", "NEW DELHI: CLSA, which maintains a 'buy' rating on Sun Pharma, says the valuations are no longer at a premium with peers, though it deserves one. The US FDA observations at Halol, sustainability of high margins, valuations and delay in Ranbaxy turnaround due to cultural differences are key concerns. Recent US approval from Halol should ease concerns around the plant, while Sun's acquisition track record of 20 years gives us confidence of a timely turnaround of Ranbaxy, says a report by CLSA. Shares of Sun Pharma have rallied over 20 per cent so far in the year 2015, compared to a 4 per cent gain seen in the BSE Sensex. Concern 1: US FDA issues at Halol deeper than thought earlier. Investors were concerned about the 23 US FDA observations at Halol, which accounts for 25 per cent of US sales in our view. However, recent approval to manufacture a SPARC product is likely to ease those concerns. While the approval does not completely eliminate the US FDA escalation risk, it lowers the probability of an import alert/warning letter in our view, says the report. Concern 2: Sustainability of high operating margins, low tax rate. High margins are driven by favourable pricing for Taro, strong product mix in the US, robust India business and tight cost structure. We note that Sun's margins were 35percent in FY11 even before Taro started taking price increases in the US. CLSA expects Sun's own margins to gradually decline to 41percent by FY20. Sun derived 40percent of PBT in FY14 from tax-exempt zones. It is difficult to project the tax rate for FY16 due to lack of clarity on contribution of profits from tax free zones and the impending merger with Ranbaxy. Concern 3: Valuations expensive on a risk adjusted basis. Lupin is a preferred pick for investors on a risk adjusted basis. However, recent rally for Lupin/other peers brings its PE valuations in line with Sun Pharma. While we are bullish on Lupin's growth too, Sun provides greater visibility on free cash generation through the Ranbaxy turnaround. Concern 4: Cultural difference could delay the Ranbaxy turnaround. Investors feel that cultural difference could delay the Ranbaxy turnaround and put US$250m of synergy benefits at risk. Sun's track record of turning around 16 acquisitions, which came with diverse cultures, gives us confidence of its ability to turn around Ranbaxy. Moreover Sun's acquisition is in the generic space, an area they understand well.", "NEW DELHI: State-run insurance major LIC on Wednesday committed Rs 1.5 lakh crore to the Indian Railways for development of various commercially viable projects in one of the largest railway networks in the world. The investment would be made over a period of five years. LIC has taken the task of supporting Indian Railways... It is a commercial decision... LIC will invest Rs 1.5 lakh crore over a period of five years, finance minister Arun Jaitley said here. The investment would be done in bonds issued by various railway entities such Indian Railways Finance Corporation (IRFC), beginning next fiscal.", "MUMBAI: The rupee fell by six paise to a fresh two-month low of 62.82 against the US dollar in early trade on Wednesday at the Interbank Foreign Exchange due to rise in the Greenback's value against other global currencies. Forex dealers attributed the fall in the rupee to the dollar's strength against other global currencies and sustained capital outflows but a higher opening in the domestic stock market capped the rupee's fall. The rupee had lost 21 paise to end at two-month low of 62.76 against the dollar in Tuesday's trade on sustained dollar demand from importers amid rate hike concerns by the US Federal Reserve.","ET Now: Let us start with the Bank Nifty. That was the consensus trade for 2015; buy banks and do not sell PSU banks, and that trade has reversed completely? Devang Mehta: Yes and the major part of the fall in the Bank Nifty is because of the absence of any sort of cues. In fact, the 25 bps surprise rate cut by the RBI was also sold into. So probably, this has more to do with the drag in the earnings that we saw in the last quarter and there are no evidences that the Q4 earnings for a lot of PSU banks would be good. So probably Bank Nifty is leading the market down, which was even leading the market on the way up. So for how much time would be your pharma, IT as well FMCG stocks support the market in terms of its upmove is anybody's call. Probably there is a lack of cues, that is the absence of any fresh trigger for the Indian market at least till the next one month when the new result season or the Q4 result season starts. So yes, one needs to be a little cautious. The money again would find its way into the defensives. ET Now: What is the sense that you are getting about the ongoing telecom auctions? It is turning out to be a bump off for the incumbents, be it an Idea or a Bharti? Devang Mehta: Yes. Probably Bharti as well as Idea have borne the brunt of a huge bill coming their way. Whatever I gather from watching the TV channels is that probably the bills would be a lot lesser and the incumbent would be benefited by a lot. Reliance Jio was supposed to be a big threat for all these companies, which is not coming out at this point. So yes, for Idea and Bharti, the pent-up demand would be to buy these stocks and they would rally a little bit if the final numbers come out in a short while or may be by tomorrow. ET Now: But I wonder what is the excitement all about? Ultimately be it Bharti, Idea, Reliance or RComm, they will have to shell out top dollar in order to acquire some of the spectrums. Balance sheets would be stretched. In the short term, ARPUs will not recover, and interest outgo will only increase. Devang Mehta: Definitely. Seeing the health of the balance sheet of almost all these companies, except for the exception of maybe Idea to a certain extent whose dynamics because of the pure operations in Indian market are doing well. Generally, we have maintained that the telecom sector can still underperform for some time for the reasons that you have mentioned. I fully agree that because of a lot of load on the balance sheet of these companies as well as non-expansion in the ARPUs and not even addition of the value added services business, these businesses will suffer and these are only trading gains that people would get into. But for investors we would still say that telecom is a sector which one can safely avoid. ET Now: The pharma index for three years on the trot has given a positive return. This year it has appreciated by about 16%, that makes up the best sub performing index. So what explains the underlying strength in the pharma index? Devang Mehta: Three things actually come to the fore. One is the Indian competencies in terms of the pharma sector. Another part is the export competitiveness because of the weakening of the Indian currency. The third thing is a huge market in India itself, probably even as I said about exports. So these three factors come to the fore. An important part is that normally all these companies have been coming up with good set of numbers quarter over quarter and we have seen a two-three years of exemplary performances by the leaders like Sun Pharma or Lupin or Dr Reddy for the exception of one or two quarters. But generally, all these companies who have done some acquisitions have also turned profitable. So we feel that there is still some upside left in the stocks, though I would say that valuations in the large cap space are a little too expensive for comfort, but we do not see pharma stocks correcting big time. So there is some comfort for the investors in pharma stocks. I like stocks like Granules India, Suven Life Sciences, and Natco Pharma. There is still some upside left in these midcap stocks"])
#tfs_tuple = kmeansCluster(text)
#hierarchicalCluster1(text)
#print tfs_tuple[1]
#print tfs_tuple[0]

def docClus (json_file):
	json_data = open(json_file)
	root_node = json.load(json_data)
	json_data.close()
	#print root_node["root"][0]["title"]
	articles = root_node["root"]
	titles_dict = {}
	contents_dict = {}
	for article in articles:
		titles_dict[article["id"]] = article["title"]
		contents_dict[article["id"]] = article["content"].encode('utf-8')

	#print titles_dict
	#tfs = hierarchicalCluster(titles_dict.values())
	#print tfs

	#print len(contents_dict.values())

	tfs_tuple = kmeansCluster_docs(contents_dict.values(), n_clusters=13)
	'''for key in titles_dict.keys():
		print (key, titles_dict[key] , tfs_tuple[key-1])
	'''
	titles_clustered = defaultdict(list)

	for i in range(len(tfs_tuple)) :
		titles_clustered[tfs_tuple[i]].append(i+1)

	#clusterings at level 0
	#print titles_clustered

	docsClustered = defaultdict(dict)

	for cluster in titles_clustered.keys():
		similarDocs = []
		indices = titles_clustered[cluster]
		for index in indices:
			similarDocs.append(contents_dict[index])
		#print similarDocs
		#print "---------------------------"
		tfs_tuple_doc = kmeansCluster_docs(similarDocs,n_clusters=12)
		#print tfs_tuple_doc
		#print "***************************"
		docsClustered[cluster] = defaultdict(list)
		for i in range(len(tfs_tuple_doc)):
			docsClustered[cluster][tfs_tuple_doc[i]].append(indices[i]) 

	print "document clusterings : "
	for key in docsClustered.keys():
		print "Level 1 - label : ", key
		v = docsClustered[key]
		for key1 in v.keys():
			print "Level 2 - label : ", key1
			print "document ids : ", v[key1]

	'''for key1 in docsClustered.keys():
		print key1
		val = docsClustered[key1]
		for key2 in val.keys():
			print key2 , val[key2]'''

	return docsClustered