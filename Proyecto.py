import sys
import os

indicador = 0

#######################################
#####                             #####
#####    Analizador sintáctico    #####
#####                             #####
#######################################

#Errores
def error():
    print("\nError en la linea " + str(globalLin[indicador-1]))
    print("No se esperaba el token " + globalTokens[indicador] + '\n')
    sys.exit(1)


#Ejecución del analizado sintáctico
def program():
    global indicador
    declaration()
    if globalTokens[indicador] == 'EOF':
        pass
    else:
        error()

#Declaraciones---------------------------------------------
def declaration():
    if class_decl():
        declaration()
    elif fun_decl():
        declaration()
    elif var_decl():
        declaration()
    elif statement():
        declaration()
    else: pass
        
def class_decl():
    global indicador
    if globalTokens[indicador] == 'CLASS':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if class_inher():
                if globalTokens[indicador] == '{':
                    indicador += 1
                    if functions():
                        if globalTokens[indicador] == '}':
                            indicador += 1
                            return True
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def class_inher():
    global indicador
    if globalTokens[indicador] == '<':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            return True
        else: error()
    else: return True

def fun_decl():
    global indicador
    if globalTokens[indicador] == 'FUN':
        indicador += 1
        if funct(): return True
    else: return False

def var_decl():
    global indicador
    if globalTokens[indicador] == 'VAR':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if var_init():
                if globalTokens[indicador] == ';':
                    indicador += 1
                    return True
                else: error()
            else: error()
        else: error()
    else: return False

def var_init():
    global indicador
    if globalTokens[indicador] == '=':
        indicador += 1
        if expression():
            return True
    else: return True

#Sentencias------------------------------------------------
def statement():
    global indicador
    if expr_stmt():
        return True
    elif for_stmt():
        return True
    elif if_stmt():
        return True
    elif print_stmt():
        return True
    elif return_stmt():
        return True
    elif while_stmt():
        return True
    elif block():
        return True
    else: return False

def expr_stmt():
    global indicador
    if expression():
        if globalTokens[indicador] == ';':
            indicador += 1
            return True
        else: error()
    else: return False

def for_stmt():
    global indicador
    if globalTokens[indicador] == 'FOR':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if for_stmt_1():
                if for_stmt_2():
                    if for_stmt_3():
                        if globalTokens[indicador] == ')':
                            indicador += 1
                            if statement():
                                return True
                            else: error()
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def for_stmt_1():
    global indicador
    if var_decl():
        return True
    elif expr_stmt():
        return True
    elif globalTokens[indicador] == ';':
        indicador += 1
        return True
    else: return False

def for_stmt_2():
    global indicador
    if expression():
        if globalTokens[indicador] == ';':
            indicador += 1
            return True
        else: error()
    elif globalTokens[indicador] == ';':
        indicador += 1
        return True
    else: return False

def for_stmt_3():
    global indicador
    if expression():
        return True
    else: return True

def if_stmt():
    global indicador
    if globalTokens[indicador] == 'IF':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if expression():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if statement():
                        if else_statement():
                            return True
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def else_statement():
    global indicador
    if globalTokens[indicador] == 'ELSE':
        indicador += 1
        if statement():
            return True
        else: error()
    else: return True

def print_stmt():
    global indicador
    if globalTokens[indicador] == 'PRINT':
        indicador += 1
        if expression():
            if globalTokens[indicador] == ';':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def return_stmt():
    global indicador
    if globalTokens[indicador] == 'RETURN':
        indicador += 1
        if return_exp_opc():
            if globalTokens[indicador] == ';':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def return_exp_opc():
    global indicador
    if expression():
        return True
    else: return True

def while_stmt():
    global indicador
    if globalTokens[indicador] == 'WHILE':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if expression():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if statement():
                        return True
                    else: error()
                else: error()
            else: error()
        else: error()   
    else: return False

