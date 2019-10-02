import math
import random
import string

import matplotlib.pyplot as plt
import numpy as np

random.seed(0)

# Crea un numero al azar entre a y b
def rand(a, b):
    return (b-a)*random.random() + a

# Inicializa una matriz Ixj 
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# se utilizara como funcion sigmoide la tanh
def sigmoid(x):
    return math.tanh(x)
    
# La derivada de la funcion sigmoide en terminos de la salida (y)
def dsigmoid(y):
    return 1.0 - y**2
    # return sigmoid(y)*(1-sigmoid(y))


class CMatriz:
    def __init__(self, ne, no, ns):
        self.errorValue = []
        # Se define la cantidad de nodos de las capas de entrada, oculta y salida de acuerdo a los datos ingresados
        self.ne = ne + 1  # +1 que es el nodo de bias
        self.no = no
        self.ns = ns

        # Se establecen las activaciones para los nodos de cada capa
        self.ae = [1.0]*self.ne
        self.ao = [1.0]*self.no
        self.a_s = [1.0]*self.ns

        # Se crean las 2 matrices de los pesos  
        self.we = makeMatrix(self.ne, self.no)
        self.ws = makeMatrix(self.no, self.ns)

        # Se le dan valores aleatorios a los pesos de las matrices
        for i in range(self.ne):
            for j in range(self.no):
                self.we[i][j] = rand(-0.1, 0.1)
        for j in range(self.no):
            for k in range(self.ns):
                self.ws[j][k] = rand(-0.1, 0.1)

        # Se guardan las matrices para tener en cuenta el factor de inercia
        self.ce = makeMatrix(self.ne, self.no)
        self.cs = makeMatrix(self.no, self.ns)

    def actualizar(self, entradas):
        if len(entradas) != self.ne-1:
            raise ValueError('Numero incorrecto de entradas')

        # se ingresan los datos de entrada a los nodos de la capa de entrada
        for i in range(self.ne-1):
            self.ae[i] = entradas[i]

        # Se calcula si los datos que llegan a los nodos de la capa oculta pasan por el umbral
        for j in range(self.no):
            sum = 0.0
            for i in range(self.ne):
                sum = sum + self.ae[i] * self.we[i][j]
            self.ao[j] = sigmoid(sum)

        # Se calcula si los datos que llegan a los nodos de la capa de salida pasan por el umbral
        for k in range(self.ns):
            sum = 0.0
            for j in range(self.no):
                sum = sum + self.ao[j] * self.ws[j][k]
            val = sigmoid(sum)
            if(val >= 0.9 and val <= 1.1):
                val = 1
            elif(val >= -0.1 and val <= 0.1):
                val = 0
            self.a_s[k] = val

        return self.a_s[:]

    def BackPropagate(self, objetivos, A, IN):
        if len(objetivos) != self.ns:
            raise ValueError('Numero incorrecto de salida')

        # se calcula el error obtenido en la capa de salida
        diferencia_salidas = [0.0] * self.ns
        for k in range(self.ns):
            error = objetivos[k]-self.a_s[k]
            diferencia_salidas[k] = dsigmoid(self.a_s[k]) * error

        # se calcula el error obtenido en la capa oculta
        diferencia_oculta = [0.0] * self.no
        for j in range(self.no):
            error = 0.0
            for k in range(self.ns):
                error = error + diferencia_salidas[k]*self.ws[j][k]
            diferencia_oculta[j] = dsigmoid(self.ao[j]) * error

        # Actualiza los pesos de oculta-salida
        for j in range(self.no):
            for k in range(self.ns):
                cambio = diferencia_salidas[k]*self.ao[j]
                self.ws[j][k] = self.ws[j][k] + A*cambio + IN*self.cs[j][k]
                self.cs[j][k] = cambio

        # Actualiza los pesos de entrada-oculta
        for i in range(self.ne):
            for j in range(self.no):
                cambio = diferencia_oculta[j]*self.ae[i]
                self.we[i][j] = self.we[i][j] + A*cambio + IN*self.ce[i][j]
                self.ce[i][j] = cambio

        # se calcula el error obtenido entre la salida esperada y la obtenida
        error = 0.0
        for k in range(len(objetivos)):
            error = error + 0.5*(objetivos[k]-self.a_s[k])**2
        return error

    def probar(self, patrones):
        for p in patrones:
            print(p[0], '->', self.actualizar(p[0]))

    """def weights(self):
        print('Pesos de Entrada:')
        for i in range(self.ne):
            print(self.we[i])
        print()
        print('Pesos de Salida:')
        for j in range(self.no):
            print(self.ws[j])"""

    def getError(self, error):
        self.errorValue.append(error)

    def entrenar(self, patrones, iteraciones=1000, A=0.5, IN=0.1):
        # Tenemos que A es el factor de aprendizaje y IN el factor de inercia
        for i in range(iteraciones):
            error = 0.0
            for p in patrones:
                entradas = p[0]
                objetivos = p[1]
                self.actualizar(entradas)
                error_anterior = error
                error = error + self.BackPropagate(objetivos, A, IN)
                if (error_anterior == error and A < 0.9):
                    A += 0.1
                elif (error_anterior < error and A > 0.1):
                    A -= 0.1
            self.getError(error)
            
            if (error == 0):
                print('Iteraciones: ', i)
                break


def RedNeuronal():
    lista = []
    with open('entradas_7seg.txt') as fichero:
        for linea in fichero:
            lista.append(linea.strip("\n"))
    print(lista)
    lista = lista[::-1]
    tamanio = int(lista.pop())
    nodos_entrada = int(lista.pop())
    nodos_salida = int(lista.pop())

    patron = []
    for i in range(0, tamanio):
        pares = []
        valores = []
        for j in range(0, nodos_entrada):
            valores.append(int(lista.pop()))
        pares.append(valores)
        valores = []
        for j in range(0, nodos_salida, 1):
            valores.append(int(lista.pop()))
        pares.append(valores)
        patron.append(pares)

    

    # se crea red con nodos_entrada como la cantidad de nodos de entradas, (nodos_entrada+nodos_salida)/2 nodos para la capa oculta y nodos_salida como nodos de la capa de salida
    nodos_oculta = math.ceil((nodos_entrada+nodos_salida)/2) + 1

    n = CMatriz(nodos_entrada, (nodos_oculta), nodos_salida)
    # se entrena la red con los patrones ingresados
    n.entrenar(patron)
    # se realiza la prueba con los patrones ingresados
    n.probar(patron)

    patron1 = [
        [[1, 1, 1, 0, 0, 1, 1]],
        [[1, 1, 1, 0, 0, 0, 1]],
        [[0, 0, 1, 1, 1, 1, 1]]
    ]

    plt.plot(n.errorValue)
    plt.title("Grafico de errores")
    plt.xlabel("Iteracion")   # Establece el título del eje x
    plt.ylabel("Error")   # Establece el título del eje y

    plt.show()
    # n.probar(pat1)
    # x = np.array([0, 1, 2, 3, 4, 5, 6])
    # y = np.array(n.errorValue)
    # plt.bar(x, y, align="center")
    # plt.title('Barras de progreso de error')
    # plt.legend(['error'])
    # plt.show()


if __name__ == '__main__':
    RedNeuronal()
