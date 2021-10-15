from clases import Factura, Error, Fecha, Autorizacion
import xml.dom.minidom 
import re

# las autorizaciones única variable global
autorizaciones = []

# xml de entrada a lista de objetos
def xmlF():
    facturas = []
    archivo = open('solicitud.xml', 'r+')
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
    # invirtiendo la lista
    #facturas = list(reversed(facturas))
    verificaciones(facturas)


# verificaciones para cada factura
def verificaciones(facturas):
    referencias = []
    for f in facturas:
        # del tiempo solo necesitaremos la fecha
        f.fecha = re.search(r'([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})', f.fecha).group()
        
        # referencia
        if len(f.referencia) <= 40:
            if f.referencia in referencias:
                f.referencia = Error(True, 'referencia repetida')
                print('referencia duplicada')          
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
        
    # volviendo a invertir la lista como estaba originalmente
    #facturas = list(reversed(facturas))
    autorizacion(facturas)



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
def autorizacion(facturas):
    # facturas rechazadas
    facRechazado(facturas)

    # cantidad de fechas en las facturas correctas (días)
    fechas = []
    for fac in facturas:
        # filtrando las facturas correctas
        if not fac.rechazado:
            # si es la primera factura se añadirá el día
            if len(fechas) == 0:
                fechas.append(Fecha(fac.fecha))
            else:
                # bandera para saber si la fecha de la factura ya se ha registrado
                flag = False
                for f in fechas:
                    if fac.fecha == f.fecha:
                        flag = True
                # si la fecha no se ha registrado, se procede a registrarla
                if not flag:
                    fechas.append(Fecha(fac.fecha))
                    
    # correlativo por día
    for fac in facturas:
        # filtrando las facturas correctas
        if not fac.rechazado:
            for f in fechas:
                if fac.fecha == f.fecha:
                    parteFechas = f.fecha.split('/')
                    # año[2], mes[1], día[0]
                    fecha = parteFechas[2] + parteFechas[1] + parteFechas[0]
                    fac.numAutorizacion = fecha + ('%0.8d' % f.contador)
                    f.contador += 1

    contadores(facturas, fechas)
                    

# descartando las facturas rechazadas
def facRechazado(facturas):
    for fac in facturas:
        if type(fac.referencia) == Error:
            print('soi un error de referencia')
            fac.rechazado = True
        elif type(fac.nitEmisor) == Error:
            print('soi un error de nit emisor')
            fac.rechazado = True
        elif type(fac.nitReceptor) == Error:
            print('soi un error de nit receptor')
            fac.rechazado = True
        elif type(fac.valor) == Error:
            print('soi un error de valor')
            fac.rechazado = True
        elif type(fac.iva) == Error:
            print('soi un error de iva')
            fac.rechazado = True
        elif type(fac.total) == Error:
            print('soi un error de total')
            fac.rechazado = True


# contadores para los controles de facturas
def contadores(facturas, fechas):
    if len(autorizaciones) == 0:
        for f in fechas:
            # creando un objeto de tipo Autorización
            autorizacion = Autorizacion()         
            autorizacion = fechasF(facturas, autorizacion, f)
            # fecha de una autoriazación
            autorizacion.fecha = f.fecha

            # agregando cada autorización a la lista de autorizaciones
            autorizaciones.append(autorizacion)
    else:
        for autorizacion in autorizaciones:
            fechasF(facturas, autorizacion, autorizacion.fecha)

    # probando
    for a in autorizaciones:
        print('fecha' + a.fecha + '\nfacRecibidas' + str(a.facRecibidas) + '\neEmisor' +
            str(a.eEmisor) + '\neReceptor' + str(a.eReceptor) + '\neIva' + 
            str(a.eIva) + '\neTotal' + str(a.eTotal) + '\neReferencia' +
            str(a.eReferencia) + '\nfacCorrectas' + str(a.facCorrectas) + '\nemisores' +
            str(a.emisores) + '\nreceptores' + str(a.receptores) + '\n')

        for  fac in a.facturas:
            print(fac.numAutorizacion)

    salida(autorizaciones)


def fechasF(facturas, autorizacion, f):
    for fac in facturas:
        # filtrando por fechas
        if f.fecha == fac.fecha:
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
        eReferencia = xmlDoc.createElement("TOTAL")
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


    # guardando el fichero en la ruta especificada
    archivo = open('autorizacion.xml', 'w')
    archivo.write(xmlDoc.toprettyxml())
    archivo.close()
    print("Se ha escrito el archivo con éxito! :D")