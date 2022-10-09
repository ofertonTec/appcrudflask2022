from email.mime import image
from flask import Flask, render_template, url_for,request,redirect,flash,jsonify
import json
from flask_cors import CORS
from flask_mysqldb import MySQL
#INICIO: mostrar foto
from datetime import datetime
from flask import send_from_directory
import os
#FIN: mostrar foto
app= Flask(__name__)
app.secret_key = 'many random bytes'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'admin01'
#app.config['MYSQL_PASSWORD'] = 'admin01'
#app.config['MYSQL_DB'] = 'ventas'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b8e78062f3909c'
app.config['MYSQL_PASSWORD'] = '64532001'
app.config['MYSQL_DB'] = 'heroku_631eb2166968388'
CORS(app)
#INICIO: Mostrar la foto
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)
#FIN: Mostrar la foto 

mysql= MySQL(app)

#********************VARIABLES GLOBALES*********************#
listaProductos=[]
mensajes=[]
productosSleccionados=[]

@app.route('/')
def iniciarApp():
    return mostrarProductos()
#INICIO: Listar Empleados
@app.route('/empleado', methods =['GET'])
def mostrarEmpleados():
    cursor =mysql.connection.cursor()
    cursor.execute('SELECT  *FROM empleado')
    data = cursor.fetchall()
    cursor.close()
    return render_template('empleados/empleado.html', empleados=data)
#FIN: Listar Empleados

#INICIO: Crear nuevo empleado
@app.route('/NuevoEmpleado',  methods=['POST'])
def insertarEmpleado():
    if request.method=="POST":
        dni=request.form['dni']
        nombre=request.form['nombre']
        email=request.form['email']
        foto=request.files['foto']
        now= datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        if foto.filename !='':
            nuevoNombreFoto=tiempo+foto.filename
            foto.save("uploads/"+nuevoNombreFoto)
        cursor= mysql.connection.cursor()
        cursor.execute('INSERT INTO empleado(DNI,NOMBRE,EMAIL,FOTO) VALUES(%s,%s,%s,%s)',(dni,nombre,email,nuevoNombreFoto))
        mysql.connection.commit()
        return redirect('/empleado')

#FIN: Crear nuevo empleado

#INICIO: Eliminar empleado
@app.route('/eliminarEmpleado/<string:dni>', methods=['GET'])
def eliminarEmpleado(dni):
    flash('Se elimino exitosamente el registro')
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM empleado  WHERE DNI = %s", (dni,))
    mysql.connection.commit()
    return redirect('/empleado') 

#FIN: Eliminar empleado

#INICIO: Editar empleado
@app.route('/actualizarEmpleado' , methods=['POST'])
def actualizarEmpleado():
    if request.method=='POST':
        dni= request.form['dni']
        nombre=request.form['nombre']
        correo=request.form['email']
        foto=request.files['foto']
        cursor= mysql.connection.cursor()
        now= datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        if foto.filename != '':
            nuevoNombreFoto = tiempo +foto.filename
            foto.save("uploads/{}".format(nuevoNombreFoto))
            cursor.execute('SELECT foto FROM empleado WHERE dni={}'.format(dni))
            fila =cursor.fetchall()
            os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
            cursor.execute('UPDATE empleado SET foto=%s WHERE dni=%s',(nuevoNombreFoto,dni))
            mysql.connection.commit()
        cursor.execute("UPDATE empleado SET  nombre=%s, email=%s  WHERE dni=%s",(nombre,correo,dni))
        mysql.connection.commit()
        flash('Datos actualizados correctamente')
        return redirect('/empleado')
#FIN: Editar empleado


