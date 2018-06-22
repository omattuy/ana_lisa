from lists import List

class Errors:

	def __init__(self, targetFile):
		self.targetFile = targetFile

	def collectAllLists(self):
	    listSyntax = ': List'
	    self.list_of_lists = []
	    line = self.targetFile.readline()
	    while line:
	        if line.find(listSyntax) != -1:
	            l = List()
	            if line.find('[') != -1:
	                l.setListAlias(line[line.find('[') + 1 :line.find(']')])
	            elif line.find('<') != -1:
	                l.setListAlias(line[line.find('<') + 1 :line.find('>')])
	            while line.find('atomic') == -1:
	                line = self.targetFile.readline()
	            if 'true' in line:
	                l.setAtomicList(True)
	            elif 'false' in line:
	                l.setAtomicList(False)
	            self.list_of_lists.append(l)
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return self.list_of_lists

	def checkListsWithIncorrectSyntax(self):
		self.list_of_lists = self.collectAllLists()
		self.lists_with_incorrect_syntax = []
		line = self.targetFile.readline()
		for l in self.list_of_lists:
			line = self.targetFile.readline()
			lineNumber = 1
			list_line_numbers = []
			while line:
				if line.find(l.getListAlias()) != -1 and line.find('if') != -1 and line.find('{') != -1:
					print('debug -> ' + l.getListAlias() + ' ' + str(lineNumber))
					if l.getAtomicList() == True and line.find(' IN ') != -1:
						if l not in self.lists_with_incorrect_syntax:
							list_line_numbers.append(lineNumber)
							l.setListLineNumber(list_line_numbers)
							self.lists_with_incorrect_syntax.append(l)
						else:
							l.getListLineNumber().append(lineNumber)
					elif l.getAtomicList() == False and line.find(' IN ') == -1:
						if l not in self.lists_with_incorrect_syntax:
							list_line_numbers.append(lineNumber)
							l.setListLineNumber(list_line_numbers)
							self.lists_with_incorrect_syntax.append(l)
						else:
							l.getListLineNumber().append(lineNumber)
				line = self.targetFile.readline()
				lineNumber = lineNumber + 1
			self.targetFile.seek(0)
		return self.lists_with_incorrect_syntax