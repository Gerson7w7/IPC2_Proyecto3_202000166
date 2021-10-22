from clases import Factura, Error, Autorizacion
import xml.dom.minidom 
import re
import numpy
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def inicioProceso():
    # las autorizaciones
    autorizaciones = []
    db = open('database.xml', 'r')
    data = db.read()
    if len(data) != 0:
        databaseCarga(autorizaciones)
    xmlF(autorizaciones)

# xml de entrada a lista de objetos
def xmlF(autorizaciones):
    facturas = []
    archivo = open('solicitud.xml', 'r')
    xmlDoc = xml.dom.minidom.parse(archivo) # para manejar el xml con las etiquetas
    data = xmlDoc.documentElement
    fac = data.getElementsByTagName("DTE") # lo separa por facturas en una lista
    for f in fac:
        # creando una instancia de tipo factura por cada factura
        factura = Factura()

        # fecha de la factura
        t = f.getElementsByTagName('TIEMPO')[0]
        tiempo = t.firstChild.data
        tiempo = tiempo.strip()
        factura.fecha = tiempo

        # referencia
        r = f.getElementsByTagName('REFERENCIA')[0]
        referencia = r.firstChild.data
        referencia = referencia.strip()
        factura.referencia = referencia

        # nit emisor
        e = f.getElementsByTagName('NIT_EMISOR')[0]
        emisor = e.firstChild.data
        emisor = emisor.strip()
        factura.nitEmisor = emisor

        # nit receptor
        r = f.getElementsByTagName('NIT_RECEPTOR')[0]
        receptor = r.firstChild.data
        receptor = receptor.strip()
        factura.nitReceptor = receptor

        # valor
        v = f.getElementsByTagName('VALOR')[0]
        valor = v.firstChild.data
        valor = valor.strip()
        factura.valor = valor

        # iva 
        i = f.getElementsByTagName('IVA')[0]
        iva = i.firstChild.data
        iva = iva.strip()
        factura.iva = iva

        # total
        t = f.getElementsByTagName('TOTAL')[0]
        total = t.firstChild.data
        total = total.strip()
        factura.total = total

        # agregando a la lista de facturas
        facturas.append(factura)
    verificaciones(facturas, autorizaciones)


