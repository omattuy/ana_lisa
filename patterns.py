from topicanalysis import TopicAnalysis
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
	    self.readmeFileDoesNotExists = False
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
	        self.readmeFileDoesNotExists = True
	    return self.readmeFileDoesNotExists

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