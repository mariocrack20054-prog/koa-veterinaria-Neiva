"""
Paquete routes: aquí van los Blueprints de la aplicación.

Hice un archivo por cada tabla de la base de datos y todos siguen la
misma estructura, para que sea fácil de entender y de mantener:

    leer_formulario()  -> valida los datos que llegan del formulario
    listar()           -> GET  /tabla/               muestra todos los registros
    crear()            -> GET/POST /tabla/nuevo      formulario y guardado
    editar(id)         -> GET/POST /tabla/<id>/editar formulario precargado
    eliminar(id)       -> POST /tabla/<id>/eliminar  borra el registro

Archivos: duenos.py, mascotas.py, veterinarios.py, servicios.py, citas.py
"""
