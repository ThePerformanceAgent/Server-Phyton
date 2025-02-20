import time
from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/trends', methods=['POST'])
def get_trends():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'Crédito Habitação')

        app.logger.info(f"Recebendo keyword: {keyword}")

        # Adiciona um delay para evitar bloqueio do Google
        time.sleep(5)  # Espera 5 segundos antes de consultar

        pytrends = TrendReq(hl='pt-BR', tz=0)
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='PT', gprop='youtube')

        trends_data = pytrends.interest_over_time()

        if trends_data.empty:
            app.logger.warning("Nenhum dado retornado pelo Pytrends")
            return jsonify({"error": "No data found for this keyword"}), 404

        return jsonify(trends_data.to_dict()), 200

    except Exception as e:
        app.logger.error(f"Erro no servidor: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
