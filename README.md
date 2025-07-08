# AliExpress Afiliado - API Flask

Este projeto expõe um endpoint em Flask para transformar qualquer link de produto do AliExpress em:

- Link de afiliado com seu `aff_fsk`
- Título do produto
- Imagem
- Preço

Ideal para integração com Make, Telegram, bots ou automações.

---

## 📦 Como usar

### Endpoint:

POST /produto

### Corpo da requisição:
```json
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

