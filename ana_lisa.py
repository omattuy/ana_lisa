# ( ) Uso de estruturas globais
# ( ) Uso de constantes
# ( ) Uso de flags de preliminares
# ( ) Uso de estruturas muito conhecidas
# ( ) Uso de estrutura mínima de um frame
# ( ) Identifica listas nao atômicas com sintaxe de lista atômica e vice-versa
# ( ) Análise do português
# ( ) Detectar uso de frases ou expressões em português que possam diminuir a qualidade do texto. Pensar na criação de um arquivo com lista de expressões não recomendadas
# ( ) Detectar integers que possam causar problemas caso sejam usados para criar vetores
# (X) Uso de statement of work
# (X) Identificar existência de TODO
# (X) Identificar existência de FIXME
# (X) Verificar se o número de caracteres nos names e requests não ultrapasse 100
# (X) Identifica a existência de codigo comentado
# (X) Identifica operandos declarados, mas não operados
# (X) Identifica a existência ou não de README

from comments import Comment

fileName = ""
list_Names = []
list_Requests = []
list_Fixmes = []
list_Todos = []
list_DeclaredVariables = []
list_UnusedVariables = []
checkExistenceLargeName = False
checkExistenceLargeRequest = False
checkExistenceFixme = False
checkExistenceTodo = False
checkExistenceGrammar = False
checkExistenceComment = False
checkExistenceStatement = False
checkExistenceUnusedVariable = False
readmeFileDoesNotExists = False
checkExistenceTopic = False
countComments = 0

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
    global list_Names
    global checkExistenceLargeName
    name = "name = "
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(name) != -1:
            nameUnderAnalysis = line[line.find(name)+7:len(line)-1]
            if (len(nameUnderAnalysis) > 100):
                redFlag = ("Linha " + str(count) + ": " + nameUnderAnalysis)
                list_Names.append(redFlag)
                checkExistenceLargeName = True
        line = targetFile.readline()
        count = count + 1
    targetFile.close()

