class Errors:

	list_lists = []

	def __init__(self, targetFile):
		self.targetFile = targetFile

	def collectAllLists(self):
	    listSyntax = ': List'
	    global list_lists
	    line = self.targetFile.readline()
	    while line:
	        if line.find(listSyntax) != -1:
	            l = List()
	            if line.find('[') != -1:
	                l.setListAlias(line[line.find('['):line.find(']') + 1])
	            elif line.find('<') != -1:
	                l.setListAlias(line[line.find('<'):line.find('>') + 1])
	            while line.find('atomic') == -1:
	                line = self.targetFile.readline()
	            if 'true' in line:
	                l.setTypeList(True)
	            elif 'false' in line:
	                l.setTypeList(False)
	            list_lists.append(l)
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return list_lists

	def checkListsWithIncorrectSyntax(self):
	    lists_with_incorrect_syntax = []
	    line = self.targetFile.readline()
	    global list_lists
	    for l in list_lists:
	        line = self.targetFile.readline()
	        lineNumber = 1
	        list_line_numbers = []
	        while line:
	            if line.find('.' + l.getListAlias()[1:len(l.getListAlias())-1]) != -1:
	                if l.getTypeList() == True and line.find('IN') != -1:
	                    if l not in lists_with_incorrect_syntax:
	                        list_line_numbers.append(lineNumber)
	                        l.setListLineNumber(list_line_numbers)
	                        lists_with_incorrect_syntax.append(l)
	                    else:
	                        l.getListLineNumber().append(lineNumber)
	                elif l.getTypeList() == False and line.find('IN') == -1:
	                    if l not in lists_with_incorrect_syntax:
	                        list_line_numbers.append(lineNumber)
	                        l.setListLineNumber(list_line_numbers)
	                        lists_with_incorrect_syntax.append(l)
	                    else:
	                        l.getListLineNumber().append(lineNumber)
	            line = self.targetFile.readline()
	            lineNumber = lineNumber + 1
	        self.targetFile.seek(0)
	    self.targetFile.seek(0)
	    return lists_with_incorrect_syntax