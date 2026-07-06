from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Obtener la ruta exacta de la carpeta donde está este archivo (api/)
ruta_api = os.path.dirname(os.path.abspath(__file__))

# Forzar a Python a mirar dentro de 'api' y dentro de 'api/pybcv'
sys.path.append(ruta_api)
sys.path.append(os.path.join(ruta_api, 'pybcv'))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        try:
            # Importamos directamente la clase PyBCV desde el archivo tasas_de_cambios.py
            # Esto se salta el intermediario de __init__.py si está generando conflicto
            from tasas_de_cambios import PyBCV
            bcv = PyBCV()
            
            tasas_data = {
                "status": "success",
                "dolar": bcv.get_rate(currency_code='USD'),
                "euro": bcv.get_rate(currency_code='EUR')
            }
        except Exception as e:
            tasas_data = {
                "status": "error",
                "message": f"Error ejecutando modulo directo: {str(e)}",
                "clase_error": str(type(e).__name__)
            }

        self.wfile.write(json.dumps(tasas_data).encode('utf-8'))