# Verifica se há requests com número de caracteres que sejam maiores que 100
def checkRequestSize(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceLargeRequest
    global list_Requests
    request = "request = "
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(request) != -1:
            requestUnderAnalysis = line[line.find(request)+10:len(line)-1]
            if (len(requestUnderAnalysis) > 100):
                redFlag = "Linha " + str(count) + ": " + requestUnderAnalysis
                list_Requests.append(redFlag)
                checkExistenceLargeRequest = True
        line = targetFile.readline()
        count = count + 1
    targetFile.close()

# Identifica a existência de FIXMEs
def checkExistenceFixmes(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceFixme
    global list_Fixmes
    fixme = "FIXME"
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(fixme) != -1:
            fixmeUnderAnalysis = line[line.find(fixme)+6:len(line)]
            redFlag = "Linha " + str(count) + ":" + fixmeUnderAnalysis
            list_Fixmes.append(redFlag)
            checkExistenceFixme = True
        line = targetFile.readline()
        count = count + 1
    targetFile.close()

# Identifica a existência de TODO
def checkExistenceTodos(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceTodo
    global list_Todos
    todo = "// TODO"
    line = targetFile.readline()
    count = 1
    while line:
        if line.find(todo) != -1:
            todoUnderAnalysis = line[line.find(todo)+7:len(line)]
            redFlag = "Linha " + str(count) + ":" + todoUnderAnalysis
            list_Todos.append(redFlag)
            checkExistenceTodo = True
        line = targetFile.readline()
        count = count + 1
    targetFile.close()

# Identifica a existência do tube Grammar()
def checkExistenceGrammarTube(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceGrammar
    grammar = "grammar("
    line = targetFile.readline()
    while line:
        if line.find(grammar) != -1:
            checkExistenceGrammar = True
        line = targetFile.readline()
    targetFile.close()

# Identifica a existência de codigo comentado
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
            c.setCompleteComment(line[line.find(idx_beg_comment)+2:line.find(idx_end_comment)])
            list_comments.append(c)
            lineNumber = lineNumber + 1
        elif line.find(idx_beg_comment) != -1 and line.find(idx_end_comment) == -1:
            c = Comment()
            c.setLineNumberBegComment(lineNumber)
            print('Teste: ', str(c.getLineNumberBegComment()))
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

# Identifica a existência de statement no template
def checkExistenceStatements(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceStatement
    statement = "Statement"
    line = targetFile.readline()
    while line:
        if line.find(statement) != -1:
            checkExistenceStatement = True
        line = targetFile.readline()
    targetFile.close()

# Identifica operandos declarados, mas não operados
def collectAllVariablesAndCheckExistenceUnusedVariables(fileName):

    # Identifica todos os operandos declarados (tipo Struct apenas)
    def collectAllVariables(fileName):
        targetFile = open(fileName, "r", encoding="utf-8")
        global list_DeclaredVariables
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
        line = targetFile.readline()
        while line:
            if line.find(begVariable) != -1:
                if (line.find(ti) == -1 and line.find(te) == -1 and line.find(cu) == -1 and line.find(re) == -1 and line.find(bo) == -1 and line.find(li) == -1 and line.find(st) == -1 and line.find(da) == -1 and line.find(i) == -1):
                    idxBegVariable = line.find(begVariable)
                    idxEndVariable = line.find(endVariable)
                    list_DeclaredVariables.append(line[idxBegVariable+2:idxEndVariable])
            line = targetFile.readline()
        targetFile.close()

    # Identifica operandos (tipo Struct apenas) não operados
    def checkExistenceUnusedVariables(fileName):
        targetFile = open(fileName, "r", encoding="utf-8")
        global list_UnusedVariables
        global list_DeclaredVariables
        for u in list_DeclaredVariables:
            count = 0
            line = targetFile.readline()
            while line:
                if line.find(u + ".") != -1:
                    count = count + 1
                line = targetFile.readline()
            if count == 0:
                list_UnusedVariables.append(u)
            targetFile.seek(0)
        targetFile.close()

    collectAllVariables(fileName)
    checkExistenceUnusedVariables(fileName)

# Verifica se foi criado arquivo README
def checkExistenceReadmeFile(fileName):
    if fileName.find("TEMP_") != -1:
        filePath = fileName[:fileName.find("TEMP_")]
    elif fileName.find("FRM_") != -1:
        filePath = fileName[:fileName.find("FRM_")]
    import os.path
    my_file = filePath + "README.txt"
    global readmeFileDoesNotExists
    if os.path.isfile(my_file) == False:
        readmeFileDoesNotExists = True

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
            </head> <body> <center><bold><h2>ANÁLISE DO TEMPLATE 
            """

    if fileName.find("TEMP_") != -1:
        shortFileName = fileName[fileName.find("TEMP_"):len(fileName)]
    elif fileName.find("FRM_") != -1:
        shortFileName = fileName[fileName.find("FRM_"):len(fileName)]
    message = message + shortFileName + """</h2></bold></center>"""
    message = message + """<br><br><table id="relatorio">"""

    if checkExistenceLargeName == True:
        message = message + "<tr><th>NAMES COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Names:
            message = message + "<tr><td>" + i + "</td></tr>"

    if checkExistenceLargeRequest == True:
        message = message + "<tr><th>REQUESTS COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Requests:
            message = message + "<tr><td>" + i + "</td></tr>"

    if checkExistenceFixme == True:
        message = message + "<tr><th>FIXMEs</th></tr>"
        for i in list_Fixmes:
            message = message + "<tr><td>" + i + "</td></tr>"

    if checkExistenceTodo == True:
        message = message + "<tr><th>TODOs</th></tr>"
        for i in list_Todos:
            message = message + "<tr><td>" + i + "</td></tr>"

    if len(list_UnusedVariables) > 0:
        message = message + "<tr><th>OPERANDOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_UnusedVariables:
            message = message + "<tr><td>" + i + "</td></tr>"

    if checkExistenceComment == True:
        message = message + "<tr><th>COMENTÁRIOS</th></tr> <tr><td>Este template contém " + str(countComments) + " trechos de código comentado.<tr><td>"

    if checkExistenceGrammar == False:
        message = message + "<tr><th>GRAMMAR</th></tr> <tr><td>O tube grammar() não foi usado em nenhum momento neste template.</tr></td>"

    if checkExistenceStatement == False:
        message = message + "<tr><th>STATEMENT OF WORK</th></tr> <tr><td>Neste template não há statement of work.</td></tr>"

    if readmeFileDoesNotExists == True:
        message = message + "<tr><th>README</th></tr> <tr><td>Não foi criado um arquivo README.txt para este template.</td></tr>"

    message = message + """</table></body></html>"""

    f.write(message)
    f.close()
    webbrowser.open_new_tab('Relatorio.html')

selectFile()
#checkNameSize(fileName)
#checkRequestSize(fileName)
#checkExistenceFixmes(fileName)
#checkExistenceTodos(fileName)
#checkExistenceGrammarTube(fileName)
checkExistenceComment(fileName)
#checkExistenceStatements(fileName)
#collectAllVariablesAndCheckExistenceUnusedVariables(fileName)
#checkExistenceReadmeFile(fileName)
createReport()