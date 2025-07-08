from flask import Flask, request, jsonify
import hmac
import hashlib
import time
import urllib.parse
import requests
import os

app = Flask(__name__)

# Dados da sua conta
APP_KEY = "514670"
APP_SECRET = "N03ZKerO5cChzHDiy4xk5jUJcxnpsHsu"
AFF_FSK = "cadadiaumcafe"

def extract_product_id(url):
    try:
        clean = url.split('/')[-1]
        return clean.split(".")[0]
    except:
        return None

def generate_signature(params: dict, app_secret: str) -> str:
    sorted_params = sorted((k, v) for k, v in params.items() if v is not None and k != 'sign')
    base_string = ''.join(f"{k}{v}" for k, v in sorted_params)
    signature = hmac.new(app_secret.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha256)
    return signature.hexdigest().upper()

@app.route("/produto", methods=["POST"])
def get_product_info():
    data = request.json
    url = data.get("url")

    if not url or "aliexpress.com/item/" not in url:
        return jsonify({"error": "URL inválida do AliExpress"}), 400

    product_id = extract_product_id(url)
    if not product_id:
        return jsonify({"error": "Não foi possível extrair o ID do produto"}), 400

    method = "aliexpress.affiliate.productdetail.get"
    timestamp = str(int(time.time() * 1000))
    params = {
        "app_key": APP_KEY,
        "method": method,
        "timestamp": timestamp,
        "sign_method": "sha256",
        "product_ids": product_id,
        "target_currency": "BRL",
        "target_language": "PT",
        "tracking_id": AFF_FSK
    }

    sign = generate_signature(params, APP_SECRET)
    params["sign"] = sign

    url_api = "https://api-sg.aliexpress.com/sync"
    response = requests.get(url_api, params=params)
    
    try:
        result = response.json()
        item = result["resp_result"]["result"]["products"][0]
        return jsonify({
            "product_id": item["product_id"],
            "title": item["product_title"],
            "price": item["sale_price"],
            "image": item["product_main_image_url"],
            "affiliate_link": item["promotion_link"]
        })
    except Exception as e:
        return jsonify({"error": "Erro ao buscar dados do produto", "detalhe": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
