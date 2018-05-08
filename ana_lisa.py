# ( ) Uso de estruturas globais
# ( ) Uso de constantes
# ( ) Uso de flags de preliminares
# ( ) Uso de estruturas muito conhecidas
# ( ) Uso de estrutura mínima de um frame
# (X) Uso de statement of work
# (X) Identificar existência de TODO
# (X) Identificar existência de FIXME
# (X) Verificar se o número de caracteres nos names e requests não ultrapasse 100
# (X) Identifica a existência de codigo comentado
# (X) Identifica operandos declarados, mas não operados
# ( ) Identifica listas nao atômicas com sintaxe de lista atômica e vice-versa
# ( ) Identifica a existência ou nao de README


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
    nameUnderAnalysis = ""
    redFlag = ""
    line = targetFile.readline()
    count = 1
    while line:
        if (line.find(name) != -1):
            nameUnderAnalysis = line[line.find(name)+6:len(line)]
            if (len(nameUnderAnalysis) > 100):
                redFlag = ("Linha " + str(count) + ":" + nameUnderAnalysis)
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
    requestUnderAnalysis = ""
    redFlag = ""
    line = targetFile.readline()
    count = 1
    while line:
        if (line.find(request) != -1):
            requestUnderAnalysis = line[line.find(request)+10:len(line)]
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
    redFlag = ""
    fixme = "FIXME"
    fixmeUnderAnalysis = ""
    line = targetFile.readline()
    count = 1
    while line:
        if (line.find(fixme) != -1):
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
    redFlag = ""
    todo = "// TODO"
    todoUnderAnalysis = ""
    line = targetFile.readline()
    count = 1
    while line:
        if (line.find(todo) != -1):
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
    grammar = "grammar"
    line = targetFile.readline()
    while line:
        if (line.find(grammar) != -1):
            checkExistenceGrammar = True
        line = targetFile.readline()
    targetFile.close()

# Identifica a existência de codigo comentado
def checkExistenceComment(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceComment
    global countComments
    comment = "/*"
    line = targetFile.readline()
    while line:
        if (line.find(comment) != -1):
            countComments = countComments + 1
            checkExistenceComment = True
        line = targetFile.readline()
    targetFile.close()

# Identifica a existência de statement no template
def checkExistenceStatements(fileName):
    targetFile = open(fileName, "r", encoding="utf-8")
    global checkExistenceStatement
    statement = "Statement"
    line = targetFile.readline()
    while line:
        if (line.find(statement) != -1):
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
        idxBegVariable = 0
        idxEndVariable = 0
        line = targetFile.readline()
        while line:
            if (line.find(begVariable) != -1):
                if (line.find(te) == -1 and line.find(cu) == -1 and line.find(re) == -1 and line.find(bo) == -1 and line.find(li) == -1 and line.find(st) == -1 and line.find(da) == -1 and line.find(i) == -1):
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
                if (line.find(u + ".") != -1):
                    count = count + 1
                line = targetFile.readline()
            if (count == 0):
                list_UnusedVariables.append(u)
            targetFile.seek(0)
        targetFile.close()

    collectAllVariables(fileName)
    checkExistenceUnusedVariables(fileName)

# Identifica a existência de listas atômicas com sintaxe incorreta



# Verifica se foi criado arquivo README
def checkExistenceReadmeFile(fileName):
    filePath = fileName[:fileName.find("TEMP")]
    import os.path
    my_file = filePath + "README"
    if (os.path.isfile(my_file)):
        print ("README existe")
    else:
        print ("README não existe")







    



# Criação de arquivo HTML com relatório das informações relevantes
def createReport():
    import webbrowser
    global fileName
    shortFileName = ""
    f = open('Relatorio.html','w')

    message = """<html> <head>
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

            </head> <body> <center><bold><h2>ANÁLISE DO TEMPLATE """
    shortFileName = fileName[fileName.find("TEMP"):len(fileName)]
    message = message + shortFileName + """</h2></bold></center>"""
    message = message + """<br><br><table id="relatorio">"""

    if (checkExistenceLargeName == True):
        message = message + "<tr><th>NAMES COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Names:
            message = message + "<tr><td>" + i + "</td></tr>"

    if (checkExistenceLargeRequest == True):
        message = message + "<tr><th>REQUESTS COM MAIS DO QUE 100 CARACTERES</th></tr>"
        for i in list_Requests:
            message = message + "<tr><td>" + i + "</td></tr>"

    if (checkExistenceFixme == True):
        message = message + "<tr><th>FIXMEs</th></tr>"
        for i in list_Fixmes:
            message = message + "<tr><td>" + i + "</td></tr>"

    if (checkExistenceTodo == True):
        message = message + "<tr><th>TODOs</th></tr>"
        for i in list_Todos:
            message = message + "<tr><td>" + i + "</td></tr>"

    if (len(list_UnusedVariables) > 0):
        message = message + "<tr><th>OPERANDOS DECLARADOS, MAS NÃO OPERADOS</th></tr>"
        for i in list_UnusedVariables:
            message = message + "<tr><td>" + i + "</td></tr>"

    if (checkExistenceComment == True):
        message = message + "<tr><th>COMENTÁRIOS</th></tr> <tr><td>Este template contém " + str(countComments) + " trechos de código comentado.<tr><td>"

    if (checkExistenceGrammar == False):
        message = message + "<tr><th>GRAMMAR</th></tr> <tr><td>O tube grammar() não foi usado em nenhum momento neste template.</tr></td>"

    if (checkExistenceStatement == False):
        message = message + "<tr><th>STATEMENT OF WORK</th></tr> <tr><td>Neste template não há statement of work.</td></tr>"

    message = message + """</table></body></html>"""

    f.write(message)
    f.close()
    webbrowser.open_new_tab('Relatorio.html')

selectFile()
checkNameSize(fileName)
checkRequestSize(fileName)
#checkExistenceFixmes(fileName)
checkExistenceTodos(fileName)
checkExistenceGrammarTube(fileName)
checkExistenceComment(fileName)
checkExistenceStatements(fileName)
collectAllVariablesAndCheckExistenceUnusedVariables(fileName)
checkExistenceReadmeFile(fileName)
createReport()
