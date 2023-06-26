import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
# importar el controaldor
import controladorapp

opciones = {}
user = ""

# initializations
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "Archivos PDF"

# settings
app.secret_key = "987654321"

# routes
@app.route('/')
@app.route('/libreria')
def Index():
    return render_template('login.html', mensaje=(True,False))

@app.route('/valid_usr', methods = ['POST'])
def valid_usr():
    global opciones
    global user
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['pwd']
        if (user != "" and password != ""):
            usuario = controladorapp.obtener_usuario(user, password)
            if len(usuario) > 0 :
                opciones = controladorapp.obtener_permisos(usuario[0][2])
                flash('Usuario Aceptado')
                return render_template('inicio.html', options = opciones, mensaje= (True,False))
            else:
                flash('Usuario o Contraseña Incorrecta')
                return render_template('login.html', mensaje = (True,False))
        else:
            flash('Usuario y/o Contraseña No Ingresados')
            return render_template('login.html', mensaje = (False,True))

@app.route('/register_usr')
def register_usr():
    return render_template('register.html', mensaje = (False,True))

@app.route('/recover_usr')
def recover_usr():
    return render_template('recuperar.html', mensaje = (False,True))

@app.route('/alu_query')
def alu_query():
    global user
    global opciones    
    registros = controladorapp.obtener_alumnos(user, "PUBLICADO")
    return render_template('alumno.html',listmaterial = registros, options = opciones, mensaje= (True,False))
    #return render_template('notyet.html', options = opciones, mensaje = (False,True))

@app.route('/alu_buy/<id>',methods=['POST'])
def alu_buy():
    global user
    global opciones
    if request.method == 'POST':
        in_fecha = datetime.today().strftime('%Y-%m-%d')
        controladorapp.actualizar_estado(id, 'SOLICITADO', in_fecha);
        materiales = controladorapp.obtener_valorizar()
        return render_template('valorizar.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

    
@app.route('/doc_query')
def doc_query():
    global user
    global opciones
    materiales = controladorapp.obtener_materiales(user)
    return render_template('docente.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

@app.route('/doc_publish/<id>')
def doc_publish(id):
    global user
    global opciones
    alumnos = controladorapp.actualizar_estado(id, 'PUBLICADO')
    materiales = controladorapp.obtener_materiales(user)
    return render_template('docente.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

@app.route('/doc_delete/<id>')
def doc_delete(id):
    return render_template('notyet.html', options = opciones, mensaje = (False,True))

@app.route('/doc_upload')
def doc_upload():
    cursos = controladorapp.obtener_cursos(user)
    materias = controladorapp.obtener_materias(user)
    return render_template('subir.html', options = opciones, listcursos=cursos, listmaterias=materias, mensaje = (False,True))

@app.route('/doc_uploadfile', methods = ['POST'])
def doc_uploadfile():
    global user
    if request.method == 'POST':
        titulo = request.form['titulo']
        curso = request.form['curso']
        materia = request.form['materia']
        # obtenemos el archivo del input "archivo"
        f = request.files['customFile']
        filename = secure_filename(f.filename)
        # Guardamos el material
        controladorapp.insertar_material(titulo, curso, materia, filename, user)
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        flash('Archivo subido exitosamente')
        return redirect(url_for('doc_query'))

@app.route('/lib_printer')
def lib_printer():
    global opciones
    global user
    materiales = controladorapp.obtener_procesar()
    return render_template('procesar.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

@app.route('/lib_reclaim')
def lib_reclaim():
    return render_template('notyet.html', options = opciones, mensaje = (False,True))

@app.route('/lib_sell')
def lib_sell():
    return render_template('notyet.html', options = opciones, mensaje = (False,True))

@app.route('/lib_valor')
def lib_valor():
    global opciones
    global user
    materiales = controladorapp.obtener_valorizar()
    return render_template('valorizar.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

@app.route('/lib_updvalor/<id>', methods = ['POST'])
def lib_updvalor(id):
    global opciones
    global user
    if request.method == 'POST':
        in_volumen = request.form['volumen']
        in_valor = request.form['valor']
        in_fecha = datetime.today().strftime('%Y-%m-%d')
        controladorapp.actualizar_valor(id, in_volumen, in_valor, in_fecha);
        materiales = controladorapp.obtener_valorizar()
        return render_template('valorizar.html', listmaterial = materiales,  options = opciones, mensaje = (False,True))

@app.route('/lib_valor/update/<id>', methods=['POST'])
def lib_valor_upd(id):
    return render_template('notyet.html', options = opciones, mensaje = (False,True))

#-----------------------------------------------------------------------------
#
#@app.route('/menu/<id>')
#def Menu():
#    return render_template('inicio.html')
#
#@app.route('/add_contact', methods = ['POST'])
#def add_contact():
#    if request.method == 'POST':
#        cuit = request.form['cuit']
#        nombre = request.form['nombre']
#        limitecredito = request.form['limitecredito']
#        descuento = request.form['descuento']
#        controladorapp.insertar_contacto(cuit, nombre, #limitecredito, descuento)
#        flash('Contacto Agregado satisfactoriamente')
#        return redirect(url_for('Index'))
#
#@app.route('/edit/<id>', methods = ['POST', 'GET'])
#def get_contact(id):
#    contacto = controladorapp.obtener_contacto_por_id(id)
#    return render_template('editarContacto.html', contact #= contacto)
#
#@app.route('/update/<id>', methods=['POST'])
#def update_contact(id):
#    if request.method == 'POST':
#        cuit = request.form['cuit']
#        nombre = request.form['nombre']
#        limitecredito = request.form['limitecredito']
#        descuento = request.form['descuento']
#        controladorapp.actualizar_contacto(nombre, #limitecredito, descuento, cuit)
#        flash('Contacto Actualizado Satisfactoriamente')
#        mensaje={'Contacto Actualizado #Satisfactoriamente', url_for('Index')}
#        return render_template('mensaje.html', #mensa=mensaje)        
#        #return redirect(url_for('Index'))
#
#@app.route('/delete/<string:id>', methods = ['POST',#'GET'])
#def delete_contact(id):
#    controladorapp.eliminar_contacto(id)
#    flash('Contacto Removido Satisfactoriamente')
#    return redirect(url_for('Index'))
#
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
