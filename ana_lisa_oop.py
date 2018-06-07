import webbrowser
from comments import Comment # TODO - confirmar se é necessário importar aqui e não apenas em pendencies.py
from topics import Topic # TODO - confirmar se é necessário importar aqui e não apenas em topicanalysis.py
from lists import List
from patterns import Patterns
from pendencies import Pendencies
from errors import Errors
import tkinter as tk
from tkinter import filedialog
import os.path # TODO - confirmar se é necessário importar aqui e não apenas em patterns.py

def selectFile():
    root = tk.Tk()
    root.withdraw()
    fileName = filedialog.askopenfilename()
    return fileName

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

    # PADRÕES
    pt = Patterns(targetFile, fileName)

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

    if pt.checkExistenceGrammarTube() == False:
        message = message + "<tr><th>TUBE GRAMMAR()</th></tr> <tr><td>O tube grammar() não foi usado em nenhum momento neste template.</tr></td>"

    if pt.checkExistenceStatements() == False:
        message = message + "<tr><th>STATEMENT OF WORK</th></tr> <tr><td>Neste template não há statement of work.</td></tr>"

    if pt.checkExistenceReadmeFile() == True:
        message = message + "<tr><th>README</th></tr> <tr><td>Não foi criado um arquivo README.txt para este template.</td></tr>"

    list_empty_space_characters = pt.checkExistenceEmptySpaceCharacter()
    if len(list_empty_space_characters) > 0:
        message = message + "<tr><th>LINHAS COM ESPAÇO ESPAÇO VAZIO</th></tr>"
        for i in list_empty_space_characters:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_static_topics = pt.collectOnlyStaticTopics()
    if len(list_static_topics) > 0:
        message = message + "<tr><th>TÓPICOS ESTÁTICOS (SEM LÓGICA INTERNA)</th></tr>"
        for i in list_static_topics:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    list_topics_large_number_paragraphs = pt.collectTopicsLargeNumberParagraphs()
    if len(list_topics_large_number_paragraphs) > 0:
        message = message + "<tr><th>TÓPICOS COM MAIS DE 10 PARÁGRAFOS</th></tr>"
        for i in list_topics_large_number_paragraphs:
            message = message + "<tr><td>" + i.getNameTopic() + "</td></tr>"

    # PENDÊNCIAS
    pd = Pendencies(targetFile)

    list_Fixmes = pd.checkExistenceFixmes()
    if len(list_Fixmes) > 0:
        message = message + "<tr><th>FIXMEs</th></tr>"
        for i in list_Fixmes:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_Todos = pd.checkExistenceTodos()
    if len(list_Todos) > 0:
        message = message + "<tr><th>TODOs</th></tr>"
        for i in list_Todos:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_unfinished_prints = pd.checkExistenceUnfinishedPrints()
    if len(list_unfinished_prints) > 0:
        message = message + "<tr><th>PRINTS NÃO FINALIZADOS</th></tr>"
        for i in list_unfinished_prints:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_comments = pd.checkExistenceComment()
    if len(list_comments) > 0:
        message = message + "<tr><th>COMENTÁRIOS</th></tr>"
        for c in list_comments:
            message = message + "<tr><td>Linha " + str(c.getLineNumberBegComment()) + ": " + c.getCompleteComment() + "</tr></td>"

    list_UnusedVariables = pd.collectAllVariablesAndCheckExistenceUnusedVariables()
    list_UnusedStructs = pd.collectAllVariablesAndCheckExistenceUnusedStructs()
    list_all_unused_variables_structs = list_UnusedVariables + list_UnusedStructs

    if len(list_all_unused_variables_structs) > 0:
        message = message + "<tr><th>OPERANDOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_all_unused_variables_structs:
            message = message + "<tr><td>" + i + "</td></tr>"

    list_topics_not_being_used = pd.collectTopicsNotBeingUsed()
    if len(list_topics_not_being_used) > 0:
        message = message + "<tr><th>TÓPICOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_topics_not_being_used:
            message = message + "<tr><td>" + i.getNameTopic()[:i.getNameTopic().find(']')+1] + "</td></tr>"

    # ERROS
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

    message = message + """</table></body></html>"""
    f.write(message)
    f.close()
    webbrowser.open_new_tab('Relatorio.html')

fileName = selectFile()
targetFile = open(fileName, "r", encoding = "utf-8")
createReport(targetFile, fileName)
targetFile.close()