from Lista import Lista
from Tokens import Token
from ErrorLexico import Error

class Analizador:
    def __init__(self) -> None:
        
        self.equivalencias_reservadas = {
            'CrearBD': 'use',
            'EliminarDB': 'DropDataBase',
            'CrarColeccion': 'createCollection',
            'EliminarColeccion': 'dropCollection',
            'InsertarUnico': 'InsertOne'
        }

        self.alfabetoMayusculas = ['A','B','C','D','E','F','G','H','I','J','J','L','M','N','O','P','Q','R','S','T',
                                   'U','V','W','X','Y','Z']
        self.alfabetoMinuscular = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.alfabetoNumero = ['0','1','2','3','4','5','6','7','8','9']
        self.ID = ['A','B','C','D','E','F','G','H','I','J','J','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9']
        self.lista_lexemas = []

        self.tokens = {
            'RFUNCION': ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 
                         'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico'],
            'RASIGNACION': '=',
            'RNUEVA': 'nueva',
            'RCOMILLASIMPLES': '\'',
            'RCOMILLASDOBLES':  '\"',
            'RID': self.ID,
            'RPARENABIERTO': '(',
            'RPARENVERRADO': ')',
            'RPUNTOCOMA': ';',
            'RCOMA': ',',
            'RDOSPUNTOS': ':'
        }
        
        self.lista_ignorar = ['\n', '\t',' ']
        self.lista = Lista()
        self.lista_errores = Lista()
        

    def Analizar(self, text):
        
        self.columna = 1
        self.fila =1
        count=0
        while count<len(text):
            char = text[count]
            charanterior = text[count-1]
            if (count+1)<len(text):
                charsiguiente = text[count+1]

            if char == '\n':
                self.fila+=1
                self.columna=1

            if char=='-' and text[count+1]=='-':
                comentario = self.comentarioLinea(text[count:])
                count+=len(comentario)

            if text[count] == '/' and text[count+1] == '*':
                comentarios = self.comentarioVariasLineas(text[count:])
                count+=len(comentarios)
                self.columna+=len(comentarios)

            if char in self.alfabetoNumero:
                if charsiguiente in self.alfabetoMayusculas or charsiguiente in self.alfabetoMinuscular:
                    lexemaError = self.Lexemas(text[count:])
                    count+=len(lexemaError)
                    token0 = Error('Léxico',self.fila, self.columna, 'Error', 'No puede comenzar por numero')
                    self.lista_errores.insertar(token0)
            
            if char ==';':
                for k in self.tokens:
                    if char in self.tokens[k]:
                        token = Token(k,char)
                        self.lista.insertar(token)

            #----------------------------------------FUNCIONES----------------------------------
            if char in self.alfabetoMayusculas:
                if charanterior == '\n' or charanterior == ' ':
                    lexema = self.funciones(text[count:])
                    self.lista_lexemas.append(lexema)
                    count+=len(lexema)
                    aceptacion = 0
                    for i in self.tokens:
                        if lexema in self.tokens[i]:
                            print(f'Token: {i} , Lexema: {lexema}, Fila: {self.fila}, Columna: {self.columna}')
                            token = Token(i,lexema)
                            self.lista.insertar(token)
                            aceptacion=1
                    if aceptacion==0:
                        token1 = Token('RID', lexema)
                        self.lista.insertar(token1)
                    aceptacion=0
                    self.columna+=len(lexema)

            
            if char in self.alfabetoMinuscular or char=='=':
                lexema2 = self.Lexemas(text[count:])
                self.lista_lexemas.append(lexema2)
                count+=len(lexema2)
                aceptacion2=0
                for j in self.tokens:
                    if lexema2 in self.tokens[j]:
                        print(f'Token: {j} , Lexema: {lexema2}, Fila: {self.fila}, Columna: {self.columna}')
                        token2 = Token(j, lexema2)
                        self.lista.insertar(token2)
                        aceptacion2=1
                if aceptacion2==0:
                    token3 = Token('RID', lexema2)
                    self.lista.insertar(token3)
                aceptacion2=0
                self.columna+=len(lexema2)
    
            count+=1
            self.columna+=1
        print(self.lista_lexemas)
        #self.tokensReconocidos()
        #for i in self.lista_lexemas:
         #   if i in self.equivalencias_reservadas:
          #      print(self.equivalencias_reservadas.get(i))

    def Lexemas(self, text):
        count = 0
        lexema = ''
        while count<len(text):
            char = text[count]
            if char =='\n':
                self.fila+=1
                self.columna=1
            if char == " " or char== '\n' or char =="(" or char=="\"":
                return lexema
            if char in self.alfabetoMayusculas or char in self.alfabetoMinuscular or char in self.alfabetoNumero or char=='=':
                lexema+=char
            else:
                print('error')
            count+=1

    
                

    def comentarioLinea(self, text):
        comentario = ''
        count = 0
        while True:
            char = text[count]
            if char == '\n':
                self.fila+=1
                self.columna=1
                return comentario
            else:
                comentario+=char
            count+=1

    def funciones(self, text):
        funcion = ''
        string = ''
        count = 0
        aceptacion = 0
        while True:
            char = text[count]
            if char =='\n':
                self.fila+=1
                self.columna=1
            if char ==';':
                for k in self.tokens:
                    if char in self.tokens[k]:
                        token = Token(k,char)
                        self.lista.insertar(token)
            if char == '"':
                aceptacion+=1
                if aceptacion == 2:
                    aceptacion = 0
                    token2 = Token('RString', string)
                    self.lista.insertar(token2)
                    string=''
                if aceptacion==1:
                    string+=char            
            if char == ' ' or char == '\n' or char=='(':
                return funcion
            else:
                funcion+=char
            count+=1

    def comentarioVariasLineas(self, text):
        count = 0
        comentarios = ''
        while True:
            char = text[count]
            if char == '\n':
                self.fila+=1
                self.columna=1
            if char == '*' and text[count+1] == '/':
                return comentarios
            else:
                comentarios+=char
            count+=1

    def errores(self, text):
        pass


    def tokensReconocidos(self, lexema):
        for i in self.tokens:
            if lexema in self.tokens[i]:
                return True




entrada = '''
--Esto es un comentario de una sola línea
-- Este es otro comentario

/*
Esto es un comentario
de varias
lineas
*/

CrearBD base1 = nueva CrearBD();

EliminarBD eliminarbase1 = nueva EliminarBD('base1');
'''

#j = Analizador()
#j.Analizar(entrada)