#Funcion que convierte
def convertirDataDictianry(data, listKeys):
    lista= list(data)
    keys=[]
    for key in listKeys:
        keys.append(key)
    nueva_lista=[]
    for producto in lista:
        nueva_lista.append(producto)
        resultado = [ dict(zip(keys, i)) for i in nueva_lista ]
    return resultado