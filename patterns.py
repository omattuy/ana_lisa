from topicanalysis import TopicAnalysis
from repetitive_code import RepetitiveCode
import os.path

class Patterns:

	def __init__(self, targetFile, fileName):
		self.targetFile = targetFile
		self.fileName = fileName

	def checkNameSize(self):
		self.list_Names = []
		name = "name = "
		line = self.targetFile.readline()
		count = 1
		while line:
			if line.find(name) != -1:
				nameUnderAnalysis = line[line.find('\"') + 1:len(line) - 2]
				if (len(nameUnderAnalysis) > 100):
					redFlag = ("Linha " + str(count) + ": " + nameUnderAnalysis)
					self.list_Names.append(redFlag)
			line = self.targetFile.readline()
			count = count + 1
		self.targetFile.seek(0)
		return self.list_Names

	def checkRequestSize(self):
		self.list_Requests = []
		request = "request = "
		line = self.targetFile.readline()
		count = 1
		while line:
			if line.find(request) != -1:
				requestUnderAnalysis = line[line.find('\"') + 1:len(line) - 2]
				if (len(requestUnderAnalysis) > 100):
					redFlag = "Linha " + str(count) + ": " + requestUnderAnalysis
					self.list_Requests.append(redFlag)
			line = self.targetFile.readline()
			count = count + 1
		self.targetFile.seek(0)
		return self.list_Requests

	def checkExistenceGrammarTube(self):
	    self.checkExistenceGrammar = False
	    grammar = "grammar("
	    line = self.targetFile.readline()
	    while line:
	        if line.find(grammar) != -1:
	            self.checkExistenceGrammar = True
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return self.checkExistenceGrammar

	def checkExistenceStatements(self):
	    self.checkExistenceStatement = False
	    statement = "Statement"
	    line = self.targetFile.readline()
	    while line:
	        if line.find(statement) != -1:
	            self.checkExistenceStatement = True
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return self.checkExistenceStatement

	def checkExistenceReadmeFile(self):
	    self.readmeFileDoesNotExist = False
	    if self.fileName.find("TEMP_") != -1:
	        filePath = self.fileName[:self.fileName.find("TEMP_")]
	    elif self.fileName.find("FRM_") != -1:
	        filePath = self.fileName[:self.fileName.find("FRM_")]
	    elif self.fileName.find("NODES_") != -1:
	        filePath = self.fileName[:self.fileName.find("NODES_")]
	    elif self.fileName.find("STRC_") != -1:
	        filePath = self.fileName[:self.fileName.find("STRC_")]
	    my_file = filePath + "README.txt"
	    if os.path.isfile(my_file) == False:
	        self.readmeFileDoesNotExist = True
	    return self.readmeFileDoesNotExist

	def checkExistenceEmptySpaceCharacter(self):
	    self.list_empty_space_characters = []
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line[len(line) - 2] == ' ':
	            redFlag = "Linha " + str(count)
	            self.list_empty_space_characters.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return self.list_empty_space_characters

	def collectOnlyStaticTopics(self):
	    ta = TopicAnalysis(self.targetFile)
	    self.list_all_topics = ta.collectAllTopics()
	    self.list_static_topics = []
	    for t in self.list_all_topics:
	        if 'use topic[' not in t.getCompleteTopic() and 'use *topic[' not in t.getCompleteTopic():
	            if 'if' not in t.getCompleteTopic():
	                self.list_static_topics.append(t)
	    return self.list_static_topics

	def collectTopicsLargeNumberParagraphs(self):
	    ta = TopicAnalysis(self.targetFile)
	    self.list_all_topics = ta.collectAllTopics()
	    self.list_topics_large_number_paragraphs = []
	    for t in self.list_all_topics:
	        if 'use topic[' not in t.getCompleteTopic() and 'use *topic[' not in t.getCompleteTopic():
	            if t.getCompleteTopic().count('\p') > 10:
	                self.list_topics_large_number_paragraphs.append(t)
	    return self.list_topics_large_number_paragraphs

	def checkExistenceRepetitiveLinesCode(self):
		def getFourLinesCode():
			idx = 0
			list_four_lines_code = []
			all_lines_of_file = self.targetFile.readlines()
			while idx < len(all_lines_of_file):
				self.four_lines_code = ""
				rp = RepetitiveCode()
				for i in range(4):
					if idx < len(all_lines_of_file):
						self.four_lines_code += all_lines_of_file[idx]
						if i == 0:
							self.first_line = idx
							idx += 1
						elif i == 3:
							idx = self.first_line + 1
						else:
							idx += 1
				rp.setNumberFirstLine(self.first_line)
				rp.setFourLinesCode(self.four_lines_code)
				list_four_lines_code.append(rp)
			return list_four_lines_code

		def checkEntireDocumentForRepetitiveCode(list_four_lines_code):
			repetitive_section = []
			for l in list_four_lines_code:
				idx = 0
				count = 0
				while idx < len(list_four_lines_code):
					if l.getFourLinesCode() == list_four_lines_code[idx].getFourLinesCode():
						count += 1
						if count >= 2:
							repetitive_section.append(l)
					idx += 1
			return repetitive_section

		list_four_lines_code = getFourLinesCode()
		repetitive_section = checkEntireDocumentForRepetitiveCode(list_four_lines_code)
		#for i in repetitive_section:
		#	print(i.getFourLinesCode())