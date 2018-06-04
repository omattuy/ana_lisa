import os.path
from comments import Comment

class Pendencies:

	def __init__(self, fileName, targetFile):
		self.fileName = fileName
		self.targetFile = targetFile

	def checkExistenceReadmeFile(self):
	    readmeFileDoesNotExists = False
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
	        readmeFileDoesNotExists = True
	    return readmeFileDoesNotExists

	def checkExistenceFixmes(self):
	    list_Fixmes = []
	    fixme = "FIXME"
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(fixme) != -1:
	            fixmeUnderAnalysis = line[line.find(fixme)+6:len(line)]
	            redFlag = "Linha " + str(count) + ":" + fixmeUnderAnalysis
	            list_Fixmes.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_Fixmes

	def checkExistenceTodos(self):
	    list_Todos = []
	    todo = "// TODO"
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(todo) != -1:
	            todoUnderAnalysis = line[line.find(todo)+7:len(line)]
	            redFlag = "Linha " + str(count) + ": " + todoUnderAnalysis
	            list_Todos.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_Todos

	def checkExistenceComment(self):
	    lineNumber = 1
	    idx_beg_comment = "/*"
	    idx_end_comment = "*/"
	    list_comments = []
	    comment = ""
	    line = self.targetFile.readline()
	    while line:
	        if line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) != -1:
	            c = Comment()
	            c.setLineNumberBegComment(lineNumber)
	            c.setCompleteComment(line[line.find(idx_beg_comment)+2:line.find(idx_end_comment)])
	            list_comments.append(c)
	        elif line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) == -1:
	            c = Comment()
	            c.setLineNumberBegComment(lineNumber)
	            while line.find(idx_end_comment) == -1:
	                comment = comment + line
	                line = self.targetFile.readline()
	                lineNumber = lineNumber + 1
	            comment = comment + line # Última linha do comentário
	            c.setCompleteComment(comment)
	            list_comments.append(c)
	        line = self.targetFile.readline()
	        comment = ""
	        lineNumber = lineNumber + 1
	    self.targetFile.seek(0)
	    return list_comments

	def checkExistenceStatements(self):
	    checkExistenceStatement = False
	    statement = "Statement"
	    line = self.targetFile.readline()
	    while line:
	        if line.find(statement) != -1:
	            checkExistenceStatement = True
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return checkExistenceStatement

	def checkExistenceUnfinishedPrints(self):
	    list_unfinished_prints = []
	    unfinished_prints = "print \"\""
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(unfinished_prints) != -1:
	            redFlag = "Linha " + str(count)
	            list_unfinished_prints.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return list_unfinished_prints