# si el archivo autorización está lleno, se cargaran los datos
def databaseCarga(autorizaciones):
    archivo = open('database.xml', 'r')
    xmlDoc = xml.dom.minidom.parse(archivo) # para manejar el xml con las etiquetas
    data = xmlDoc.documentElement
    aut = data.getElementsByTagName("AUTORIZACION") # lo separa por facturas en una lista
    for a in aut:
        # creando una instancia de tipo autorizacion por cada autorización
        autorizacion = Autorizacion()

        # fecha de la autorizacion
        t = a.getElementsByTagName('FECHA')[0]
        tiempo = t.firstChild.data
        tiempo = tiempo.strip()
        autorizacion.fecha = tiempo

        # facturas recibidas de la autorizacion
        fr = a.getElementsByTagName('FACTURAS_RECIBIDAS')[0]
        facRecibidas = fr.firstChild.data
        facRecibidas = facRecibidas.strip()
        autorizacion.facRecibidas = int(facRecibidas)

        # errores de la autorizacion
        e = a.getElementsByTagName('ERRORES')[0]
        # error nit emisor 
        ne = e.getElementsByTagName('NIT_EMISOR')[0]
        nitEmisor = ne.firstChild.data
        nitEmisor = nitEmisor.strip()
        autorizacion.eEmisor = int(nitEmisor)
        # error nit receptor 
        nr = e.getElementsByTagName('NIT_RECEPTOR')[0]
        nitReceptor = nr.firstChild.data
        nitReceptor = nitReceptor.strip()
        autorizacion.eReceptor = int(nitReceptor)
        # error iva 
        i = e.getElementsByTagName('IVA')[0]
        iva = i.firstChild.data
        iva = iva.strip()
        autorizacion.eIva = int(iva)
        # error total 
        t = e.getElementsByTagName('TOTAL')[0]
        total = t.firstChild.data
        total = total.strip()
        autorizacion.eTotal = int(total)
        # error referencia 
        rd = e.getElementsByTagName('REFERENCIA_DUPLICADA')[0]
        referencia = rd.firstChild.data
        referencia = referencia.strip()
        autorizacion.eReferencia = int(referencia)
        
        # facturas correctas de la autorizacion
        fc = a.getElementsByTagName('FACTURAS_CORRECTAS')[0]
        facCorrectas = fc.firstChild.data
        facCorrectas = facCorrectas.strip()
        autorizacion.facCorrectas = int(facCorrectas)

        # cantidad de emisores de la autorizacion
        ce = a.getElementsByTagName('CANTIDAD_EMISORES')[0]
        emisores = ce.firstChild.data
        emisores = emisores.strip()
        autorizacion.emisores = int(emisores)

        # cantidad de emisores de la autorizacion
        cr = a.getElementsByTagName('CANTIDAD_RECEPTORES')[0]
        receptores = cr.firstChild.data
        receptores = receptores.strip()
        autorizacion.receptores = int(receptores)

        # lista de autorizaciones
        la = a.getElementsByTagName('LISTADO_AUTORIZACIONES')[0]
        aprobaciones = la.getElementsByTagName('APROBACION')
        facturas = []
        for aprobacion in aprobaciones:
            # facturas aprobadas
            factura = Factura()
            # nit emisor 
            ne = aprobacion.getElementsByTagName('NIT_EMISOR')[0]
            nitEmisor = ne.firstChild.data
            nitEmisor = nitEmisor.strip()
            referencia = ne.getAttribute("ref")
            factura.nitEmisor = nitEmisor
            factura.referencia = referencia
            # nit receptor 
            nr = aprobacion.getElementsByTagName('NIT_RECEPTOR')[0]
            nitReceptor = nr.firstChild.data
            nitReceptor = nitReceptor.strip()
            factura.nitReceptor = nitReceptor
            # valor
            v = aprobacion.getElementsByTagName('VALOR')[0]
            valor = v.firstChild.data
            valor = valor.strip()
            factura.valor = float(valor)
            # iva
            i = aprobacion.getElementsByTagName('IVA')[0]
            iva = i.firstChild.data
            iva = iva.strip()
            factura.iva = float(iva)
            # total
            t = aprobacion.getElementsByTagName('TOTAL')[0]
            total = t.firstChild.data
            total = total.strip()
            factura.total = float(total)
            # código de aprobación
            ca = aprobacion.getElementsByTagName('CODIGO_APROBACION')[0]
            numAutorizacion = ca.firstChild.data
            numAutorizacion = numAutorizacion.strip()
            factura.numAutorizacion = numAutorizacion

            # añadiendo las facturas a la lista
            facturas.append(factura)
        # añadiendo la lista de facturas a la autorizacion
        autorizacion.facturas = facturas

        # añadiendo los autorizaciones en la lista
        autorizaciones.append(autorizacion)

    return autorizaciones


# verificaciones para cada factura
def verificaciones(facturas, autorizaciones):
    referencias = []
    if len(autorizaciones) != 0:
        for aut in autorizaciones:
            for fac in aut.facturas:
                referencias.append(fac.referencia)

    for f in facturas:
        # del tiempo solo necesitaremos la fecha
        f.fecha = re.search(r'([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})', f.fecha).group()
        
        # referencia
        if len(f.referencia) <= 40:
            if f.referencia in referencias:
                f.referencia = Error(True, 'referencia repetida')
         
            else:
                referencias.append(f.referencia)
        else:
            f.referencia = Error(True, 'referencia demasiado grande')
            continue

        # verificando el nit emisor
        f.nitEmisor = verificacionNIT(f.nitEmisor)

        # verificando el nit receptor
        f.nitReceptor = verificacionNIT(f.nitReceptor)

        if type(f.nitEmisor or f.nitReceptor or f.referencia) == Error:
            continue

        # el valor solo se verificará si es un dígito valor
        if re.search('[0-9]+([.][0-9]+)?', f.valor):
            # convirtiendo a decimal
            f.valor = float(f.valor)
        else:
            f.valor = Error(True, 'no es digito')
            continue
        
        # iva
        if re.search('[0-9]+([.][0-9]+)?', f.iva):
            iva = round(f.valor * 0.12, 2)
            # convirtiendo a decimal
            f.iva = float(f.iva)
            if not(f.iva == iva):
                f.iva = Error(True, 'iva mal calculado')
                continue
        else:
            f.iva = Error(True, 'no es digito')
            continue

        # total
        if re.search('[0-9]+([.][0-9]+)?', f.total):
            # convirtiendo a decimal
            f.total = float(f.total)
            total = f.valor + f.iva
            if not(f.total == total):
                f.total = Error(True, 'total mal calculado')
                continue
        else:
            f.total = Error(True, 'no es digito')
            continue
        
    autorizacion(facturas, autorizaciones)



