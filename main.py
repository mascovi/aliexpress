
from flask import Flask, request, jsonify
import hmac
import hashlib
import time
import urllib.parse
import requests
import os

app = Flask(__name__)

# Dados do Pedro
APP_KEY = "514670"
APP_SECRET = "N03ZKerO5cChzHDiy4xk5jUJcxnpsHsu"
AFF_FSK = "cadadiaumcafe"

def generate_signature(params: dict, app_secret: str) -> str:
    sorted_params = sorted((k, v) for k, v in params.items() if v is not None and k != 'sign')
    base_string = ''.join(f"{k}{v}" for k, v in sorted_params)
    signature = hmac.new(app_secret.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha256)
    return signature.hexdigest().upper()

@app.route("/buscar", methods=["GET"])
def buscar():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Parâmetro 'keyword' é obrigatório"}), 400

    try:
        timestamp = str(int(time.time() * 1000))
        method = "aliexpress.affiliate.product.query"
        keyword_decoded = urllib.parse.unquote(keyword)

        params = {
            "app_key": APP_KEY,
            "method": method,
            "timestamp": timestamp,
            "sign_method": "sha256",
            "keywords": keyword_decoded,
            "target_currency": "BRL",
            "target_language": "PT",
            "tracking_id": AFF_FSK,
            "page_size": 5,
            "page_no": 1,
            "sort": "commissionRateDown"
        }

        sign = generate_signature(params, APP_SECRET)
        params["sign"] = sign

        response = requests.get("https://api-sg.aliexpress.com/sync", params=params)
        data = response.json()

        try:
            products = data["resp_result"]["result"]["products"]
        except:
            return jsonify({"error": "Nenhum produto encontrado"}), 404

        resultados = []
        for item in products:
            resultados.append({
                "title": item.get("product_title"),
                "price": item.get("sale_price"),
                "image": item.get("product_main_image_url"),
                "affiliate_link": item.get("promotion_link")
            })

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": "Erro inesperado na busca", "detalhe": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
