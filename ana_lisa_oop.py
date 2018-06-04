import webbrowser
from topics import Topic
from lists import List
from pendencies import Pendencies
from patterns import Patterns
from errors import Errors
import tkinter as tk
from tkinter import filedialog

def selectFile():
    root = tk.Tk()
    root.withdraw()
    fileName = filedialog.askopenfilename()
    return fileName

def checkNamesAllTopics(targetFile):
    line = targetFile.readline()
    name_all_topics = []
    while line:
        if line.find('topic') != -1 and line.find('{') != -1:
            t = Topic()
            t.setNameTopic(line[line.find('topic'):line.find('{')+1])
            name_all_topics.append(t)
        line = targetFile.readline()
    targetFile.seek(0)
    return name_all_topics

def collectAllTopics(targetFile):
    name_all_topics = checkNamesAllTopics(targetFile)
    list_all_topics = []
    topic_wrong_syntax = []
    for name in name_all_topics:
        line = targetFile.readline()
        while line:
            if line.find(name.getNameTopic()) != -1:
                t = Topic()
                topic = line
                count_maximum = 1
                count_opening = 1
                count_closing = 0
                line = targetFile.readline()
                while count_opening > count_closing:
                    topic = topic + line
                    if line.find('{') != -1:
                        count_opening += 1
                    if line.find('}') != -1:
                        count_closing += 1
                    line = targetFile.readline()
                    if count_maximum > 6000:
                        topic_wrong_syntax.append('O tópico ' + name.getNameTopic() + ' contém número desigual entre chaves de abertura ( { ) e de fechamento ( } )')
                        break
                    count_maximum += 1
                t.setCompleteTopic(topic)
                t.setNameTopic(name.getNameTopic()[:name.getNameTopic().find(' ')])
                list_all_topics.append(t)
            line = targetFile.readline()
        targetFile.seek(0)
    targetFile.seek(0)
    return list_all_topics

def collectOnlyStaticTopics(targetFile):
    list_all_topics = collectAllTopics(targetFile)
    list_static_topics = []
    for t in list_all_topics:
        if 'use topic[' not in t.getCompleteTopic() and 'use *topic[' not in t.getCompleteTopic():
            if 'if' not in t.getCompleteTopic():
                list_static_topics.append(t)
    targetFile.seek(0)
    return list_static_topics

def collectTopicsLargeNumberParagraphs(targetFile):
    list_all_topics = collectAllTopics(targetFile)
    list_topics_large_number_paragraphs = []
    for t in list_all_topics:
        if 'use topic[' not in t.getCompleteTopic() and 'use *topic[' not in t.getCompleteTopic():
            if t.getCompleteTopic().count('\p') > 10:
                list_topics_large_number_paragraphs.append(t)
    targetFile.seek(0)
    return list_topics_large_number_paragraphs

def collectTopicsNotBeingUsed(targetFile):
    name_all_topics = checkNamesAllTopics(targetFile)
    list_topics_not_being_used = []
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
    targetFile.seek(0)
    return list_topics_not_being_used

def collectAllVariablesAndCheckExistenceUnusedStructs(targetFile):

    # Identifica todos os operandos declarados (tipo Struct apenas)
    def collectAllStructs(targetFile, begVariable, endVariable):
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
        targetFile.seek(0)
        return list_DeclaredStructs

    # Identifica operandos (tipo Struct apenas) não operados
    def checkExistenceUnusedStructs(targetFile):
        list_DeclaredStructs = collectAllStructs(targetFile, "+<", "> : ")
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
        targetFile.seek(0)
        return list_UnusedStructs

    list_UnusedStructs = checkExistenceUnusedStructs(targetFile)
    return list_UnusedStructs

def collectAllVariablesAndCheckExistenceUnusedVariables(targetFile):

    # Identifica todos os operandos declarados (tipos primitivos apenas)
    def collectAllVariables(targetFile, begVariable, endVariable):
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
        targetFile.seek(0)
        return list_DeclaredVariables

    # Identifica operandos (tipos primitivos apenas) não structs
    def checkExistenceUnusedVariables(targetFile):
        list_DeclaredVariables = collectAllVariables(targetFile, "+<", "> : ")
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
        targetFile.seek(0)
        return list_UnusedVariables
    list_UnusedVariables = checkExistenceUnusedVariables(targetFile)
    return list_UnusedVariables

