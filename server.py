from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/trends', methods=['POST'])
def get_trends():
    data = request.get_json()
    keyword = data.get('keyword', 'Crédito Habitação')

    pytrends = TrendReq(hl='pt-BR', tz=0)
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='PT', gprop='youtube')

    trends_data = pytrends.interest_over_time()

    if trends_data.empty:
        return jsonify({"error": "No data found for this keyword"}), 404
    
    return jsonify(trends_data.to_dict()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
