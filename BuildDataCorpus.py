import os
from os import path
import json
from datetime import datetime
import time
import ReplacePronoun

class BuildDataCorpus():
	def __init__(self, input_file_dir, output_file_dir, corpus_filename):
		self.input_file_dir = input_file_dir
		self.output_file_dir = output_file_dir
		self.corpus_filename = corpus_filename

	def buildJson(self):
		os.chdir(self.input_file_dir)
		files = filter(path.isfile, os.listdir("."))
		json_array = []
		index = 0
		article_id = 0
		for json_file in files:
			data = json.loads(open(json_file).read())['root']
			file_date = time.ctime(os.path.getmtime(json_file))
			for news in data:
				dt = news["pubdate"] 
				t1 = datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S +0530")
				if index == 0 or t1 >= t2:
					article_id +=1
					news["id"] = article_id
					content = news["content"]
					#print(type(content))
					content = ReplacePronoun.replacePronoun(content)
					news["content"] = content
					json_array.append(news)
			t2 = datetime.strptime(file_date,"%a %b %d %H:%M:%S %Y")		
			index += 1		
		data = {}
		data["root"] = json_array
		os.chdir(self.output_file_dir)
		with open(self.corpus_filename, 'w') as outfile:
		    json.dump(data, outfile)
#b = BuildDataCorpus(<path_of_input_directory>,<path_of_output_directory>,<output_json_file>)
print "hello"
b = BuildDataCorpus('C:\wamp\www\DataCorpus_Anu', 'C:\Python27', 'DataCorpus4.json')
b.buildJson()		    

 		
