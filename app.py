from flask import Flask, render_template, url_for, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL


app= Flask(__name__)
app.secret_key = 'many random bytes'

#app.config['MySQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
#app.config['MySQL_USER'] = 'b8e78062f3909c'
#app.config['MySQL_PASSWORD'] = '64532001'
#app.config['MySQL_BD'] = 'heroku_631eb2166968388'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b8e78062f3909c'
app.config['MYSQL_PASSWORD'] = '64532001'
app.config['MYSQL_DB'] = 'heroku_631eb2166968388'
CORS(app)
mysql= MySQL(app)
@app.route('/')
def iniciarApp():
    return render_template('inicio.html')

@app.route('/empleado', methods =['GET'])
def mostrarEmpleados():
    cursor =mysql.connection.cursor()
    cursor.execute('SELECT  *FROM empleado')
    data = cursor.fetchall()
    cursor.close()
    return render_template('empleados/empleado.html', empleados=data)

if __name__ == '__main__':
    app.run(debug=True)