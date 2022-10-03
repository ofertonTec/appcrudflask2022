from flask import Flask, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL


app= Flask(__name__)

app.config['MYSQL_HOST']='us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER']='b8e78062f3909c'
app.config['MYSQL_PASSWORD']='64532001'
app.config['MYSQL_BD']='heroku_631eb2166968388'
mysql= MySQL(app)
CORS(app)

@app.route('/')
def iniciarApp():
    return render_template('inicio.html')

@app.route('/empleado')
def mostrarEmpleados():
    return render_template('empleados/empleado.html')

if __name__ == '__main__':
    app.run(debug=True)