def block():
    global indicador
    if globalTokens[indicador] == '{':
        indicador += 1
        if block_decl():
            if globalTokens[indicador] == '}':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def block_decl():
    global indicador
    if declaration():
        if block_decl():
            return True
        else: error()
    else: return True

#Expresiones----------------------------------------------
def expression():
    global indicador
    if assignment(): return True
    else: return False

def assignment():
    global indicador
    if logic_or():
        if assignment_opc(): return True
        else: error()
    else: return False

def assignment_opc():
    global indicador
    if globalTokens[indicador] == '=':
        indicador += 1
        if expression(): return True
        else: error()
    else: return True

def logic_or():
    global indicador
    if logic_and():
        if logic_or_2(): return True
        else: error()
    else: return False

def logic_or_2():
    global indicador
    if globalTokens[indicador] == 'OR':
        indicador += 1
        if logic_and():
            if logic_or_2(): return True
            else: error()
        else: error()
    else: return True

def logic_and():
    global indicador
    if equality():
        if logic_and_2(): return True
        else: error()
    else: return False

def logic_and_2():
    global indicador
    if globalTokens[indicador] == 'AND':
        indicador += 1
        if equality():
            if logic_and_2(): return True
            else: error()
        else: error()
    else: return True

def equality():
    global indicador
    if comparison():
        if equality_2(): return True
        else: error()
    else: return False

def equality_2():
    global indicador
    if globalTokens[indicador] == '!=':
        indicador += 1
        if comparison():
            if equality_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '==':
        indicador += 1
        if comparison():
            if equality_2(): return True
            else: error()
        else: error()
    else: return True

def comparison():
    global indicador
    if term():
        if comparison_2(): return True
        else: error()
    else: return False

def comparison_2():
    global indicador
    if globalTokens[indicador] == '>':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '>=':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '<':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '<=':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    else: return True

def term():
    global indicador
    if factor():
        if term_2(): return True
        else: error()
    else: return False

def term_2():
    global indicador
    if globalTokens[indicador] == '-':
        indicador += 1
        if factor():
            if term_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '+':
        indicador += 1
        if factor():
            if term_2(): return True
            else: error()
        else: error()
    else: return True

def factor():
    global indicador
    if unary():
        if factor_2(): return True
        else: error()
    else: return False

def factor_2():
    global indicador
    if globalTokens[indicador] == '/':
        indicador += 1
        if unary():
            if factor_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '*':
        indicador += 1
        if unary():
            if factor_2(): return True
            else: error()
        else: error()
    else: return True

def unary():
    global indicador
    if globalTokens[indicador] == '!':
        indicador += 1
        if unary(): return True
        else: error()
    elif globalTokens[indicador] == '-':
        indicador += 1
        if unary(): return True
        else: error()
    elif call(): return True
    else: return False

def call():
    global indicador
    if primary():
        if call_2(): return True
        else: error()
    else: return False

def call_2():
    global indicador
    if globalTokens[indicador] == '(':
        indicador += 1
        if arguments_opc():
            if globalTokens[indicador] == ')':
                indicador += 1
                if call_2(): return True
                else: error()
            else: error()
        else: error()
    elif globalTokens[indicador] == '.':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if call_2(): return True
            else: error()
        else: error()
    else: return True

def call_opc():
    global indicador
    
def primary():
    global indicador
    if globalTokens[indicador] == 'TRUE':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'FALSE':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'NULL':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'THIS':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'NUMERO':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'STRING':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'ID':
        indicador += 1
        return True
    elif globalTokens[indicador] == '(':
        indicador += 1
        if expression():
            if globalTokens[indicador] == ')':
                indicador += 1
                return True
            else: error()
        else: error()
    elif globalTokens[indicador] == 'SUPER':
        indicador += 1
        if globalTokens[indicador] == '.':
            indicador += 1
            if globalTokens[indicador] == 'ID':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

