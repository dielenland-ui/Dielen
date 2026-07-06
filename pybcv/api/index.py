from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import importlib.util

# 1. Configurar rutas absolutas locales dentro de la carpeta 'api'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Cabeceras obligatorias para evitar bloqueos de CORS en VentaChévere
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # 2. Carga dinámica absoluta apuntando a 'api/pybcv/tasas_de_cambios.py'
            ruta_tasas = os.path.join(BASE_DIR, 'pybcv', 'tasas_de_cambios.py')
            
            # Simulamos el espacio de nombres padre para resolver los 'from ._requests' internos
            especificacion = importlib.util.spec_from_file_location("pybcv.tasas_de_cambios", ruta_tasas)
            modulo_tasas = importlib.util.module_from_spec(especificacion)
            
            sys.modules["pybcv.tasas_de_cambios"] = modulo_tasas
            especificacion.loader.exec_module(modulo_tasas)
            
            # Instanciar la clase nativa de la librería local
            bcv = modulo_tasas.PyBCV()
            
            # Formatear la respuesta JSON con las tasas en tiempo real
            response_data = {
                "status": "success",
                "dolar": bcv.get_rate(currency_code='USD'),
                "euro": bcv.get_rate(currency_code='EUR')
            }
            
        except Exception as e:
            response_data = {
                "status": "error",
                "message": f"Error en ejecución del empaquetado local: {str(e)}",
                "clase_error": str(type(e).__name__)
            }

        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
