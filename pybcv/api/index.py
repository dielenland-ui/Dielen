from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import importlib.util

# 1. Configurar rutas absolutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Forzar a Python a reconocer la carpeta raíz de la función
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # 2. Carga dinámica absoluta para burlar el error de paquete relativo
            ruta_tasas = os.path.join(BASE_DIR, 'pybcv', 'tasas_de_cambios.py')
            
            # Definimos el nombre del módulo simulando la jerarquía completa
            especificacion = importlib.util.spec_from_file_location("pybcv.tasas_de_cambios", ruta_tasas)
            modulo_tasas = importlib.util.module_from_spec(especificacion)
            
            # Registramos el módulo formalmente en el sistema antes de ejecutarlo
            sys.modules["pybcv.tasas_de_cambios"] = modulo_tasas
            especificacion.loader.exec_module(modulo_tasas)
            
            # Instanciamos la clase de tu carpeta local
            bcv = modulo_tasas.PyBCV()
            
            # Extraemos los datos del BCV
            response_data = {
                "status": "success",
                "dolar": bcv.get_rate(currency_code='USD'),
                "euro": bcv.get_rate(currency_code='EUR')
            }
            
        except Exception as e:
            response_data = {
                "status": "error",
                "message": f"Error en ejecución del empaquetado: {str(e)}",
                "clase_error": str(type(e).__name__)
            }

        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