#Otras----------------------------------------------------
def funct():
    global indicador
    if globalTokens[indicador] == 'ID':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if parameters_opc():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if block(): return True
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def functions():
    global indicador
    if funct():
        if functions(): return True
        else: error()
    else: return True

def parameters_opc():
    global indicador
    if parameters(): return True
    else: return True

def parameters():
    global indicador
    if globalTokens[indicador] == 'ID':
        indicador += 1
        if parameters_2(): return True
        else: error()
    else: False

def parameters_2():
    global indicador
    if globalTokens[indicador] == ',':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if parameters_2(): return True
            else: error()
        else: error()
    else: return True

def arguments_opc():
    global indicador
    if arguments(): return True
    else: return True

def arguments():
    global indicador
    if expression():
        if arguments_2(): return True
        else: error()
    else: False

def arguments_2():
    global indicador
    if globalTokens[indicador] == ',':
        indicador += 1
        if expression():
            if arguments_2(): return True
            else: error()
        else: error()
    else: return True



###################################
#####                         #####
#####    Analizador léxico    #####
#####                         #####
###################################

#Quita comillas
def convCadena(cadena):
        newPala = []
        for c in cadena:
            if c != "\"":
                newPala += c
        return "".join(newPala)

#Imprime tokens
def imprimeTokens(cadenas, tokens):
    for i in range(len(cadenas)):
        #Para floats
        if tokens[i] == 'FLOAT':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {float(cadenas[i])}')
        #Para enteros
        elif tokens[i] == 'INT':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {int(cadenas[i])}')
        #Para cadenas
        elif tokens[i] == 'STRING':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {str(convCadena(cadenas[i]))}')
        #Para los otros
        elif cadenas[i] != '\n':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}')
    return

#Comprueba si es un numero flotante
def compfloat(cadena):
    for c in cadena:
        if c == '.':
            return True 
    return False

#Palabras reservadas
def reservadas(cadena):
    palabrasHM = {'for':'FOR', 'fun':'FUN', 'false':'FALSE', 'if':'IF', 'print':'PRINT', 'return':'RETURN', 
                'true':'TRUE', 'var':'VAR', 'else':'ELSE', 'or':'OR', 'null':'NULL', 'try':'TRY',
                'not':'NOT', 'break':'BREAK', 'and':'AND', 'identificador':'ID',
                'string':'STRING', '=':'=', 'while':'WHILE',
                '+':'+', '-':'-', '/':'/', '*':'*', '+=':'+=',
                '<=':'<=', '>=':'>=', '==':'==', '!=':'!=', '<':'<', '>':'>',
                '-=':'-=', '{':'{', '}':'}', '[':'[', ']':']',
                '(':'(', ')':')', ';':';', '.':'.', ',':',',
                'class':'CLASS', 'this':'THIS', 'super':'SUPER', 'numero':'NUMERO'}
    if cadena in palabrasHM :
        return palabrasHM[cadena]
    else: 
        return False
  
#Asignar palabras reservadas en tokens
def PalRe(cadena):
    tokens=[]
    for cad in cadena:
        if(reservadas(cad))!=False:
            tokens.append(reservadas(cad)) 
        elif (letras(cad[0])):
            tokens.append(reservadas('identificador'))
        #Tipo de número
        elif(numeros(cad[0]) or cad[0] == '.'):
            if(compfloat(cad)):
                tokens.append(reservadas('numero'))
            else:
                tokens.append(reservadas('numero'))
        #Tipo de dato
        elif(comillas(cad[0])):
            if(len(cad)>2):
                tokens.append(reservadas('string'))
            else:
                tokens.append(reservadas(cad))
        else:
            tokens.append(reservadas(cad))

    #Agrega EOF al último
    tokens.append('EOF')

    return tokens

#Categorias
def comillas(caracter):
    return caracter in "\""
def simbolos(caracter):
    return caracter in "(){}[],.:;-+*/!=<>%&"
def espacios(caracter):
    return caracter in " \n\t"
def letras(caracter):
    return caracter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX_"
