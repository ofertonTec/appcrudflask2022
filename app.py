from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL


app= Flask(__name__)

@app.route('/')
def inciarApp():
    return 'Inicio'

@app.route('/empleado')
def mostrarEmpleados():
    return 'Empleados'

if __name__ == '__main__':
    app.run()