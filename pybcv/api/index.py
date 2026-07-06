from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Forzar a Python a buscar librerías dentro de la carpeta 'api'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Cabeceras para permitir que VentaChévere consulte sin bloqueos de CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        try:
            # Importamos desde la carpeta local que acabas de subir
            from pybcv import PyBCV
            bcv = PyBCV()
            
            # Extraemos las tasas usando los métodos nativos de tu carpeta
            tasas_data = {
                "status": "success",
                "dolar": bcv.get_rate(currency_code='USD'),
                "euro": bcv.get_rate(currency_code='EUR')
            }
        except Exception as e:
            # Si el código local falla por alguna razón, capturamos el error real
            tasas_data = {
                "status": "error",
                "message": f"Fallo en la librería local: {str(e)}",
                "clase_error": str(type(e).__name__)
            }

        self.wfile.write(json.dumps(tasas_data).encode('utf-8'))
