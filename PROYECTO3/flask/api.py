from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from procesos import inicioProceso, fechasHTML, resumen1, resumen2, crearPDF

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
    save_file = open('solicitud.xml', 'w')
    save_file.write(str_file)
    save_file.close()
    return Response(status=204)


@app.route('/procesos', methods=['GET'])
def get_procesos():
    autorizacion = open('autorizacion.xml', 'r+')
    return Response(status=200,
                    response=autorizacion.read(),
                    content_type='text/plain')


@app.route('/procesos', methods=['POST'])
def post_procesos():
    inicioProceso()
    return Response(status=204)


@app.route('/reset', methods=['POST'])
def reset():
    archivo = open('autorizacion.xml', 'w')
    archivo.write('')
    archivo.close()

    archivo = open('database.xml', 'w')
    archivo.write('')
    archivo.close()
    
    return Response(status=204)


@app.route('/fechas', methods=['GET'])
def get_fechas():
    fechas = fechasHTML()
    return Response(status=200,
                    response=fechas,
                    content_type='text/plain')   


@app.route('/grafica', methods=['GET'])
def get_graficas():
    selector = str(request.args.get('selector'))
    inferior = str(request.args.get('inferior'))
    superior = str(request.args.get('superior'))
    tipo = int(request.args.get('tipo'))
    grafica = resumen1(selector)
    grafica = resumen2(inferior, superior, tipo, grafica)
    crearPDF(grafica)

    return jsonify(
        fecha = grafica.fecha,
        nits = grafica.nits,
        ivaEmitido = grafica.ivaEmitido,
        ivaRecibido = grafica.ivaRecibido,
        monto = grafica.monto
    )


if __name__=='__main__':
    app.run(debug = True, port = 5000)