# verificaciones de nits
def verificacionNIT(nit):
    inicio = len(nit) - 2
    # posicion
    n = 1
    # sumatoria
    suma = 0
    for i in range(inicio, -1, -1):
        # 1. y 2. multiplicando cada digito por su posición
        suma += int(nit[i])*n
        n += 1

    # 3. modulo 11 de la suma
    mod = suma % 11

    # 4. 11 - mod
    suma = 11 - mod

    # 5.suma mod 11
    mod = suma % 11

    # verificando si es válido o no
    if mod == 10 and nit[-1:] == 'k':
        print('nit válido')
    elif mod < 10 and nit[-1:] == str(mod):
        print('nit válido')
    else:
        nit = Error(True, 'nit invalido')
    
    return nit


# correlativos para las autorizaciones
def autorizacion(facturas, autorizaciones):
    # facturas rechazadas
    facRechazado(facturas)

    # cantidad de fechas en las facturas correctas (días)
    fechas = []

    for a in autorizaciones:
        fechas.append(a.fecha)
        
    for fac in facturas:
        # filtrando las facturas correctas
        if not fac.rechazado:
            # si es la primera factura se añadirá el día
            if len(fechas) == 0:
                fechas.append(fac.fecha)
            else:
                # bandera para saber si la fecha de la factura ya se ha registrado
                flag = False
                for f in fechas:
                    if fac.fecha == f:
                        flag = True
                # si la fecha no se ha registrado, se procede a registrarla
                if not flag:
                    fechas.append(fac.fecha)               

    contadores(facturas, fechas, autorizaciones)
                    

# descartando las facturas rechazadas
def facRechazado(facturas):
    for fac in facturas:
        if type(fac.referencia) == Error:
            fac.rechazado = True
        elif type(fac.nitEmisor) == Error:
            fac.rechazado = True
        elif type(fac.nitReceptor) == Error:
            fac.rechazado = True
        elif type(fac.valor) == Error:
            fac.rechazado = True
        elif type(fac.iva) == Error:
            fac.rechazado = True
        elif type(fac.total) == Error:
            fac.rechazado = True


# contadores para los controles de facturas
def contadores(facturas, fechas, autorizaciones):
    if len(autorizaciones) == 0:
        for f in fechas:
            print("=============================")
            # creando un objeto de tipo Autorización
            autorizacion = Autorizacion()         
            autorizacion = fechasF(facturas, autorizacion, f)
            # fecha de una autoriazación
            autorizacion.fecha = f

            # agregando cada autorización a la lista de autorizaciones
            autorizaciones.append(autorizacion)
    else:
        fechasA = []
        for autorizacion in autorizaciones:
            print('hola 1')
            print(autorizacion.fecha)
            fechasA.append(autorizacion.fecha)

        for f in fechas:
            print('hola2')
            print(f)
            if f in fechasA:
                print( "============= fecha repetida")
                for autorizacion in autorizaciones:
                    if f == autorizacion.fecha:
                        autorizacion = fechasF(facturas, autorizacion, f)
            else: 
                print( "============= fecha nueva")
                # creando un objeto de tipo Autorización
                autorizacion = Autorizacion()         
                autorizacion = fechasF(facturas, autorizacion, f)
                # fecha de una autoriazación
                autorizacion.fecha = f

                # agregando cada autorización a la lista de autorizaciones
                autorizaciones.append(autorizacion)

    # correlativo por día
    for autorizacion in autorizaciones:
        contador = 1
        for fac in autorizacion.facturas:
            # filtrando las facturas correctas
            parteFechas = autorizacion.fecha.split('/')
            # año[2], mes[1], día[0]
            fecha = parteFechas[2] + parteFechas[1] + parteFechas[0]
            fac.numAutorizacion = fecha + ('%0.8d' % contador)
            contador += 1

    # # probando
    # for a in autorizaciones:
    #     print('fecha' + a.fecha + '\nfacRecibidas' + str(a.facRecibidas) + '\neEmisor' +
    #         str(a.eEmisor) + '\neReceptor' + str(a.eReceptor) + '\neIva' + 
    #         str(a.eIva) + '\neTotal' + str(a.eTotal) + '\neReferencia' +
    #         str(a.eReferencia) + '\nfacCorrectas' + str(a.facCorrectas) + '\nemisores' +
    #         str(a.emisores) + '\nreceptores' + str(a.receptores) + '\n')

    #     for  fac in a.facturas:
    #         print(fac.numAutorizacion)

    salida(autorizaciones)
    databaseSalida(autorizaciones)


