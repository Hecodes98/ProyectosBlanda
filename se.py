import pymongo

import numpy as np
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb+srv://karem-admin:karemgiovanna10@clusterinicial-qrqbw.mongodb.net/test?retryWrites=true&w=majority")
db = client.blanda
consulta = db.consultas
regla = db.reglas
hecho = db.hechos

sintomas=[]
tabla = {
    '25':0,
    '26':0,
    '27':0,
    '28':0,
    '29':0,
    '30':0,
}

def tipo(var, dic):
    cont = 0
    consec = var['consecuente']
    ponde = var['ponderacion']

    r = isinstance(consec, list)
    if r == True:
        for i in consec:
            m = str(int(i))
            dic[m]=dic[m]+(1-dic[m])*ponde[cont]
            cont+=1
    else:
        m = str(int(consec))
        dic[m] = dic[m]+(1-dic[m])*ponde



print("\nBIENVENIDO")
print("\nSintomas comunes en perros")
cont = 1
for i in hecho.find({ 'id': {"$lt": 25 } }):
    print(str(cont)+". "+ i['descripcion'])
    cont+=1

inp= input("\nDe los anteriores sintomas, por favor ingrese los numeros correspondientes (con una , intermedia) a los sintomas que presente su mascota: ")
sintomas = inp.split(",")
for i in sintomas:
    '''for j in hecho.find({"id": float(i)}):
        num = j['id']'''
    for k in regla.find({"antecedente": num}):
        tipo(k,tabla)
            
enfermedad = tabla.items()
elec1 = 0 #ponderacion
elec2 = 0 #enfermedad
for num , pon in enfermedad:
    if pon>elec1:
        elec1 = pon
        elec2 = num
for i in hecho.find({"id": float(elec2)}):
    res = i['descripcion']
    print(res)


x = np.array([1,2,3,4,5,6])
lista = [ tabla[key] for key in tabla ]
y = np.array(lista)

plt.bar(x,y, align="center")
plt.show()
print("+++")
print(tabla['25'])
print(tabla['26']) 
print(tabla['27']) 
print(tabla['28']) 
print(tabla['29']) 
print(tabla['30']) 
print("+++")    
                
                
        