def numeros(caracter):
    return caracter in "1234567890"
def operadores(caracter):
    return caracter in ["!=", "==", "<=", ">="]
def operaciones(caracter):
    return caracter in "/=+-*"
def llaves(caracter):
    return caracter in "{[()]}"

#Comprueba que sea numero
def compnum(cadena):
    validar = True
    for n in cadena:
        if numeros(n) == False:
            validar = False
    return validar

#Separa cada token
def separador(cadena):
    lineas = []
    estado = 0
    tokens = []
    tokenaux = []
    listado = []
    #Separa letras(cadenas), numeros, operadores, espacios, palabras reservadas
    for c in cadena:
        #Estado 0 - Inicio
        if letras(c) and estado == 0:
            estado = 1
            tokenaux += c
        elif numeros(c) and estado == 0:
            estado = 2 
            tokenaux += c
        elif comillas(c) and estado == 0:
            estado = 3
            tokenaux += c
        elif simbolos(c) and estado == 0:
            tokens += c
        elif espacios(c) and estado == 0:
            tokens += c
        #Estado 1 - Letras
        elif (letras(c) or numeros(c)) and estado == 1:
            tokenaux += c
        elif comillas(c) and estado == 1:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolos(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        #Estado 2 - Números
        elif numeros(c) and estado == 2:
            tokenaux += c
        elif comillas(c) and estado == 2:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolos(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif letras(c) and estado == 2:
            estado = 1
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        #Estado 3 - Cadenas
        elif not(comillas(c)) and estado == 3:
            tokenaux += c
        elif comillas(c) and estado == 3:
            estado = 0
            tokenaux += c
            tokens.append("".join(tokenaux))
            tokenaux.clear()
    if estado == 3:
        print("Error léxico, una cadena no fue terminanda")
        sys.exit(1)
    if estado == 2 or estado == 1:
        tokens.append("".join(tokenaux))
        tokenaux.clear()
    tokenaux.clear()

    #Junta los operadores: "<=" ">=" "==" "!=" "+="
    for i in range(len(tokens)):
        try:
            if (tokens[i] in "!=+-<>") and tokens[i+1] == "=":
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                tokenaux.clear()
        except IndexError:
            pass
    tokenaux.clear()

    #Junta los numeros flotantes
    compru = 0
    for i in range(len(tokens)):
        try:    
            if compru != 0:
                compru -= 1
            elif compnum(tokens[i]) and tokens[i+1] == "." and compnum(tokens[i+2]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokenaux += tokens[i+2]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                tokens[i+2] = ""
                listado.append(i+1)
                listado.append(i+2)
                compru = 2
                tokenaux.clear() 
            elif tokens[i] == "." and compnum(tokens[i+1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i+1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()

        except IndexError:
            if (i + 2) > len(tokens):
                compru = 0
            elif tokens[i] == "." and compnum(tokens[i+1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i+1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
         
    tokenaux.clear()

    #Elimina los datos sobrados
    listado.sort()
    cont = 0
    for num in listado:
        num -= cont
        tokens.pop(num)
        cont += 1
    
    #Elimina espacios
    cont=0
    for i in range(len(tokens)):
        if tokens[i]==' ':
            cont+=1
    for j in range(cont):
        tokens.remove(' ')

    #Elimina espacios \t
    cont=0
    for i in range(len(tokens)):
        if tokens[i]=='\t':
            cont+=1
    for j in range(cont):
        tokens.remove('\t')
    
    #Elimina saltos de linea
    cont=0

    for i in range(len(tokens)):    
        if tokens[i]=='\n':
            cont+=1
        else: lineas.append(cont+1)
    for j in range(cont):
        tokens.remove('\n')

    return tokens, lineas

#Omite los comentarios
def remove(cadena):
    estado = 0
    cad = []
    for c in cadena:
        #estado 0
        if estado == 0 and c == '/':
            estado = 1
            cad += c
        elif estado == 0 and c != '/':
            cad += c
        #estado 1
        elif estado == 1 and c == '/':
            estado = 2
            cad.pop()
        elif estado == 1 and c == '*':
            estado = 3
            cad.pop()
        elif estado == 1 and c != '/':
            estado = 0
            cad += c
        #estado 2
        elif estado == 2 and c == '\n':
            estado = 0
            cad += c
        #estado 3
        elif estado == 3 and c == '*':
            estado = 4
        #estado 4
        elif estado == 4 and c == '*':
            estado = 4 
        elif estado == 4 and c == '/':
            estado = 0
        elif estado == 4 and c != '/':
            estado = 3  
        if estado != 0:
            if c == '\n':
                cad += c
    return cad


###################################
#####                         #####
#####  Analizador semantico   #####
#####                         #####
###################################

#Solver Aritmetico
def resolver(n):    
    if len(n.get_hijos()) == 0:
        if n.get_token() == 'NUMERO':
            return float(n.get_lex())
        if n.get_token() == 'STRING':
            return str(n.get_lex())
        elif n.get_token() == 'ID':
            return obtenerValor(n.get_lex())

    izq = n.get_hijos()[0]
    der = n.get_hijos()[1]

    resultado_izquierdo = resolver(izq)
    resultado_derecho = resolver(der)

    if isinstance(resultado_izquierdo, float) and isinstance(resultado_derecho, float):
        if n.get_token() == '+':
            return resultado_izquierdo + resultado_derecho
        elif n.get_token() == '-':
            return resultado_izquierdo - resultado_derecho
        elif n.get_token() == '*':
            return resultado_izquierdo * resultado_derecho
        elif n.get_token() == '/':
            return resultado_izquierdo / resultado_derecho
    elif isinstance(resultado_izquierdo, str) and isinstance(resultado_derecho, str):
        if n.get_token() == '+':
            return resultado_izquierdo + resultado_derecho
        else:
            print("No se esperaba el operador '" + n.get_token() + "' en la concatenación")
            sys.exit(1)
            
    else:
        print("Error de concatenación entre " + str(resultado_izquierdo) + " y '" + str(resultado_derecho) + "'")
        sys.exit(1)

    return None


# Solver comparativo
def comparativo(n):
    if len(n.get_hijos()) == 0:
        if n.get_token() == 'NUMERO':
            return float(n.get_lex())
        if n.get_token() == 'STRING':
            return str(n.get_lex())
        elif n.get_token() == 'ID':
            return obtenerValor(n.get_lex()) 
        
    izq = n.get_hijos()[0]
    der = n.get_hijos()[1]
    
    resultado_izquierdo = comparativo(izq)
    resultado_derecho = comparativo(der)
    
    if isinstance(resultado_izquierdo, float) and isinstance(resultado_derecho, float):
        if n.get_token() == '>':
            return resultado_izquierdo > resultado_derecho
        elif n.get_token() == '>=':
            return resultado_izquierdo >= resultado_derecho
        elif n.get_token() == '<':
            return resultado_izquierdo < resultado_derecho
        elif n.get_token() == '<=':
            return resultado_izquierdo <= resultado_derecho
        elif n.get_token() == '==':
            return resultado_izquierdo == resultado_derecho
        elif n.get_token() == '!=':
            return resultado_izquierdo != resultado_derecho 
    elif isinstance(resultado_izquierdo, bool) and isinstance(resultado_derecho, bool):
        if n.get_token() == 'OR':
            return resultado_izquierdo or resultado_derecho
        elif n.get_token() == 'AND':
            return resultado_izquierdo and resultado_derecho 
    else:
        print("Error de comparación entre '" + str(resultado_izquierdo) + "' y '" + str(resultado_derecho) + "'")
        sys.exit(1)


# Tabla de Símbolos
tablaSimbolos = {}
def insertaValor(ID, value):
    global tablaSimbolos
    tablaSimbolos[ID] = value
def existeVariable(ID):
    global tablaSimbolos
    if ID in tablaSimbolos:
        return True
    else:
        return False
def obtenerValor(ID):
    global tablaSimbolos
    if ID in tablaSimbolos:
        return tablaSimbolos[ID]
    else:
        print("Error semantico, no se declaro la variable '" + ID + "'") 
        sys.exit(1)


#Para variable
def generaVar(padre):
    t = padre.get_token()
    if t == 'VAR':
        hijo = padre.get_hijos()[0]
        if existeVariable(hijo.get_lex()):
                print("La variable '" + hijo.get_lex() + "' ya a sido declarada")
                sys.exit(1)
        elif len(padre.get_hijos()) == 1:
            insertaValor(hijo.get_lex(), None)
        elif(len(padre.get_hijos()) == 2):
            hijo2 = padre.get_hijos()[1]
            insertaValor(hijo.get_lex(), resolver(hijo2))


# Resolver Árbol
def recorrer(padre):
    for n in padre.get_hijos():
        t = n.get_token()
        if t == "+" or t == '-' or t == '*' or t == '/': #Listo
            pass
        elif t == 'VAR':
            hijo = n.get_hijos()[0]
            if existeVariable(hijo.get_lex()):
                    print("La variable '" + hijo.get_lex() + "' ya a sido declarada")
                    sys.exit(1)
            elif len(n.get_hijos()) == 1:
                insertaValor(hijo.get_lex(), None)
            elif(len(n.get_hijos()) == 2):
                hijo2 = n.get_hijos()[1]
                insertaValor(hijo.get_lex(), resolver(hijo2))
        elif t == 'IF':
            hijo = n.get_hijos()[0]
            hijos = n.get_hijos()
            if comparativo(hijo):
                recorrer(n)
            elif hijos[-1].get_token() == 'ELSE':
                recorrer(hijos[-1])
        elif t == 'PRINT': #Listo
            print(resolver(n.get_hijos()[0]))
        elif t == 'WHILE':
            hijo = n.get_hijos()[0]
            while comparativo(hijo):
                recorrer(n)
        elif t == 'FOR':
            auxhijo = n.quitarHijo(0)
            generaVar(auxhijo)
            auxhijo = n.quitarHijo(1)
            n.insertar_siguiente_hijo(auxhijo)
            while comparativo(n.get_hijos()[0]):
                recorrer(n)
        elif t == '=':
            hijo1 = n.get_hijos()[0]
            hijo2 = n.get_hijos()[1]
            if existeVariable(hijo1.get_lex()):
                insertaValor(hijo1.get_lex(), resolver(hijo2))
            else:
                print("La variable '" + hijo.get_lex() + "' no se ha declarado")
                sys.exit()
            


# Clase Nodo
class Nodo:
    def __init__(self, tokens, lex):
        self.tokens = tokens
        self.lex = lex
        self.hijos = []

    def insertar_hijo(self, n):
        if self.hijos is None:
            self.hijos = [n]
        else:
            self.hijos.insert(0, n)

    def insertar_siguiente_hijo(self, n):
        if self.hijos is None:
            self.hijos = [n]
        else:
            self.hijos.append(n)

    def insertar_hijos(self, nodosHijos):
        for n in nodosHijos:
            if self.hijos is None:
                self.hijos = [n]
            else:
                self.hijos.append(n)
    
    def quitarHijo(self, num):
        return self.hijos.pop(num)

    def get_token(self):
        return self.tokens
    
    def get_lex(self):
        return self.lex

    def get_hijos(self):
        return self.hijos
 

# Generador AST
def generadorAST(tokens, lexico):
    raiz = Nodo(None, None)
    pilaPadres = [raiz]
    pila = []

    padre = raiz

    for i in range(len(tokens)):
        t = tokens[i]
        lex = lexico[i]
        
        if t == 'EOF':
            break

        if esPalabraReservada(t):
            n = Nodo(t, lex)

            padre = pilaPadres[-1]
            padre.insertar_siguiente_hijo(n)

            pilaPadres.append(n)
            padre = n

        elif esOperando(t):
            n = Nodo(t, lex)
            pila.append(n)

        elif esOperador(t):
            ari = aridad(t)
            n = Nodo(t, lex)
            for i in range(ari):
                nodo_aux = pila.pop()
                n.insertar_hijo(nodo_aux)
            pila.append(n)

        elif t == ';':
            if len(pila) == 0:
                pilaPadres.pop()
                padre = pilaPadres[-1]
            else:
                n = pila.pop()

                if padre.get_token() == 'VAR':
                    if n.get_token() == '=':
                        padre.insertar_hijos(n.get_hijos())
                    else:
                        padre.insertar_siguiente_hijo(n)
                    pilaPadres.pop()
                    padre = pilaPadres[-1]
                elif padre.get_token() == 'PRINT':
                    padre.insertar_siguiente_hijo(n)
                    pilaPadres.pop()
                    padre = pilaPadres[-1]
                else:
                    padre.insertar_siguiente_hijo(n)
    return raiz
    

# Palabras extra
def esPalabraReservada(cadena):
    palabras = ['VAR', 'IF', 'PRINT', 'ELSE', 'FOR', 'WHILE'] 
    if cadena in palabras:
        return True
    else: 
        return False
    
def esEstructControl(cadena):
    palabras = ['IF', 'ELSE', 'FOR', 'WHILE'] 
    if cadena in palabras:
        return True
    else: 
        return False
    
def esOperando(cadena):
    palabras = ['ID', 'NUMERO', 'STRING'] 
    if cadena in palabras:
        return True
    else: 
        return False
    
def esOperador(cadena):
    palabras = ['+', '-', '*', '/', '=', '>', '>=', '<', '<=', '==', '!=', 'AND', 'OR'] 
    if cadena in palabras:
        return True
    else: 
        return False
    
def precedenciaMayorIgual(pila, token):
    return  obtenerPrecedencia(pila) >= obtenerPrecedencia(token)

def obtenerPrecedencia(cadena):
    if cadena == '*' or cadena == '/':
        return 7
    elif cadena == '+' or cadena == '-':
        return 6
    elif cadena == '>' or cadena == '>=' or cadena == '<' or cadena == '<=':
        return 5
    elif cadena == '!=' or cadena == '==':
        return 4
    elif cadena == 'AND':
        return 3
    elif cadena == 'OR':
        return 2
    elif cadena == '=':
        return 1
    return 0

def aridad(cadena):
    palabras = ['+', '-', '*', '/', '=', '>', '>=', '<', '<=', '==', '!=', 'AND', 'OR']
    if cadena in palabras:
        return 2
    else: 
        return 0


# Generación postfija
def GenePost():
    global globalTokens
    global globalLex
    pilaTok = []
    pilaLex = []
    postfijaTokens = []
    postfijaLex = []
    estructControlPila = []
    estructControl = False

    for i in range(len(globalTokens)):
        token = globalTokens[i]

        #Por si termina
        if token == 'EOF':
            break

        #Si es palabra reservada
        if esPalabraReservada(token):
            postfijaTokens.append(token)
            postfijaLex.append(globalLex[i])
            if esEstructControl(token):
                estructControl = True
                estructControlPila.append(token)

        # Si es operando
        elif esOperando(token):
            postfijaTokens.append(token)
            postfijaLex.append(globalLex[i])

        # Si es parentesis que abre
        elif token == '(':
            pilaTok.append(token)
            pilaLex.append(globalLex[i])

        # Si es parentesis que cierra
        elif token == ')':
            while (len(pilaTok) != 0) and (pilaTok[-1] != '('):
                temp1 = pilaTok.pop()
                temp2 = pilaLex.pop()
                postfijaTokens.append(temp1)
                postfijaLex.append(temp2)
            if pilaTok[-1] == '(':
                pilaTok.pop()
                pilaLex.pop()
            if estructControl and (globalTokens[i + 1] == '{'):
                postfijaTokens.append(';')
                postfijaLex.append(';')

        # Si es operador
        elif esOperador(token):
            while (len(pilaTok) != 0) and (precedenciaMayorIgual(pilaTok[-1], token)):
                temp1 = pilaTok.pop()
                temp2 = pilaLex.pop()
                postfijaTokens.append(temp1)
                postfijaLex.append(temp2)
            pilaTok.append(token)
            pilaLex.append(globalLex[i])
        
        # Si es punto y coma
        elif token ==';':
            while (len(pilaTok) != 0) and (pilaTok[-1] != '{') and (pilaTok[-1] != '('):
                temp1= pilaTok.pop()
                temp2= pilaLex.pop()
                postfijaTokens.append(temp1)
                postfijaLex.append(temp2)
            postfijaTokens.append(token)
            postfijaLex.append(globalLex[i])
        
        # Si es llave que abre
        elif token =='{':
            pilaTok.append(token)
            pilaLex.append(globalLex[i])

        # Si es llave que cierra
        elif token == '}' and estructControl:
            if (globalTokens[i + 1]== 'ELSE'):
                pilaTok.pop()
                pilaLex.pop()
            else:
                
                pilaTok.pop()
                pilaLex.pop()
                postfijaTokens.append(';')
                postfijaLex.append(';')
                tokenaux = estructControlPila.pop()
                if (tokenaux=='ELSE'):
                    estructControlPila.pop()
                    postfijaLex.append(';')
                    postfijaTokens.append(';')
                if len(estructControlPila) == 0:
                    estructControl=False  
    # Si la pila no esta vacía
    while(len(pilaTok) != 0):
        temp1=pilaTok.pop()
        temp2=pilaLex.pop()
        postfijaTokens.append(temp1)
        postfijaLex.append(temp2)
    # Si la pila estruct no esta vacía
    while(len(estructControlPila) != 0):
        estructControlPila.pop()
        postfijaTokens.append(';')
        postfijaLex.append(';')
            
    return postfijaTokens, postfijaLex


#############################
###                       ###
###   Función principal   ###
###                       ###
#############################

def strings(tokens, lex):
    for i in range(len(tokens)):
        if tokens[i] == 'STRING':
            lex[i] = convCadena(lex[i])
    return tokens, lex

def lexico(cadena):
    cad = remove(cadena)
    global globalLex, globalLin
    globalLex, globalLin = separador(cad)
    global globalTokens 
    globalTokens = PalRe(globalLex)
    program()
    postfijaTokens, postfijaLex = GenePost()
    postfijaTokens, postfijaLex = strings(postfijaTokens, postfijaLex)
    arbol = generadorAST(postfijaTokens, postfijaLex)
    
    #print(postfijaTokens)
    #print(postfijaLex)
    recorrer(arbol)


    

#Transforma archivo txt a cadena
def transforma(archivo):
    if  not os.path.exists(archivo):
        return False
    arch = open(archivo, "r")
    cadena = []
    for linea in arch: 
        for c in linea: 
            cadena += c
    arch.close()
    return cadena



######################
#####            #####
#####    Main    #####
#####            #####
######################

#Comprueba si se introdujo un texto
if len(sys.argv) == 2:
    cadena = transforma(sys.argv[1])
    if (not cadena):
        print("Error al leer el archivo. No existe. Error 404")
    else :
        lexico(cadena)
#Comprueba si no se intodujo texto
elif len(sys.argv) == 1:
    cadena =[]
    print("Para terminar esciba 'ok'")
    while True:
        escrito = input('>>')
        if escrito != 'ok':
            cadena += escrito + '\n'
        else: break
    lexico(cadena)
#Manda error si no se cumple lo anterior    
else:
    print("Error de ejecución")
#HOLA