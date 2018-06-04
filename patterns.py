class Patterns:

	def __init__(self, targetFile):
		self.targetFile = targetFile

	def checkNameSize(self):
	    list_Names = []
	    name = "name = "
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(name) != -1:
	            nameUnderAnalysis = line[line.find('\"')+1:len(line)-2]
	            if (len(nameUnderAnalysis) > 100):
	                redFlag = ("Linha " + str(count) + ": " + nameUnderAnalysis)
	                list_Names.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_Names

	def checkRequestSize(self):
	    list_Requests = []
	    request = "request = "
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(request) != -1:
	            requestUnderAnalysis = line[line.find('\"')+1:len(line)-2]
	            if (len(requestUnderAnalysis) > 100):
	                redFlag = "Linha " + str(count) + ": " + requestUnderAnalysis
	                list_Requests.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_Requests

	def checkExistenceEmptySpaceCharacter(self):
	    list_empty_space_characters = []
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line[len(line) - 2] == ' ':
	            redFlag = "Linha " + str(count)
	            list_empty_space_characters.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_empty_space_characters

	def checkExistenceGrammarTube(self):
	    checkExistenceGrammar = False
	    grammar = "grammar("
	    line = self.targetFile.readline()
	    while line:
	        if line.find(grammar) != -1:
	            checkExistenceGrammar = True
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return checkExistenceGrammar