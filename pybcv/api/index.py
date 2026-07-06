from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# 1. FIX DE RUTAS ABSOLUTAS: Detectar con precisión dónde está corriendo el servidor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(BASE_DIR, 'pybcv')

# Inyectar las rutas en el sistema de búsqueda de Python en orden de prioridad
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configuración de cabeceras seguras para VentaChévere (Evita bloqueos de CORS)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Importación directa desde el archivo core de la librería local
            from tasas_de_cambios import PyBCV
            bcv = PyBCV()
            
            # Obtener los datos oficiales del BCV en tiempo real
            dolar_bcv = bcv.get_rate(currency_code='USD')
            euro_bcv = bcv.get_rate(currency_code='EUR')
            
            # Respuesta exitosa estructurada en JSON limpio
            response_data = {
                "status": "success",
                "dolar": dolar_bcv,
                "euro": euro_bcv
            }
            
        except ImportError as ie:
            response_data = {
                "status": "error",
                "message": f"Error crítico de importación. Verifica que los archivos (.py) de la segunda foto estén dentro de api/pybcv/. Detalle: {str(ie)}",
                "clase_error": "ImportError"
            }
        except Exception as e:
            response_data = {
                "status": "error",
                "message": f"Fallo al conectar o extraer datos del BCV: {str(e)}",
                "clase_error": str(type(e).__name__)
            }

        # Retornar el resultado al navegador/frontend
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    # Manejar peticiones previas que hacen los navegadores por seguridad (Preflight requests)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
