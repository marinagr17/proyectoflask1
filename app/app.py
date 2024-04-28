from flask import Flask, render_template, request, session, json, redirect, url_for, abort
import json
import os

app=Flask (__name__)



@app.route('/')
def index():
    return render_template('bienvenido.html')

@app.route('/buscador')
def buscador():
    cadena = session.get('cadena_busqueda', '')  # Obtener la cadena de búsqueda de la sesión
    return render_template("buscador.html", cadena=cadena)

@app.route('/lista', methods=["GET", "POST"])
def lista():
    if request.method == "POST":
        # Obtener el plato de búsqueda del formulario
        cadena_busqueda = request.form.get('cadena', '')
        try:
            # ruta completa al archivo JSON
            ruta_json = os.path.join(app.root_path, 'static', 'plantilla.json')
                
            # cargar el archivo JSON
            with open(ruta_json, 'r') as archivo:
                datos = json.load(archivo)

                # Filtrar los platos según la cadena de búsqueda
                platos_filtrados = [plato for plato in datos['menu'] if plato['nombre_plato'].startswith(cadena_busqueda)]

                # Si no se encuentran platos que coincidan, mostrar un mensaje de error
                if not platos_filtrados:
                    mensaje = "No se encontraron resultados para la búsqueda: {}".format(cadena_busqueda)
                    return render_template('lista.html', platos=[], mensaje=mensaje)

                # Almacenar la cadena de búsqueda en la sesión
                session['cadena_busqueda'] = cadena_busqueda

        except FileNotFoundError:
            # Si el archivo no se encuentra, abortar con un error 404
            abort(404)
            
        # Renderizar la plantilla 'lista.html' y pasar los platos filtrados
        return render_template('lista.html', platos=platos_filtrados)
    else:    
            # Si la solicitud es GET, redirigir de vuelta a la página de lista
        return redirect(url_for('lista'))

@app.route('/detalle/<item_id>')
def detalle(item_id):
    try:
        # ruta completa al archivo JSON
        ruta_json = os.path.join(app.root_path, 'static', 'plantilla.json')

        # cargar el archivo JSON
        with open(ruta_json, 'r') as archivo:
            datos = json.load(archivo)

            # Buscar el plato por su item_id
            plato = next((plato for plato in datos['menu'] if plato['item_id'] == item_id), None)

            # Si no se encuentra el plato, abortar con un error 404
            if plato is None:
                abort(404)

            # Renderizar la plantilla 'detalles.html' y pasar los detalles del plato
            return render_template('detalles.html', plato=plato)
    except FileNotFoundError:
        # Si el archivo no se encuentra, abortar con un error 404
        abort(404)

app.secret_key = 'marina'

if __name__=='__main__':
    app.run(debug=True)