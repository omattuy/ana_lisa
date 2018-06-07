from topics import Topic

class TopicAnalysis:

	def __init__(self, targetFile):
		self.targetFile = targetFile

	def checkNamesAllTopics(self):
	    line = self.targetFile.readline()
	    self.name_all_topics = []
	    while line:
	        if line.find('topic') != -1 and line.find('{') != -1:
	            t = Topic()
	            t.setNameTopic(line[line.find('topic'):line.find('{')+1])
	            self.name_all_topics.append(t)
	        line = self.targetFile.readline()
	    self.targetFile.seek(0)
	    return self.name_all_topics

	def collectAllTopics(self):
	    self.name_all_topics = self.checkNamesAllTopics()
	    self.list_all_topics = []
	    topic_wrong_syntax = []
	    for name in self.name_all_topics:
	        line = self.targetFile.readline()
	        while line:
	            if line.find(name.getNameTopic()) != -1:
	                t = Topic()
	                topic = line
	                count_maximum = 1
	                count_opening = 1
	                count_closing = 0
	                line = self.targetFile.readline()
	                while count_opening > count_closing:
	                    topic = topic + line
	                    if line.find('{') != -1:
	                        count_opening += 1
	                    if line.find('}') != -1:
	                        count_closing += 1
	                    line = self.targetFile.readline()
	                    if count_maximum > 6000:
	                        topic_wrong_syntax.append('O tópico ' + name.getNameTopic() + ' contém número desigual entre chaves de abertura ( { ) e de fechamento ( } )')
	                        break
	                    count_maximum += 1
	                t.setCompleteTopic(topic)
	                t.setNameTopic(name.getNameTopic()[:name.getNameTopic().find(' ')])
	                self.list_all_topics.append(t)
	            line = self.targetFile.readline()
	        self.targetFile.seek(0)
	    return self.list_all_topics