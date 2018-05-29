# ( ) Uso de estruturas globais
# ( ) Uso de constantes
# ( ) Uso de flags de preliminares
# ( ) Uso de estruturas muito conhecidas
# ( ) Uso de estrutura mínima de um frame
# ( ) Identifica listas nao atômicas com sintaxe de lista atômica e vice-versa
# ( ) Análise do português
# ( ) Detectar uso de frases ou expressões em português que possam diminuir a qualidade do texto. Pensar na criação de um arquivo com lista de expressões não recomendadas
# ( ) Detectar integers que possam causar problemas caso sejam usados para criar vetores
# ( ) Criar mecanismo no arquivos HTML para permitir que o usuário faça alterações no próprio código quando necessário
# (X) Uso de statement of work
# (X) Identificar existência de TODO
# (X) Identificar existência de FIXME
# (X) Verificar se o número de caracteres nos names e requests não ultrapasse 100
# (X) Identifica a existência de codigo comentado
# (X) Identifica operandos declarados, mas não operados
# (X) Identifica a existência ou não de README

from comments import Comment
from topics import Topic

fileName = ""

# Abre possibilidade para que usuário selecione um arquivo
def selectFile():
    global fileName
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    fileName = filedialog.askopenfilename()

# Verifica se há names com número de caracteres que sejam maiores que 100
def checkNameSize(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    list_Names = []
    name = "name = "
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(name) != -1:
            nameUnderAnalysis = line[line.find(name)+7:len(line)-1]
            if (len(nameUnderAnalysis) > 100):
                redFlag = ("Linha " + str(count) + ": " + nameUnderAnalysis)
                list_Names.append(redFlag)
        line = targetFile.readline()
        count = count + 1
    targetFile.close()
    return list_Names

# Verifica se há requests com número de caracteres que sejam maiores que 100
def checkRequestSize(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    list_Requests = []
    request = "request = "
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(request) != -1:
            requestUnderAnalysis = line[line.find(request)+10:len(line)-1]
            if (len(requestUnderAnalysis) > 100):
                redFlag = "Linha " + str(count) + ": " + requestUnderAnalysis
                list_Requests.append(redFlag)
        line = targetFile.readline()
        count = count + 1
    targetFile.close()
    return list_Requests

# Identifica a existência de FIXMEs
def checkExistenceFixmes(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    list_Fixmes = []
    fixme = "FIXME"
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(fixme) != -1:
            fixmeUnderAnalysis = line[line.find(fixme)+6:len(line)]
            redFlag = "Linha " + str(count) + ":" + fixmeUnderAnalysis
            list_Fixmes.append(redFlag)
        line = targetFile.readline()
        count = count + 1
    targetFile.close()
    return list_Fixmes

# Identifica o nome de todos os tópicos no template
def checkNamesAllTopics(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    line = targetFile.readline()
    name_all_topics = []
    while line:
        if line.find('topic') != -1 and line.find('{') != -1:
            t = Topic()
            t.setNameTopic(line[line.find('topic'):line.find('{')+1])
            name_all_topics.append(t)
        line = targetFile.readline()
    targetFile.close()
    return name_all_topics

# Coleta todos os tópicos no template
def collectAllTopics(fileName):
    name_all_topics = checkNamesAllTopics(fileName)
    targetFile = open(fileName, "r", encoding="utf-8")
    list_all_topics = []
    for name in name_all_topics:
        line = targetFile.readline()
        while line:
            if line.find(name.getNameTopic()) != -1:
                t = Topic()
                topic = line
                count_opening = 1
                count_closing = 0
                line = targetFile.readline()
                while count_opening > count_closing:
                    topic = topic + line
                    if line.find('{') != -1 and line.find('}') == -1:
                        count_opening += 1
                    elif line.find('{') == -1 and line.find('}') != -1:
                        count_closing += 1
                    elif line.find('{') != -1 and line.find('}') != -1:
                        count_opening += 1
                        count_closing += 1
                    line = targetFile.readline()
                t.setCompleteTopic(topic)
                t.setNameTopic(name.getNameTopic()[:name.getNameTopic().find(' ')])
                list_all_topics.append(t)
            line = targetFile.readline()
        targetFile.seek(0)
    targetFile.close()
    return list_all_topics

# Coleta apenas os tópicos estáticos
def collectOnlyStaticTopics(fileName):
    list_all_topics = collectAllTopics(fileName)
    list_static_topics = []
    for t in list_all_topics:
        if 'if' not in t.getCompleteTopic():
            list_static_topics.append(t)
    return list_static_topics

# Coleta os tópicos com grande quantidade de parágrafos
def collectTopicsLargeNumberParagraphs(fileName):
    list_all_topics = collectAllTopics(fileName)
    list_topics_large_number_paragraphs = []
    for t in list_all_topics:
        if t.getCompleteTopic().count('\p') > 10:
            list_topics_large_number_paragraphs.append(t)
    return list_topics_large_number_paragraphs

# Coleta todos os tópicos não operados
def collectTopicsNotBeingUsed(fileName):
    name_all_topics = checkNamesAllTopics(fileName)
    list_topics_not_being_used = []
    targetFile = open(fileName, "r", encoding = "utf-8")
    for t in name_all_topics:
        count = 0
        line = targetFile.readline()
        while line:
            if line.find(t.getNameTopic()[:t.getNameTopic().find(']')+1]) != -1:
                count += 1
            line = targetFile.readline()
        if count == 1:
            list_topics_not_being_used.append(t)
        targetFile.seek(0)
    targetFile.close()
    return list_topics_not_being_used

# Identifica a existência de TODO
def checkExistenceTodos(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    list_Todos = []
    todo = "// TODO"
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(todo) != -1:
            todoUnderAnalysis = line[line.find(todo)+7:len(line)]
            redFlag = "Linha " + str(count) + ": " + todoUnderAnalysis
            list_Todos.append(redFlag)
        line = targetFile.readline()
        count = count + 1
    targetFile.close()
    return list_Todos

# Identifica a existência de prints não finalizados
def checkExistenceUnfinishedPrints(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    list_unfinished_prints = []
    unfinished_prints = "print \"\""
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(unfinished_prints) != -1:
            redFlag = "Linha " + str(count)
            list_unfinished_prints.append(redFlag)
        line = targetFile.readline()
        count = count + 1
    targetFile.close()
    return list_unfinished_prints

# Identifica a existência do tube Grammar()
def checkExistenceGrammarTube(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    checkExistenceGrammar = False
    grammar = "grammar("
    line = targetFile.readline()
    while line:
        if line.find(grammar) != -1:
            checkExistenceGrammar = True
        line = targetFile.readline()
    targetFile.close()
    return checkExistenceGrammar

# Identifica a existência de código comentado
def checkExistenceComment(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    lineNumber = 1
    idx_beg_comment = "/*"
    idx_end_comment = "*/"
    list_comments = []
    comment = ""
    line = targetFile.readline()
    while line:
        if line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) != -1:
            c = Comment()
            c.setLineNumberBegComment(lineNumber)
            c.setCompleteComment(line[line.find(idx_beg_comment)+2:line.find(idx_end_comment)])
            list_comments.append(c)
            lineNumber = lineNumber + 1
        elif line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) == -1:
            c = Comment()
            c.setLineNumberBegComment(lineNumber)
            while line.find(idx_end_comment) == -1:
                comment = comment + line
                line = targetFile.readline()
                lineNumber = lineNumber + 1
            comment = comment + line # Última linha do comentário
            c.setCompleteComment(comment)
            list_comments.append(c)
        else:
            lineNumber = lineNumber + 1
        line = targetFile.readline()
        comment = ""
    targetFile.close()
    return list_comments

# Identifica a existência de statement no template
def checkExistenceStatements(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    checkExistenceStatement = False
    statement = "Statement"
    line = targetFile.readline()
    while line:
        if line.find(statement) != -1:
            checkExistenceStatement = True
        line = targetFile.readline()
    targetFile.close()
    return checkExistenceStatement

# Identifica operandos declarados, mas não operados
def collectAllVariablesAndCheckExistenceUnusedStructs(fileName):

    # Identifica todos os operandos declarados (tipo Struct apenas)
    def collectAllStructs(fileName, begVariable, endVariable):
        targetFile = open(fileName, "r", encoding="utf-8")
        list_DeclaredStructs = []
        begVariable = begVariable
        endVariable = endVariable
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
        line = targetFile.readline()
        while line:
            if line.find(begVariable) != -1:
                if (line.find(ti) == -1 and line.find(te) == -1 and line.find(cu) == -1 and line.find(re) == -1 and line.find(bo) == -1 and line.find(li) == -1 and line.find(st) == -1 and line.find(da) == -1 and line.find(i) == -1):
                    idxBegVariable = line.find(begVariable)
                    idxEndVariable = line.find(endVariable)
                    list_DeclaredStructs.append(line[idxBegVariable+2:idxEndVariable])
            line = targetFile.readline()
        targetFile.close()
        return list_DeclaredStructs

    # Identifica operandos (tipo Struct apenas) não operados
    def checkExistenceUnusedStructs(fileName):
        list_DeclaredStructs = collectAllStructs(fileName, "+<", "> : ")
        targetFile = open(fileName, "r", encoding="utf-8")
        list_UnusedStructs = []
        for u in list_DeclaredStructs:
            count = 0
            line = targetFile.readline()
            while line:
                if line.find(u + ".") != -1:
                    count = count + 1
                line = targetFile.readline()
            if count == 0:
                list_UnusedStructs.append(u)
            targetFile.seek(0)
        targetFile.close()
        return list_UnusedStructs

    list_UnusedStructs = checkExistenceUnusedStructs(fileName)
    return list_UnusedStructs

# Identifica operandos declarados, mas não operados
def collectAllVariablesAndCheckExistenceUnusedVariables(fileName):

    # Identifica todos os operandos declarados (tipos primitivos apenas)
    def collectAllVariables(fileName, begVariable, endVariable):
        targetFile = open(fileName, "r", encoding="utf-8")
        list_DeclaredVariables = []
        begVariable = begVariable
        endVariable = endVariable
        idxBegVariable = 0
        idxEndVariable = 0
        line = targetFile.readline()
        while line:
            if line.find(begVariable) != -1:
                if (line.find('*') == -1 and line.find('struct') == -1):
                    idxBegVariable = line.find(begVariable)
                    idxEndVariable = line.find(endVariable)
                    list_DeclaredVariables.append(line[idxBegVariable+2:idxEndVariable])
            line = targetFile.readline()
        targetFile.close()
        return list_DeclaredVariables

    # Identifica operandos (tipos primitivos apenas) não structs
    def checkExistenceUnusedVariables(fileName):
        list_DeclaredVariables = collectAllVariables(fileName, "+<", "> : ")
        targetFile = open(fileName, "r", encoding="utf-8")
        list_UnusedVariables = []
        for u in list_DeclaredVariables:
            count = 0
            line = targetFile.readline()
            while line:
                if line.find(u) != -1:
                    count = count + 1
                line = targetFile.readline()
            if count == 1:
                list_UnusedVariables.append(u)
            targetFile.seek(0)
        targetFile.close()
        return list_UnusedVariables
    list_UnusedVariables = checkExistenceUnusedVariables(fileName)
    return list_UnusedVariables

# Verifica se foi criado arquivo README
def checkExistenceReadmeFile(fileName):
    readmeFileDoesNotExists = False
    if fileName.find("TEMP_") != -1:
        filePath = fileName[:fileName.find("TEMP_")]
    elif fileName.find("FRM_") != -1:
        filePath = fileName[:fileName.find("FRM_")]
    elif fileName.find("NODES_") != -1:
        filePath = fileName[:fileName.find("NODES_")]
    elif fileName.find("STRC_") != -1:
        filePath = fileName[:fileName.find("STRC_")]
    import os.path
    my_file = filePath + "README.txt"
    if os.path.isfile(my_file) == False:
        readmeFileDoesNotExists = True
    return readmeFileDoesNotExists

# Criação de arquivo HTML com relatório das informações relevantes
def createReport():
    import webbrowser
    global fileName
    f = open('Relatorio.html','w')

    message = """
            <html> <head>
            <style>
            #relatorio {
                font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            #relatorio td, #relatorio th {
                border: 1px solid #ddd;
                padding: 8px;
            }
            #relatorio tr:nth-child(even){background-color: #f2f2f2;}
            #relatorio tr:hover {background-color: #ddd;}
            #relatorio th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: #ff1a1a;
                color: white;
            }
            </style>
            </head> <body> <center><bold><h2>ANÁLISE DO TEMPLATE - """

    if fileName.find("TEMP_") != -1:
        shortFileName = fileName[fileName.find("TEMP_"):len(fileName)]
    elif fileName.find("FRM_") != -1:
        shortFileName = fileName[fileName.find("FRM_"):len(fileName)]
    elif fileName.find("NODES_") != -1:
        shortFileName = fileName[fileName.find("NODES_"):len(fileName)]
    elif fileName.find("STRC_") != -1:
        shortFileName = fileName[fileName.find("STRC_"):len(fileName)]
    message = message + shortFileName + """</h2></bold></center>"""

    message = message + """<br><br><table id="relatorio">"""

    list_Names = checkNameSize(fileName)
    if len(list_Names) > 0:
        message = message + "<tr><th>NAMES COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Names:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Requests = checkRequestSize(fileName)
    if len(list_Requests) > 0:
        message = message + "<tr><th>REQUESTS COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Requests:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Fixmes = checkExistenceFixmes(fileName)
    if len(list_Fixmes) > 0:
        message = message + "<tr><th>FIXMEs</th></tr>"
        for i in list_Fixmes:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Todos = checkExistenceTodos(fileName)
    if len(list_Todos) > 0:
        message = message + "<tr><th>TODOs</th></tr>"
        for i in list_Todos:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_unfinished_prints = checkExistenceUnfinishedPrints(fileName)
    if len(list_unfinished_prints) > 0:
        message = message + "<tr><th>PRINTS NÃO FINALIZADOS</th></tr>"
        for i in list_unfinished_prints:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_UnusedVariables = collectAllVariablesAndCheckExistenceUnusedVariables(fileName)
    list_UnusedStructs = collectAllVariablesAndCheckExistenceUnusedStructs(fileName)
    list_all_unused_variables_structs = list_UnusedVariables + list_UnusedStructs

    if len(list_all_unused_variables_structs) > 0:
        message = message + "<tr><th>OPERANDOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_all_unused_variables_structs:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_comments = checkExistenceComment(fileName)
    if len(list_comments) > 0:
        message = message + "<tr><th>COMENTÁRIOS</th></tr>"
        for c in list_comments:
            message = message + "<tr><td>Linha " + str(c.getLineNumberBegComment()) + ": " + c.getCompleteComment() + "</tr></td>"

    list_static_topics = collectOnlyStaticTopics(fileName)
    if len(list_static_topics) > 0:
        message = message + "<tr><th>TÓPICOS ESTÁTICOS (SEM LÓGICA INTERNA)</th></tr>"
        for i in list_static_topics:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    list_topics_large_number_paragraphs = collectTopicsLargeNumberParagraphs(fileName)
    if len(list_topics_large_number_paragraphs) > 0:
        message = message + "<tr><th>TÓPICOS COM MAIS DE 10 PARÁGRAFOS</th></tr>"
        for i in list_topics_large_number_paragraphs:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    list_topics_not_being_used = collectTopicsNotBeingUsed(fileName)
    if len(list_topics_not_being_used) > 0:
        message = message + "<tr><th>TÓPICOS NÃO UTILIZADOS NO TEMPLATE</th></tr>"
        for i in list_topics_not_being_used:
            message = message + "<tr><td>" + i.getNameTopic()[:i.getNameTopic().find(']')+1] + "</td></tr>"

    if checkExistenceGrammarTube(fileName) == False:
        message = message + "<tr><th>TUBE GRAMMAR()</th></tr> <tr><td>O tube grammar() não foi usado em nenhum momento neste template.</tr></td>"

    if checkExistenceStatements(fileName) == False:
        message = message + "<tr><th>STATEMENT OF WORK</th></tr> <tr><td>Neste template não há statement of work.</td></tr>"

    if checkExistenceReadmeFile(fileName) == True:
        message = message + "<tr><th>README</th></tr> <tr><td>Não foi criado um arquivo README.txt para este template.</td></tr>"

    message = message + """</table></body></html>"""
    f.write(message)
    f.close()
    webbrowser.open_new_tab('Relatorio.html')

selectFile()
createReport()