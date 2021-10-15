from flask import Flask, Response, request
from flask_cors import CORS
from procesos import xmlF

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})


@app.route('/datos', methods=['GET'])
def get_datos():
    solicitud = open('solicitud.xml', 'r+')
    return Response(status=200,
                    response=solicitud.read(),
                    content_type='text/plain')


@app.route('/datos', methods=['POST'])
def post_datos():
    str_file = request.data.decode('utf-8')
    save_file = open('solicitud.xml', 'w+')
    save_file.write(str_file)
    save_file.close()
    return Response(status=204)


@app.route('/procesos', methods=['GET'])
def get_procesos():
    print('hola desde el get')
    autorizacion = open('autorizacion.xml', 'r+')
    return Response(status=200,
                    response=autorizacion.read(),
                    content_type='text/plain')


@app.route('/procesos', methods=['POST'])
def post_procesos():
    print('hola desde el post')
    xmlF()
    return Response(status=204)


if __name__=='__main__':
    app.run(debug = True, port = 5000)