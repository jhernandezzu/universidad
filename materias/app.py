from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['materias']
materias_collection = db['materias']

# Rutas CRUD

@app.route('/')
def index():
    materias = materias_collection.find()
    return render_template('index.html', materias=materias)

@app.route('/agregar_materia', methods=['GET', 'POST'])
def agregar_materia():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        profesor = request.form['profesor']
        horario = request.form['horario']
        cupos = int(request.form['cupos'])
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        
        fecha_creacion = datetime.now()
        fecha_modificacion = fecha_creacion
        
        materia = {
            'codigo': codigo,
            'nombre': nombre,
            'descripcion': descripcion,
            'profesor': profesor,
            'horario': horario,
            'cupos': cupos,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_creacion': fecha_creacion,
            'fecha_modificacion': fecha_modificacion
        }

        materias_collection.insert_one(materia)
        return redirect(url_for('index'))

    return render_template('agregar_materia.html')

@app.route('/editar_materia/<codigo>', methods=['GET', 'POST'])
def editar_materia(codigo):
    materia = materias_collection.find_one({'codigo': codigo})

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        profesor = request.form['profesor']
        horario = request.form['horario']
        cupos = int(request.form['cupos'])
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        
        fecha_modificacion = datetime.now()

        materias_collection.update_one(
            {'codigo': codigo},
            {'$set': {
                'nombre': nombre,
                'descripcion': descripcion,
                'profesor': profesor,
                'horario': horario,
                'cupos': cupos,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'fecha_modificacion': fecha_modificacion
            }}
        )
        return redirect(url_for('index'))

    return render_template('editar_materia.html', materia=materia)

@app.route('/eliminar_materia/<codigo>')
def eliminar_materia(codigo):
    materias_collection.delete_one({'codigo': codigo})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
