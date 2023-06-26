from bd import  obtener_conexion
from datetime import datetime

def obtener_usuario(usuario, password):
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE mail = %s AND password = %s", (usuario, password))
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_permisos(usuario):
    conexion = obtener_conexion()
    permisos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT opcion, programa, icono FROM vw_Usuarios_Opciones WHERE mail  = %s", (usuario))
        permisos = cursor.fetchall()
    conexion.close()
    return permisos

def obtener_cursos(usuario):
    conexion = obtener_conexion()
    cursos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT curso FROM usuarios_cursos WHERE mail  = %s", (usuario))
        cursos = cursor.fetchall()
    conexion.close()
    return cursos

def obtener_materias(usuario):
    conexion = obtener_conexion()
    materias = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT materia FROM cursos_materias WHERE mail  = %s", (usuario))
        materias = cursor.fetchall()
    conexion.close()
    return materias

def insertar_material(titulo, curso, materia, filename, user):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO materiales(titulo, volumen, curso, materia, estado, precio, fechaestado, ubicacionurl, mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(titulo, 0, curso, materia, 'SUBIDO',0, datetime.today().strftime('%Y-%m-%d'),filename, user))
    conexion.commit()
    conexion.close()

def insertar_pedido(mail,material,fecha):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pedidos(estado, fechaestado, material_id, mail) VALUES (%s, %s, %s, %s)",('SOLICITADO', fecha, material, mail))
    conexion.commit()
    conexion.close()    

def obtener_materiales(user):
    conexion = obtener_conexion()
    materiales = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT material_id, titulo, curso, materia, estado FROM materiales WHERE mail = %s",(user)) 
        materiales = cursor.fetchall()
    conexion.close()
    return materiales

def obtener_valorizar():
    conexion = obtener_conexion()
    materiales = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT material_id, titulo, curso, materia, estado FROM materiales WHERE estado = 'SUBIDO'") 
        materiales = cursor.fetchall()
    conexion.close()
    return materiales

def actualizar_valor(id, volumen, valor, fecha):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sqltxt ="UPDATE materiales SET volumen=%s,estado='VALORIZADO',precio=%s,fechaestado=%s WHERE material_id = %s",(volumen,valor,fecha,id)
        print(sqltxt)
        cursor.execute("UPDATE materiales SET volumen=%s,estado='VALORIZADO',precio=%s,fechaestado=%s WHERE material_id = %s",(volumen,valor,datetime.today(),id)) 
    conexion.commit()
    conexion.close()

def actualizar_estado(id, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE materiales SET estado=%s WHERE material_id = %s",(estado,id)) 
    conexion.commit()
    conexion.close()

def obtener_alumnos(usuario, estado):
    conexion = obtener_conexion()
    alumnos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_alumnos_materiales WHERE mail = %s AND estado_material = %s",(usuario, estado)) 
        alumnos = cursor.fetchall()
    conexion.close()
    return alumnos

def obtener_procesar():
    conexion = obtener_conexion()
    alumnos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_materiales_pedidos WHERE estado = 'SOLICITADO'") 
        materiales = cursor.fetchall()
    conexion.close()
    return materiales

""" 
def insertar_contacto(cuit, nombre, limitecredito, descuento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO clientes(cuit, nombre, limitecredito, descuento) VALUES (%s, %s, %s, %s)",(cuit, nombre, limitecredito, descuento))
    conexion.commit()
    conexion.close()

def obtener_contactos():
    conexion = obtener_conexion()
    clientes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT cuit, nombre, limitecredito, descuento FROM clientes")
        clientes = cursor.fetchall()
    conexion.close()
    return clientes
 """

""" 
def eliminar_contacto(cuit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM clientes WHERE cuit = %s", (cuit))
    conexion.commit()
    conexion.close()


def obtener_contacto_por_id(cuit):
    conexion = obtener_conexion()
    contacto = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT cuit, nombre, limitecredito, descuento FROM clientes WHERE cuit = %s", (cuit))
        contacto = cursor.fetchone()
    conexion.close()
    return contacto


def actualizar_contacto(nombre, limitecredito, descuento, cuit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE clientes SET nombre = %s, limitecredito = %s, descuento = %s WHERE cuit = %s", (nombre, limitecredito, descuento, cuit))
    conexion.commit()
    conexion.close() """