from flask import Flask, jsonify
from flask_cors import CORS
from pybcv import PyBCV  # Ahora se importa directo, sin rutas raras
import os

app = Flask(__name__)
CORS(app)  # Permite que VentaChévere consulte la API desde cualquier dispositivo

@app.route('/api', methods=['GET'])
def obtener_tasas():
    try:
        # Instanciamos la librería oficial instalada por Pip
        bcv = PyBCV()
        
        # Extraemos las tasas oficiales en tiempo real
        dolar_bcv = bcv.get_rate(currency_code='USD')
        euro_bcv = bcv.get_rate(currency_code='EUR')
        
        return jsonify({
            "status": "success",
            "dolar": dolar_bcv,
            "euro": euro_bcv
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Fallo al consultar pybcv en el servidor: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
