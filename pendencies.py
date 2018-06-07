from comments import Comment
from topicanalysis import TopicAnalysis

class Pendencies:

	def __init__(self, targetFile):
		self.targetFile = targetFile

	def checkExistenceFixmes(self):
	    self.list_Fixmes = []
	    fixme = "FIXME"
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(fixme) != -1:
	            fixmeUnderAnalysis = line[line.find(fixme)+6:len(line)]
	            redFlag = "Linha " + str(count) + ":" + fixmeUnderAnalysis
	            self.list_Fixmes.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return self.list_Fixmes

	def checkExistenceTodos(self):
	    self.list_Todos = []
	    todo = "// TODO"
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(todo) != -1:
	            todoUnderAnalysis = line[line.find(todo)+7:len(line)]
	            redFlag = "Linha " + str(count) + ": " + todoUnderAnalysis
	            self.list_Todos.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return self.list_Todos

	def checkExistenceComment(self):
	    lineNumber = 1
	    idx_beg_comment = "/*"
	    idx_end_comment = "*/"
	    self.list_comments = []
	    comment = ""
	    line = self.targetFile.readline()
	    while line:
	        if line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) != -1:
	            c = Comment()
	            c.setLineNumberBegComment(lineNumber)
	            c.setCompleteComment(line[line.find(idx_beg_comment)+2:line.find(idx_end_comment)])
	            self.list_comments.append(c)
	        elif line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) == -1:
	            c = Comment()
	            c.setLineNumberBegComment(lineNumber)
	            while line.find(idx_end_comment) == -1:
	                comment = comment + line
	                line = self.targetFile.readline()
	                lineNumber = lineNumber + 1
	            comment = comment + line # Última linha do comentário
	            c.setCompleteComment(comment)
	            self.list_comments.append(c)
	        line = self.targetFile.readline()
	        comment = ""
	        lineNumber = lineNumber + 1
	    self.targetFile.seek(0)
	    return self.list_comments

	def checkExistenceUnfinishedPrints(self):
	    self.list_unfinished_prints = []
	    unfinished_prints = "print \"\""
	    line = self.targetFile.readline()
	    count = 1
	    while line:
	        if line.find(unfinished_prints) != -1:
	            redFlag = "Linha " + str(count)
	            self.list_unfinished_prints.append(redFlag)
	        line = self.targetFile.readline()
	        count = count + 1
	    self.targetFile.seek(0)
	    return self.list_unfinished_prints

	def collectAllVariablesAndCheckExistenceUnusedStructs(self):

	    def collectAllStructs(self):
	        self.list_DeclaredStructs = []
	        begVariable = "+<"
	        endVariable = "> : "
	        cu = "Currency"
	        re = "Real"
	        bo = "Boolean"
	        li = "List"
	        st = "String"
	        da = "Date"
	        i = "Integer"
	        te = "Text"
	        ti = "Time"
	        idxBegVariable = 0
	        idxEndVariable = 0
	        line = self.targetFile.readline()
	        while line:
	            if line.find(begVariable) != -1:
	                if (line.find(ti) == -1 and line.find(te) == -1 and line.find(cu) == -1 and line.find(re) == -1 and line.find(bo) == -1 and line.find(li) == -1 and line.find(st) == -1 and line.find(da) == -1 and line.find(i) == -1):
	                    idxBegVariable = line.find(begVariable)
	                    idxEndVariable = line.find(endVariable)
	                    self.list_DeclaredStructs.append(line[idxBegVariable+2:idxEndVariable])
	            line = self.targetFile.readline()
	        self.targetFile.seek(0)
	        return self.list_DeclaredStructs

	    def checkExistenceUnusedStructs(self):
	        self.list_DeclaredStructs = collectAllStructs(self)
	        self.list_UnusedStructs = []
	        for u in self.list_DeclaredStructs:
	            count = 0
	            line = self.targetFile.readline()
	            while line:
	                if line.find(u + ".") != -1:
	                    count = count + 1
	                line = self.targetFile.readline()
	            if count == 0:
	                self.list_UnusedStructs.append(u)
	            self.targetFile.seek(0)
	        return self.list_UnusedStructs

	    self.list_UnusedStructs = checkExistenceUnusedStructs(self)
	    return self.list_UnusedStructs

	def collectAllVariablesAndCheckExistenceUnusedVariables(self):

	    def collectAllVariables(self):
	        self.list_DeclaredVariables = []
	        begVariable = "+<"
	        endVariable = "> : "
	        idxBegVariable = 0
	        idxEndVariable = 0
	        line = self.targetFile.readline()
	        while line:
	            if line.find(begVariable) != -1:
	                if (line.find('*') == -1 and line.find('struct') == -1):
	                    idxBegVariable = line.find(begVariable)
	                    idxEndVariable = line.find(endVariable)
	                    self.list_DeclaredVariables.append(line[idxBegVariable+2:idxEndVariable])
	            line = self.targetFile.readline()
	        self.targetFile.seek(0)
	        return self.list_DeclaredVariables

	    def checkExistenceUnusedVariables(self):
	        self.list_DeclaredVariables = collectAllVariables(self)
	        self.list_UnusedVariables = []
	        for u in self.list_DeclaredVariables:
	            count = 0
	            line = self.targetFile.readline()
	            while line:
	                if line.find(u) != -1:
	                    count = count + 1
	                line = self.targetFile.readline()
	            if count == 1:
	                self.list_UnusedVariables.append(u)
	            self.targetFile.seek(0)
	        return self.list_UnusedVariables

	    self.list_UnusedVariables = checkExistenceUnusedVariables(self)
	    return self.list_UnusedVariables

	def collectTopicsNotBeingUsed(self):
	    ta = TopicAnalysis(self.targetFile)
	    self.name_all_topics = ta.checkNamesAllTopics()
	    self.list_topics_not_being_used = []
	    for t in self.name_all_topics:
	        count = 0
	        line = self.targetFile.readline()
	        while line:
	            if line.find(t.getNameTopic()[:t.getNameTopic().find(']')+1]) != -1:
	                count += 1
	            line = self.targetFile.readline()
	        if count == 1:
	            self.list_topics_not_being_used.append(t)
	        self.targetFile.seek(0)
	    return self.list_topics_not_being_used