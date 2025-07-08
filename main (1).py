from flask import Flask, request, jsonify
import time
import hashlib
import hmac
import requests

app = Flask(__name__)

# Suas credenciais da API AliExpress
APP_KEY = "514670"
APP_SECRET = "XLxBYvKXURGDjsRDsuGykEt4sy9s0eIp"
TRACKING_ID = "cadadiaumcafe"

# URL da API AliExpress
ALIEXPRESS_API_URL = "https://api-sg.aliexpress.com/sync"

# Função para gerar a assinatura
def generate_signature(params: dict, app_secret: str) -> str:
    sorted_params = sorted(params.items())
    encoded_params = "".join(f"{k}{v}" for k, v in sorted_params if k and v is not None)
    to_sign = app_secret + encoded_params + app_secret
    signature = hmac.new(app_secret.encode("utf-8"), to_sign.encode("utf-8"), hashlib.sha256).hexdigest().upper()
    return signature

# Rota de busca
@app.route("/buscar", methods=["GET"])
def buscar():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Parâmetro 'keyword' é obrigatório"}), 400

    timestamp = str(int(time.time() * 1000))
    method = "aliexpress.affiliate.hotproduct.query"

    params = {
        "app_key": APP_KEY,
        "timestamp": timestamp,
        "method": method,
        "format": "json",
        "sign_method": "sha256",
        "keywords": keyword,
        "target_currency": "BRL",
        "target_language": "PT",
        "tracking_id": TRACKING_ID,
        "page_no": "1",
        "page_size": "5",
        "platform_product_type": "ALL",
        "sort": "commission_rate_desc",
    }

    signature = generate_signature(params, APP_SECRET)
    params["sign"] = signature

    try:
        response = requests.get(ALIEXPRESS_API_URL, params=params, timeout=30)
        data = response.json()
        produtos = data.get("resp_result", {}).get("result", {}).get("products", [])

        if not produtos:
            return jsonify({"error": "Nenhum produto encontrado"})

        resultado = []
        for p in produtos:
            resultado.append({
                "titulo": p.get("product_title"),
                "preco": p.get("app_sale_price"),
                "imagem": p.get("product_main_image_url"),
                "link": p.get("promotion_link")
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": "Erro inesperado na busca", "detalhe": str(e)}), 500

# Inicialização do app Flask
if __name__ == "__main__":
    app.run(debug=True)
