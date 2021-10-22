from django.shortcuts import render, redirect
import requests
import re

# Create your views here.
endpoint = 'http://localhost:5000{}'

def index(request):
    if request.method == 'GET':  
        url = endpoint.format('/datos')  # http://localhost:5000/datos
        data = requests.get(url)  # consulta a la API
        url = endpoint.format('/procesos')  # http://localhost:5000/proceso
        cXml = requests.get(url)

        url = endpoint.format('/fechas')
        fBytes = requests.get(url)

        f = ''
        for f in fBytes:
            f = f.decode('utf-8')

        fechas = []
        while f != '':
            fecha = re.search(r'([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})', f).group()
            fechas.append(fecha)
            f = f.replace(fecha, '')

        context = {
            'data': data.text,
            'cXml': '',
            'fechas': fechas,
        }       

        if request.GET.get('bDatos') == '':
            context['cXml'] = cXml.text

        return render(request, 'index.html', context)


def carga(request):
    try:
        docs = request.FILES['document']
    except:
        return redirect('index')
    data = docs.read()
    url = endpoint.format('/datos')
    requests.post(url, data)
    return redirect('index')


def enviar(request):
    url = endpoint.format('/procesos')
    requests.post(url)
    return redirect('index')


def reset(request):
    url = endpoint.format('/reset')
    requests.post(url)
    return redirect('index')


def iva(request):
    if request.method == 'GET':
        selector = request.GET.get('selector')
        inferior = request.GET.get('inferior')
        superior = request.GET.get('superior')
        tipo = request.GET.get('tipo')
        url = endpoint.format('/grafica')  # http://localhost:5000/datos
        requests.get(url, {
            'selector': selector,
            'inferior': inferior,
            'superior': superior,
            'tipo': tipo
        })  # consulta a la API

        return render(request, 'graficas.html')


def regresar(request):
    return redirect('index')