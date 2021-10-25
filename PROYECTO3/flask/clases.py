class Factura(object):
    def __init__(self):
        self.fecha = ''
        self.referencia = ''
        self.nitEmisor = ''
        self.nitReceptor = ''
        self.valor = float
        self.iva = float
        self.total = float
        self.numAutorizacion = None
        self.rechazado = False


class Error(object):
    def __init__(self, flag, error):
        self.flag = flag
        self.error = error


class Grafica(object):
    def __init__(self, fecha, nits, ivaEmitido, ivaRecivido):
        self.fecha = fecha
        self.nits = nits
        self.ivaEmitido = ivaEmitido
        self.ivaRecibido = ivaRecivido
        self.monto = []

class Autorizacion(object):
    def __init__(self):
        self.fecha = ''
        self.facRecibidas = 0
        # ------------ errores -------------------
        self.eEmisor = 0
        self.eReceptor = 0
        self.eIva = 0
        self.eTotal = 0
        self.eReferencia = 0
        # ------------ termina errores -------------------
        self.facCorrectas = 0
        self.emisores = 0
        self.receptores = 0
        self.facturas = []
            