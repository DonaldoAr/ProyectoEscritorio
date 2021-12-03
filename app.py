from logging import debug
from flask import Flask, request, jsonify, Response, render_template, redirect, flash, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Otro import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import os
#  FUNCION PARA COLAGE
from colageImg import opacidadImagenes

# CARPETA DONDE SE ALMACENAN LOS DATOS
UPLOAD_FOLDER = 'static/uploads'
contador = 0
# SERVER 
app = Flask(__name__)
CORS(app)
app.debug = True
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1920 * 1024
# socketio, variable

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# GUARDAR EL CONTADOR EN UN JSON POR SI SE VA LA LUZ


# PATHS
# PathImagOri = r"./MosaicoPython/public/rel"
PathImagOri = r"./static/uploads"
PathImagenesRe = r"./public/Img"
PathImagenAgua = r"./fondo.jpg"
# PONERLO EN EL METODO GET


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def create_user():
    global contador
    if 'file' not in request.files:
        flash('Sin archivo')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No se a seleccionado imagen')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        contador += 1
        file.filename = str(contador)+'.jpg';
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Se cargo satisfactoriamente la imagen')
        
        print("contador: "+str(contador))
        # RENOMBRAR ARCHIVO QUE SE ENCUENTRA YA EN UPLOADS Y MANDARLO A rel
        opacidadImagenes(PathImagOri, PathImagenesRe, PathImagenAgua, contador)
        return render_template('index.html')
        # return render_template('index.html', filename=filename)
    else:
        flash('Solo se permite imagenes tipo: - png, jpg, jpeg, gif')
        return redirect(request.url)

# AGREGAR SOCKET.IO
# @app.route('/download', methods=['GET'])
@app.route('/carga', methods=['GET', 'POST'])
def other():
    # return jsonify({"respuesta":"ok"})
    # return render_template('down.html')
    return render_template('index.html')

@app.route('/display')
def display_image():
    #print('display_image filename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('index2.html')

# PARTE DE SocketIO
# @socketio.on('connect', namespace='/test')

def test_connect(filename):
    # socketio.emit('newnumber', {'number': number}, namespace='/test')
    # socketio.sleep(5)
    # thread = socketio.start_background_task(randomNumberGenerator)
    with open('./static/downloads/fin.jpg', 'rb') as f:
        image_data = f.read()
    # socketio.emit('my-image-event', {'image_data': image_data})
    # socketio.emit('out-image-event', {'image_data': image_data}, namespace='/test')


def test_disconnect():
    print('Client disconnected')



# FIN DE PARTE DE SOCKET



# RUTA NO ENCONTRADA
@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'Dato no encontrado :( ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    # app.run(debug = True)
    app.run(debug=True, host='0.0.0.0', port=9090)
    # socketio.run(app, debug=True, host='0.0.0.0', port=9000)