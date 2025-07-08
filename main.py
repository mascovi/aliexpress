from flask import Flask, request, jsonify
import requests
import hashlib
import hmac
import time
import os

app = Flask(__name__)

# Suas credenciais
app_key = "514670"
app_secret = "XLxBYvKXURGDjsRDsuGykEt4sy9s0eIp"
tracking_id = "cadadiaumcafe"

# Função para gerar a assinatura HMAC-SHA256
def generate_signature(params: dict, app_secret: str):
    sorted_params = sorted(params.items())
    encoded_params = "".join(f"{k}{v}" for k, v in sorted_params)
    to_sign = app_secret + encoded_params + app_secret
    signature = hmac.new(
        app_secret.encode("utf-8"),
        to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest().upper()
    return signature

@app.route("/")
def home():
    return "API do AliExpress rodando."

@app.route("/buscar", methods=["GET"])
def buscar():
    try:
        keyword = request.args.get("keyword", "")
        if not keyword:
            return jsonify({"error": "Parâmetro 'keyword' é obrigatório"}), 400

        timestamp = str(int(time.time() * 1000))

        # Parâmetros obrigatórios da API
        params = {
            "app_key": app_key,
            "method": "aliexpress.affiliate.hotproduct.query",
            "sign_method": "hmac",
            "timestamp": timestamp,
            "format": "json",
            "v": "2.0",
            "fields": "product_title,product_main_image_url,product_detail_url,app_sale_price,original_price,discount,promotion_link",
            "keywords": keyword,
            "target_currency": "BRL",
            "target_language": "PT",
            "tracking_id": tracking_id,
            "page_size": "5",
        }

        # Gera assinatura e adiciona aos parâmetros
        signature = generate_signature(params, app_secret)
        params["sign"] = signature

        # Chamada à API
        url = "https://api-sg.aliexpress.com/sync"
        response = requests.get(url, params=params)
        data = response.json()

        # Valida resposta
        if data.get("resp_result", {}).get("result", {}).get("products"):
            produtos = data["resp_result"]["result"]["products"]
            resultado = []
            for produto in produtos:
                resultado.append({
                    "titulo": produto.get("product_title"),
                    "imagem": produto.get("product_main_image_url"),
                    "preco": produto.get("app_sale_price"),
                    "preco_original": produto.get("original_price"),
                    "desconto": produto.get("discount"),
                    "link": produto.get("promotion_link")
                })
            return jsonify(resultado)
        else:
            return jsonify({"error": "Nenhum produto encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Erro inesperado na busca", "detalhe": str(e)}), 500

# Corrige porta para o Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