#**************************************INICIO: GESTIONAR PRODUCTOS***********************#
#INICIO: Agregar productos
@app.route('/producto' ,methods=['POST'])
def insertarProducto():
     codigo= request.form['codigo']
     nombre=request.form['nombre']
     tipo_envase=request.form['tipo_envase']
     precio_lista=request.form['precio_lista']
     tamaño=request.form['tamano']
     img=request.files['foto']
     descripcion=request.form['descripcion']
     estado=1
     now= datetime.now()
     tiempo=now.strftime("%Y%H%M%S")
     if img.filename !='':
         nuevoNombreFoto=tiempo+img.filename
         img.save("uploads/"+nuevoNombreFoto)
     cursor= mysql.connection.cursor()
     sql="INSERT INTO producto VALUES(%s,%s,%s,%s,%s, %s,%s,%s);"
     cursor.execute(sql,(codigo,nombre,tamaño,tipo_envase,precio_lista ,estado,nuevoNombreFoto,descripcion))
     mysql.connection.commit()
     return redirect('/')
#FIN: Agregar productos
#INICIO: Listar productos
@app.route('/', methods=['GET'])
def mostrarProductos():
    for mensaje in mensajes:
        flash(mensaje)
    
    if len(listaProductos) !=0:
        listaProductos.clear()
    listaEnvase=['Seleccione','Plastico','Vidrio','Caja']
    cursor= mysql.connection.cursor()
    sql='SELECT * FROM producto'
    cursor.execute(sql)
    data =cursor.fetchall()
    print(f'tipo  de la data:{type(data)}')
    print(f'tamaño  de la data:{len(data)}')
    keys=['codigo','nombre','tamaño','envase','precio_lista','estado','foto','descripcion']
    if len(data)!=0:
        resultado =convertirDataDictianry(data,keys)
        listaProductos.append(resultado)
        cantidadSelect =len(productosSleccionados)
        return render_template('productos/producto.html',listaEnvase=listaEnvase,listaProductos=resultado,cantidadSelect= cantidadSelect )
    else:
        return render_template('productos/producto.html',listaEnvase=listaEnvase)
#FIN: Listar productos

@app.route('/ingresarProductoAlCarrito', methods=['GET','POST'])
def ingresarProductoAlCarrito():
    mensajes.clear()
    codigo= request.args.get('codigo')
    cantidad=request.args.get('cantidad')
    #Verifico si el usuario ya ingreso el producto
    if (len(productosSleccionados) == 0):
        ##Completar producto y agreagar
        reconstruirProducto(codigo,cantidad)
    else:
        ##Verificar si existe el producto en la lista de productos seleccionados
        existe=[]
        for producto in productosSleccionados:
            if producto['codigo'] == codigo:
                existe.append(True)
        if len(existe)== 0:
            #completar el producto y agreagr
            reconstruirProducto(codigo,cantidad)
        else :
            mensajes.append('El producto ya ha sido añadido al carrito de compras') 
    return jsonify(productosSleccionados)
#________________________________________
def reconstruirProducto(codigo,cantidad):
    print(f'ListaProductos={listaProductos}')
    listProducts=listaProductos[0]
    for producto in listProducts:
        seleccion = producto['codigo'] == codigo
        if(seleccion):
            precio =producto['precio_lista']
            total=precio *int(cantidad)
            producto['cantidad']=cantidad
            producto['total']= round(total,2)
            productosSleccionados.append(producto)
#________________________________________

@app.route('/carrito')
def carrito():
    mensajes.clear()
    cantidadSelect=len(productosSleccionados)
    return render_template('carrito.html',listaSeleccionados= productosSleccionados ,cantidadSelect=cantidadSelect)


@app.route('/eliminarItem/<string:codigo>', methods=['GET'])
def eliminarItem(codigo):
    print(f'COdigo a eliminar:{codigo}')
    contador=0
    for producto in productosSleccionados:
        seleccion=producto['codigo'] == codigo
        if(seleccion):
            productosSleccionados.pop(contador)
        contador+=1

    return redirect('/carrito')
#**************************************FIN: GESTIONAR PRODUCTOS***********************#

def convertirListaDictionary():
    lista=[]
    for pro in listaProductos:
        for item in pro:
            lista.append(item)
    return lista

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

if __name__ == '__main__':
    app.run(debug=True)