def fechasF(facturas, autorizacion, f):
    for fac in facturas:
        # filtrando por fechas
        if f == fac.fecha:        
            # factura recibida por día
            autorizacion.facRecibidas += 1
            # contando cada error por día de cada campo
            if type(fac.referencia) == Error:
                autorizacion.eReferencia += 1
            elif type(fac.nitEmisor) == Error:
                autorizacion.eEmisor += 1
            elif type(fac.nitReceptor) == Error:
                autorizacion.eReferencia += 1
            elif type(fac.iva) == Error:
                autorizacion.eIva += 1
            elif type(fac.total) == Error:
                autorizacion.eTotal += 1

            # facturas correctas
            if fac.rechazado == False:
                autorizacion.facCorrectas += 1
                
                # agregando las facturas autorizadas
                autorizacion.facturas.append(fac)
                if len(autorizacion.facturas) == 1:
                    # contando la cantidad de receptores y emisores
                    autorizacion.emisores += 1
                    autorizacion.receptores += 1
                else:
                    # revisando si no se repite el emisor o receptor
                    for a in autorizacion.facturas:
                        if a.nitEmisor != fac.nitEmisor:
                            autorizacion.emisores += 1
                        if a.nitReceptor != fac.nitReceptor:
                            autorizacion.receptores += 1 
            
    return autorizacion


