
from flask import Flask, request, jsonify
from aliexpress_api import AliexpressApi, models
import re, urllib.parse, os

app = Flask(__name__)

# Dados de Pedro
aliexpress = AliexpressApi(
    key='514670',
    secret='N03ZKerO5cChzHDiy4xk5jUJcxnpsHsu',
    language=models.Language.PT,
    currency=models.Currency.BRL,
    tracking_id='cadadiaumcafe'
)

# Extrair link do texto
def extract_link(text):
    link_pattern = r'https?://\S+|www\.\S+'
    links = re.findall(link_pattern, text)
    return links[0] if links else None

@app.route("/produto", methods=["POST"])
def produto():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Campo 'text' ausente no JSON"}), 400

    link = extract_link(text)

    if not link or "aliexpress.com" not in link:
        return jsonify({"error": "Link do AliExpress inválido ou ausente"}), 400

    try:
        affiliate_links = aliexpress.get_affiliate_links(link)
        affiliate_link = affiliate_links[0].promotion_link if affiliate_links else link

        details = aliexpress.get_products_details([link])
        if not details:
            return jsonify({"error": "Produto não encontrado"}), 404

        produto = details[0]

        return jsonify({
            "title": produto.product_title,
            "price": produto.target.sale_price,
            "image": produto.product_main_image_url,
            "affiliate_link": affiliate_link
        })

    except Exception as e:
        return jsonify({"error": "Erro ao processar produto", "detalhe": str(e)}), 500

@app.route("/buscar", methods=["GET"])
def buscar():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Parâmetro 'keyword' é obrigatório"}), 400

    try:
        keyword_decoded = urllib.parse.unquote(keyword)
        produtos = aliexpress.get_promotion_products(keyword=keyword_decoded, page=1, page_size=5)

        resultados = []
        for p in produtos:
            resultados.append({
                "title": p.product_title,
                "price": p.target.sale_price,
                "image": p.product_main_image_url,
                "affiliate_link": p.promotion_link
            })

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": "Erro na busca", "detalhe": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
