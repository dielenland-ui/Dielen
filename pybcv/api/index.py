from http.server import BaseHTTPRequestHandler
import json
from pybcv import PyBCV

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configurar cabeceras de respuesta para el navegador (Evita error de CORS)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        try:
            # Inicializar la librería que Vercel instaló por su cuenta
            bcv = PyBCV()
            
            # Extraer las tasas en formato de diccionario limpio
            tasas_data = {
                "status": "success",
                "dolar": bcv.get_rate(currency_code='USD'),
                "euro": bcv.get_rate(currency_code='EUR')
            }
        except Exception as e:
            # Si el BCV está caído o hay error, responde esto
            tasas_data = {
                "status": "error",
                "message": str(e)
            }

        # Convertir a JSON y enviar la respuesta al frontend de VentaChévere
        self.wfile.write(json.dumps(tasas_data).encode('utf-8'))