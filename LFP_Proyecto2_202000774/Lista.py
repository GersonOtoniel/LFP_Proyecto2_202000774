class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Lista:
    def __init__(self):
        self.primero = None
        self.tamaño = 0

    def insertar(self,dato):
        nuevo = Nodo(dato)
        if self.primero == None or self.tamaño == 0:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente != None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamaño+=1

    def imprimir(self):
        actual = self.primero
        while actual!=None:
            print(actual.dato)
            actual = actual.siguiente