def createReport(targetFile, fileName):
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

    shortFileName = ""
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

    pt = Patterns(targetFile)

    list_Names = pt.checkNameSize()
    if len(list_Names) > 0:
        message = message + "<tr><th>NAMES COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Names:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Requests = pt.checkRequestSize()
    if len(list_Requests) > 0:
        message = message + "<tr><th>REQUESTS COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Requests:
            message = message + "<tr><td>" + i + "</td></tr>"

    checkExistenceGrammar = pt.checkExistenceGrammarTube()
    if checkExistenceGrammar == False:
        message = message + "<tr><th>TUBE GRAMMAR()</th></tr> <tr><td>O tube grammar() não foi usado em nenhum momento neste template.</tr></td>"

    list_empty_space_characters = pt.checkExistenceEmptySpaceCharacter()
    if len(list_empty_space_characters) > 0:
        message = message + "<tr><th>LINHAS COM ESPAÇO ESPAÇO VAZIO</th></tr>"
        for i in list_empty_space_characters:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_UnusedVariables = collectAllVariablesAndCheckExistenceUnusedVariables(targetFile)
    list_UnusedStructs = collectAllVariablesAndCheckExistenceUnusedStructs(targetFile)
    list_all_unused_variables_structs = list_UnusedVariables + list_UnusedStructs

    if len(list_all_unused_variables_structs) > 0:
        message = message + "<tr><th>OPERANDOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_all_unused_variables_structs:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_static_topics = collectOnlyStaticTopics(targetFile)
    if len(list_static_topics) > 0:
        message = message + "<tr><th>TÓPICOS ESTÁTICOS (SEM LÓGICA INTERNA)</th></tr>"
        for i in list_static_topics:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    list_topics_large_number_paragraphs = collectTopicsLargeNumberParagraphs(targetFile)
    if len(list_topics_large_number_paragraphs) > 0:
        message = message + "<tr><th>TÓPICOS COM MAIS DE 10 PARÁGRAFOS</th></tr>"
        for i in list_topics_large_number_paragraphs:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    list_topics_not_being_used = collectTopicsNotBeingUsed(targetFile)
    if len(list_topics_not_being_used) > 0:
        message = message + "<tr><th>TÓPICOS NÃO UTILIZADOS NO TEMPLATE</th></tr>"
        for i in list_topics_not_being_used:
            message = message + "<tr><td>" + i.getNameTopic()[:i.getNameTopic().find(']')+1] + "</td></tr>"

    e = Errors(targetFile)
    lists_with_incorrect_syntax = e.checkListsWithIncorrectSyntax()
    if len(lists_with_incorrect_syntax) > 0:
        message = message + "<tr><th>LISTAS COM SINTAXE INCORRETA</th></tr>"
        for i in lists_with_incorrect_syntax:
            message = message + "<tr><td>" + i.getListAlias() + " (lista "
            if i.getTypeList() == True:
                message = message + " atômica) -> uso de sintaxe de lista não atômica identificado na linha "
                for lineNumber in i.getListLineNumber():
                    if i.getListLineNumber().index(lineNumber) == 0:
                        message = message + " " + str(lineNumber)
                    else:
                        message = message + ", " + str(lineNumber)
            elif i.getTypeList() == False:
                message = message + " não atômica) -> uso de sintaxe de lista atômica identificado na linha "
                for lineNumber in i.getListLineNumber():
                    if i.getListLineNumber().index(lineNumber) == 0:
                        message = message + " " + str(lineNumber)
                    else:
                        message = message + ", " + str(lineNumber)
            message = message + "</td></tr>"

    p = Pendencies(fileName, targetFile)

    list_Fixmes = p.checkExistenceFixmes()
    if len(list_Fixmes) > 0:
        message = message + "<tr><th>FIXMEs</th></tr>"
        for i in list_Fixmes:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Todos = p.checkExistenceTodos()
    if len(list_Todos) > 0:
        message = message + "<tr><th>TODOs</th></tr>"
        for i in list_Todos:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_comments = p.checkExistenceComment()
    if len(list_comments) > 0:
        message = message + "<tr><th>COMENTÁRIOS</th></tr>"
        for c in list_comments:
            message = message + "<tr><td>Linha " + str(c.getLineNumberBegComment()) + ": " + c.getCompleteComment() + "</tr></td>"

    list_unfinished_prints = p.checkExistenceUnfinishedPrints()
    if len(list_unfinished_prints) > 0:
        message = message + "<tr><th>PRINTS NÃO FINALIZADOS</th></tr>"
        for i in list_unfinished_prints:
            message = message + "<tr><td>" + i + "</td></tr>"

    if p.checkExistenceStatements() == False:
        message = message + "<tr><th>STATEMENT OF WORK</th></tr> <tr><td>Neste template não há statement of work.</td></tr>"

    if p.checkExistenceReadmeFile() == True:
        message = message + "<tr><th>README</th></tr> <tr><td>Não foi criado um arquivo README.txt para este template.</td></tr>"

    message = message + """</table></body></html>"""
    f.write(message)
    f.close()
    webbrowser.open_new_tab('Relatorio.html')

fileName = selectFile()
targetFile = open(fileName, "r", encoding="utf-8")
createReport(targetFile, fileName)
targetFile.close()