# creando el xml de salida
def salida(autorizaciones):
    DOMimp = xml.dom.minidom.getDOMImplementation()
    xmlDoc = DOMimp.createDocument(None, "LISTAAUTORIZACIONES", None)
    # raíz del archivo
    docRoot = xmlDoc.documentElement

    # por cada autorización se crea un nodo
    for autorizacion in autorizaciones:
        # nodo autorizacion
        a = xmlDoc.createElement('AUTORIZACION')
        
        # nodo fecha y su contenido
        fecha = xmlDoc.createElement("FECHA")
        fecha.appendChild(xmlDoc.createTextNode(str(autorizacion.fecha)))
        # agregando la fecha al nodo autorizacion
        a.appendChild(fecha)

        # nodo facturas recibidas y su contenido
        fRecibidas = xmlDoc.createElement("FACTURAS_RECIBIDAS")
        fRecibidas.appendChild(xmlDoc.createTextNode(str(autorizacion.facRecibidas)))
        # agregando las facturas recibidas al nodo autorizacion
        a.appendChild(fRecibidas)

        # nodo errores y su contenido
        errores = xmlDoc.createElement("ERRORES")
        # nodo error nit emisor y su contenido
        eEmisor = xmlDoc.createElement("NIT_EMISOR")
        eEmisor.appendChild(xmlDoc.createTextNode(str(autorizacion.eEmisor)))
        # nodo error nit receptor y su contenido
        eReceptor = xmlDoc.createElement("NIT_RECEPTOR")
        eReceptor.appendChild(xmlDoc.createTextNode(str(autorizacion.eReceptor)))
        # nodo error iva y su contenido
        eIva = xmlDoc.createElement("IVA")
        eIva.appendChild(xmlDoc.createTextNode(str(autorizacion.eIva)))
        # nodo error total y su contenido
        eTotal = xmlDoc.createElement("TOTAL")
        eTotal.appendChild(xmlDoc.createTextNode(str(autorizacion.eTotal)))
        # nodo error referencia y su contenido
        eReferencia = xmlDoc.createElement("REFERENCIA_DUPLICADA")
        eReferencia.appendChild(xmlDoc.createTextNode(str(autorizacion.eReferencia)))       
        # agreando todos los errores al nodo errores
        errores.appendChild(eEmisor)
        errores.appendChild(eReceptor)
        errores.appendChild(eIva)
        errores.appendChild(eTotal)
        errores.appendChild(eReferencia)
        # agregando los errores al nodo autorizacion
        a.appendChild(errores)

        # nodo facturas correctas y su contenido
        facCorrectas = xmlDoc.createElement("FACTURAS_CORRECTAS")
        facCorrectas.appendChild(xmlDoc.createTextNode(str(autorizacion.facCorrectas)))       
        # agregando las facturas correctas al nodo autorizacion
        a.appendChild(facCorrectas)

        # nodo emisores y su contenido
        emisores = xmlDoc.createElement("CANTIDAD_EMISORES")
        emisores.appendChild(xmlDoc.createTextNode(str(autorizacion.emisores)))       
        # agregando los emisores al nodo autorizacion
        a.appendChild(emisores)

        # nodo receptores y su contenido
        receptores = xmlDoc.createElement("CANTIDAD_RECEPTORES")
        receptores.appendChild(xmlDoc.createTextNode(str(autorizacion.receptores)))       
        # agregando los receptores al nodo autorizacion
        a.appendChild(receptores)

        # nodo listado de autorizaciones y su contenido
        listAutorizaciones = xmlDoc.createElement("LISTADO_AUTORIZACIONES")
        for fac in autorizacion.facturas:
            # nodo aprobacion
            aprobacion = xmlDoc.createElement("APROBACION")
            # nodo nit emisor y su contenido
            nitEmisor = xmlDoc.createElement("NIT_EMISOR")
            nitEmisor.setAttribute('ref', str(fac.referencia))
            nitEmisor.appendChild(xmlDoc.createTextNode(str(fac.nitEmisor))) 
            aprobacion.appendChild(nitEmisor)  
            # nodo codigo de aprobacion y su contenido
            codAprobacion = xmlDoc.createElement("CODIGO_APROBACION")
            codAprobacion.appendChild(xmlDoc.createTextNode(str(fac.numAutorizacion))) 
            aprobacion.appendChild(codAprobacion)
            
            listAutorizaciones.appendChild(aprobacion)  

        # agregando el listado de autorizaciones al nodo autorizacion
        a.appendChild(listAutorizaciones)

        # nodo aprobaciones y su contenido
        aprobaciones = xmlDoc.createElement("TOTAL_APROBACIONES")      
        aprobaciones.appendChild(xmlDoc.createTextNode(str(autorizacion.facCorrectas)))       
        # agregando las aprobaciones al nodo autorizacion
        a.appendChild(aprobaciones)

        # añadimos el nodo autorización a la raíz del archivo
        docRoot.appendChild(a)

    # guardando el fichero en la ruta especificada (autorizacion.xml)
    archivo = open('autorizacion.xml', 'w')
    archivo.write(xmlDoc.toprettyxml())
    archivo.close()
    print("Se ha escrito el archivo con éxito! :D")


