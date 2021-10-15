
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


class Fecha(object):
    def __init__(self, fecha):
        self.fecha = fecha
        self.contador = 1

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
        self.facCorrectas = 0
        self.emisores = 0
        self.receptores = 0
        self.facturas = []
            