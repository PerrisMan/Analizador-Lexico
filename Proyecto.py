import sys

#Imprimir tokens
def printf(cadena):
    
    return


#Palabras reservadas
def reservadas(cadena):
    palabrasHM = {'for':'FOR','fun':'FUNCION','false':'FALSE','if':'IF', 'print':'PRINT','return':'RETURN', 'true':'TRUE',
                'var':'VARIABLE', 'else':'ELSE','or':'OR','None':'NONE','try':'TRY','not':'NOT','break':'BREAK', 'and':'AND'}
    if cadena in palabrasHM :
        return palabrasHM[cadena]
    else: 
        return False

    

#Tipo de dato
def tipovar(cadena):
    return cadena in ['entero','flotante','string','caracter']


#Asignar palabras reservadas en tokens
def PalRe(cadena):
    tokens=[]
    for cad in cadena:
        if(reservadas(cad))!=False:
            tokens.append(reservadas(cad))   
    return tokens

#Asigna los tokens
#ttokens = tipotokens(sep)
def tipotokens(cadena):
    typeT = ['letras', 'comillas', 'operadores', 'espacios', 'numeros','palabrasHM']
    for tipotokens in typeT:
        return typeT

#Categorias
def comillas(caracter):
    return caracter in "\""
def operadores(caracter):
    return caracter in "(){}[],.:;-+*/!=<>%&"
def espacios(caracter):
    return caracter in " \n\t"
def letras(caracter):
    return caracter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX_"
def numeros(caracter):
    return caracter in "1234567890"


#Comprueba que sea numero
def compnum(cadena):
    validar = True
    for n in cadena:
        if numeros(n) == False:
            validar = False
    return validar


#Separa cada token
def separador(cadena):
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
        elif operadores(c) and estado == 0:
            tokens += c
        elif espacios(c) and estado == 0:
            tokens += c
        #Estado 1 - Letras
        elif (letras(c) or numeros(c)) and estado == 1:
            tokenaux += c
        elif operadores(c) and estado == 1:
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
        elif operadores(c) and estado == 2:
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

    #Junta los operadores: "<=" ">=" "==" "!="
    for i in range(len(tokens)):
        if tokens[i] in "<>=!+-" and tokens[i+1] == "=":
            tokenaux += tokens[i]
            tokenaux += tokens[i+1]
            tokens[i] = "".join(tokenaux)
            tokens[i+1] = ""
            listado.append(i+1)
            tokenaux.clear()

    #Junta los numeros flotantes
    for i in range(len(tokens)):
        if compnum(tokens[i]) and tokens[i+1] == "." and compnum(tokens[i+2]):
            tokenaux += tokens[i]
            tokenaux += tokens[i+1]
            tokenaux += tokens[i+2]
            tokens[i] = "".join(tokenaux)
            tokens[i+1] = ""
            tokens[i+2] = ""
            listado.append(i+1)
            listado.append(i+2)
            tokenaux.clear()

    #Elimina los datos sobrados
    listado.sort()
    cont = 0
    for num in listado:
        num -= cont
        tokens.pop(num)
        cont += 1

    return tokens

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
        #estado 3
        elif estado == 3 and c == '*':
            estado = 4
        #estado 4
        elif estado == 4 and c == '/':
            estado = 0
        elif estado == 4 and c != '/':
            estado = 3  
    return cad

#Función principal------------------------------------------------------
def lexico(cadena):
    cad = remove(cadena)
    sep = separador(cad)
    ttokens = PalRe(sep)
    print(ttokens)
    return 

#Transforma archivo txt a cadena
def transforma(archivo):
    arch = open(archivo, "r")
    cadena = []
    for linea in arch: 
        for c in linea: 
            cadena += c
    arch.close()
    return cadena

# Main==================================================================

#Si existe un archivo
if len(sys.argv) > 1:
    cadena = transforma(sys.argv[1])
    lexico(cadena)
#Desde la terminal
elif len(sys.argv) == 1:
    while(1):
        cadena = input(">>> ")
        if cadena != "exit":
            lexico(cadena)
        else:
            break