# creando el xml que nos servirá de base de datos
def databaseSalida(autorizaciones):
    DOMimp = xml.dom.minidom.getDOMImplementation()
    xmlDoc = DOMimp.createDocument(None, "LISTAAUTORIZACIONES", None)
    # raíz del archivo
    docRoot = xmlDoc.documentElement

    # por cada autorización se crea un nodo
    for autorizacion in autorizaciones:
        # nodo autorizacion
        a = xmlDoc.createElement('AUTORIZACION')
        
        # nodo fecha y su contenido
        fecha = xmlDoc.createElement("FECHA")
        fecha.appendChild(xmlDoc.createTextNode(str(autorizacion.fecha)))
        # agregando la fecha al nodo autorizacion
        a.appendChild(fecha)

        # nodo facturas recibidas y su contenido
        fRecibidas = xmlDoc.createElement("FACTURAS_RECIBIDAS")
        fRecibidas.appendChild(xmlDoc.createTextNode(str(autorizacion.facRecibidas)))
        # agregando las facturas recibidas al nodo autorizacion
        a.appendChild(fRecibidas)

        # nodo errores y su contenido
        errores = xmlDoc.createElement("ERRORES")
        # nodo error nit emisor y su contenido
        eEmisor = xmlDoc.createElement("NIT_EMISOR")
        eEmisor.appendChild(xmlDoc.createTextNode(str(autorizacion.eEmisor)))
        # nodo error nit receptor y su contenido
        eReceptor = xmlDoc.createElement("NIT_RECEPTOR")
        eReceptor.appendChild(xmlDoc.createTextNode(str(autorizacion.eReceptor)))
        # nodo error iva y su contenido
        eIva = xmlDoc.createElement("IVA")
        eIva.appendChild(xmlDoc.createTextNode(str(autorizacion.eIva)))
        # nodo error total y su contenido
        eTotal = xmlDoc.createElement("TOTAL")
        eTotal.appendChild(xmlDoc.createTextNode(str(autorizacion.eTotal)))
        # nodo error referencia y su contenido
        eReferencia = xmlDoc.createElement("REFERENCIA_DUPLICADA")
        eReferencia.appendChild(xmlDoc.createTextNode(str(autorizacion.eReferencia)))       
        # agreando todos los errores al nodo errores
        errores.appendChild(eEmisor)
        errores.appendChild(eReceptor)
        errores.appendChild(eIva)
        errores.appendChild(eTotal)
        errores.appendChild(eReferencia)
        # agregando los errores al nodo autorizacion
        a.appendChild(errores)

        # nodo facturas correctas y su contenido
        facCorrectas = xmlDoc.createElement("FACTURAS_CORRECTAS")
        facCorrectas.appendChild(xmlDoc.createTextNode(str(autorizacion.facCorrectas)))       
        # agregando las facturas correctas al nodo autorizacion
        a.appendChild(facCorrectas)

        # nodo emisores y su contenido
        emisores = xmlDoc.createElement("CANTIDAD_EMISORES")
        emisores.appendChild(xmlDoc.createTextNode(str(autorizacion.emisores)))       
        # agregando los emisores al nodo autorizacion
        a.appendChild(emisores)

        # nodo receptores y su contenido
        receptores = xmlDoc.createElement("CANTIDAD_RECEPTORES")
        receptores.appendChild(xmlDoc.createTextNode(str(autorizacion.receptores)))       
        # agregando los receptores al nodo autorizacion
        a.appendChild(receptores)

        # nodo listado de autorizaciones y su contenido
        listAutorizaciones = xmlDoc.createElement("LISTADO_AUTORIZACIONES")
        for fac in autorizacion.facturas:
            # nodo aprobacion
            aprobacion = xmlDoc.createElement("APROBACION")
            # nodo nit emisor y su contenido
            nitEmisor = xmlDoc.createElement("NIT_EMISOR")
            nitEmisor.setAttribute('ref', str(fac.referencia))
            nitEmisor.appendChild(xmlDoc.createTextNode(str(fac.nitEmisor))) 
            aprobacion.appendChild(nitEmisor)  
            # nodo nit receptor y su contenido
            nitReceptor = xmlDoc.createElement("NIT_RECEPTOR")
            nitReceptor.appendChild(xmlDoc.createTextNode(str(fac.nitReceptor))) 
            aprobacion.appendChild(nitReceptor) 
            # nodo valor y su contenido
            valor = xmlDoc.createElement("VALOR")
            valor.appendChild(xmlDoc.createTextNode(str(fac.valor))) 
            aprobacion.appendChild(valor) 
            # nodo iva y su contenido
            iva = xmlDoc.createElement("IVA")
            iva.appendChild(xmlDoc.createTextNode(str(fac.iva))) 
            aprobacion.appendChild(iva) 
            # nodo total y su contenido
            total = xmlDoc.createElement("TOTAL")
            total.appendChild(xmlDoc.createTextNode(str(fac.total))) 
            aprobacion.appendChild(total) 
            # nodo codigo de aprobacion y su contenido
            codAprobacion = xmlDoc.createElement("CODIGO_APROBACION")
            codAprobacion.appendChild(xmlDoc.createTextNode(str(fac.numAutorizacion))) 
            aprobacion.appendChild(codAprobacion)
            
            listAutorizaciones.appendChild(aprobacion)  

        # agregando el listado de autorizaciones al nodo autorizacion
        a.appendChild(listAutorizaciones)

        # nodo aprobaciones y su contenido
        aprobaciones = xmlDoc.createElement("TOTAL_APROBACIONES")      
        aprobaciones.appendChild(xmlDoc.createTextNode(str(autorizacion.facCorrectas)))       
        # agregando las aprobaciones al nodo autorizacion
        a.appendChild(aprobaciones)

        # añadimos el nodo autorización a la raíz del archivo
        docRoot.appendChild(a)

    # guardando el fichero en la ruta especificada (autorizacion.xml)
    archivo = open('database.xml', 'w')
    archivo.write(xmlDoc.toprettyxml())
    archivo.close() 

    print("Se ha escrito el archivo con éxito! :D")


