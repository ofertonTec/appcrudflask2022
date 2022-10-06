from flask import Flask, render_template, url_for,request,redirect,flash
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
productosSeleccionados=[]
#INICIO: Mostrar la foto
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)
#FIN: Mostrar la foto 

mysql= MySQL(app)
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



#INICIO: Agregar productos
@app.route('/producto' ,methods=['POST'])
def insertarProducto():
     codigo= request.form['codigo']
     nombre=request.form['nombre']
     tipo_envase=request.form['tipo_envase']
     precio_lista=request.form['precio_lista']
     tamaño=request.form['tamano']
     img=request.files['foto']
     estado=1
     now= datetime.now()
     tiempo=now.strftime("%Y%H%M%S")
     if img.filename !='':
         nuevoNombreFoto=tiempo+img.filename
         img.save("uploads/"+nuevoNombreFoto)
     cursor= mysql.connection.cursor()
     sql="INSERT INTO producto VALUES(%s,%s,%s,%s,%s, %s,%s);"
     cursor.execute(sql,(codigo,nombre,tamaño,tipo_envase,precio_lista ,estado,nuevoNombreFoto))
     mysql.connection.commit()
     return redirect('/')
#FIN: Agregar productos


#INICIO: Listar productos
@app.route('/', methods=['GET'])
def mostrarProductos():
    listaEnvase=['Seleccione','Plastico','Vidrio','Caja']
    cursor= mysql.connection.cursor()
    sql='SELECT * FROM producto'
    cursor.execute(sql)
    data =cursor.fetchall()
    if(len(productosSeleccionados)!=0):
        productosSeleccionados
        
    #INCIO:conviertiendo a un diccionario la data
    keys=['codigo','nombre','tamaño','envase','precio_lista','estado','foto']
    resultado =convertirDataDictianry(data,keys)
    #FIN: conviertiendo a un diccionario la data
    seleccion=len(productosSeleccionados)
    return render_template('productos/producto.html',listaEnvase=listaEnvase, 
    listaProductos=resultado, seleccionados=productosSeleccionados, cantidadSelec= seleccion)
#FIN: Listar productos

#INICIO: añadir al carrito
@app.route('/añadirCarrito' ,methods=['POST'])
def agregarAlCarrito():
    codigo=request.form['codigo']
    nombre=request.form['nombre']
    precio=request.form['precio']
    cantidad=request.form['cantidad']
    precio_total= float(cantidad) * float(precio)
    keys=['codigo','nombre','precio','cantidad' ,'precio_total']
    producto=[codigo,nombre,precio,cantidad,precio_total]
    productosSeleccionados.append(dict(zip(keys, producto)))
    print(f'Cantidad de productos agreagado:{productosSeleccionados}')
    print(f'productosSeleccionados:{productosSeleccionados}')
    return redirect('/')
#FIN: añadir al carrito


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

if __name__ == '__main__':
    app.run(debug=True)