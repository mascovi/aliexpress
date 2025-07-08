
AliExpress Afiliado - API Flask

Este projeto expõe um endpoint em Flask para transformar qualquer link de produto do AliExpress em:

- Link de afiliado com seu aff_fsk
- Título do produto
- Imagem
- Preço

Ideal para integração com Make, Telegram, bots ou automações.

---

📦 Como usar

Endpoint:
POST /produto

Corpo da requisição:
{
  "url": "https://www.aliexpress.com/item/3256805354456256.html"
}

Resposta:
{
  "product_id": "3256805354456256",
  "title": "Título do Produto",
  "price": "87.90",
  "image": "https://...",
  "affiliate_link": "https://s.click.aliexpress.com/..."
}

---

🧪 Testes e Deploy

- Usar via Render, Make ou outro sistema HTTP
- Autenticado com App Key e Secret pessoais (já incluídos no código)
- Não é necessário rodar bot Telegram

---

✅ Requisitos

- Python 3.8+
- Flask
- Requests

Instalar com:
pip install -r requirements.txt

---

ℹ️ Observação

Este projeto não utiliza bibliotecas não oficiais e é baseado diretamente na API oficial do AliExpress Partner:
https://portals.aliexpress.com/help/api.htm