def fechasHTML():
    autorizaciones = []
    db = open('database.xml', 'r')
    data = db.read()
    if len(data) != 0:
        autorizaciones = databaseCarga(autorizaciones)
        autorizaciones = ordenar(autorizaciones)
        fechas = []
        if len(autorizaciones) != 0:
            for a in autorizaciones:
                fechas.append(a.fecha)
        else:
            fechas = ''
        return fechas


def graficas(selector, inferior, superior, tipo):
    autorizaciones = []
    db = open('database.xml', 'r')
    data = db.read()
    if len(data) != 0:
        autorizaciones = databaseCarga(autorizaciones)
        resumen1(autorizaciones, selector)
        resumen2(autorizaciones, inferior, superior, tipo)


def resumen1(autorizaciones, selector):
    # Resumen de IVA por fecha y NIT
    nits = []
    ivaEmitido = []
    ivaRecivido = []
    autorizacion = None      

    for a in autorizaciones:
        if a.fecha == selector:
            autorizacion = a
            # guardando todos los nits
            for fac in a.facturas:              
                nits.append(fac.nitEmisor)
                nits.append(fac.nitReceptor)

    # nits sin repetirse
    nits = list(set(nits))

    for n in nits:
        flagE = False
        flagR = False
        for fac in autorizacion.facturas:
            if n == fac.nitEmisor:
                ivaEmitido.append(fac.iva)
                flagE = True
            if n == fac.nitReceptor:
                ivaRecivido.append(fac.iva)
                flagR = True
        if flagE == False:
            ivaEmitido.append(0)
        if flagR == False:
            ivaRecivido.append(0)

    width = 0.4
    values = numpy.arange(len(nits))
    plt.bar(values, ivaEmitido, width, label = 'IVA emitido')
    plt.bar(values+width, ivaRecivido, width, label = 'IVA recibido')
    plt.xlabel('NITS')
    plt.ylabel('IVA')
    plt.title(f'IVA en la fecha {selector}')
    plt.legend()
    plt.xticks(values, nits)
    plt.savefig('../frontend/frontend/static/img/resumenIVA')
    plt.close()


def resumen2(autorizaciones, inferior, superior, tipo):
    autorizaciones = ordenar(autorizaciones)
    print('fechas autorizadas')
    
    flag = False
    for a in autorizaciones:
        # si la fecha de la autorizacion es el límite inferior cambia a True
        if a.fecha == inferior:
            flag = True

        # si la bandera es True, agrega la fecha
        if flag:
            print(a.fecha)

        # si la fecha de la autorizacion es el límite superior cambia a False y termina las iteraciones
        if a.fecha == superior:
            flag = False
            break


# ordenando las autorizaciones por fechas
def ordenar(autorizaciones):
    fechas = []
    for a in autorizaciones:
        fechas.append(a.fecha)

    # ordena las fechas de menor a mayor (strings)
    fechas.sort(key=lambda date: datetime.strptime(date, '%d/%m/%Y'))

    aux = []
    for f in fechas:
        for a in autorizaciones:
            if f == a.fecha:
                aux.append(a)
    return aux