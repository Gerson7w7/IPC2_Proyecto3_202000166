from django.shortcuts import render, redirect
import requests

# Create your views here.
endpoint = 'http://localhost:5000{}'

def index(request):
    if request.method == 'GET':     
        url = endpoint.format('/datos')  # http://localhost:5000/datos
        data = requests.get(url)  # consulta a la API
        url = endpoint.format('/procesos')  # http://localhost:5000/proceso
        cXml = requests.get(url)
        
        context = {
            'data': data.text,
            'cXml': cXml.text,
        }          
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