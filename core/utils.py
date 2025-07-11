import uuid
from requests import post
import qrcode
from PIL import Image
import os
API_URL = "https://api.chatgoon.com.br/api/messages/send"
TOKEN = "0fc6d24b-04d6-4158-8caf-57b5411de484"

def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code

def enviar_mensagem(numeros, mensagem):
        HEADERS_JSON = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        for numero in numeros:
            data = {
                "number": numero,
                "body": mensagem
            }
            try:
                response = post(API_URL, json=data, headers=HEADERS_JSON)

                if response.status_code == 200:
                    print(f"✅ Mensagem enviada para {numero}")
                else:
                    print(f"❌ Erro ao enviar mensagem para {numero}: {response.status_code} - {response.text}")

            except Exception as e:
                print(f"❌ Erro ao enviar para {numero}: {e}")


def gerar_qrcode_sobre_imagem(url, user, caminho_fundo, caminho_saida):
    if not os.path.exists(caminho_fundo):
        fundo = Image.new("RGB", (500, 500), color="white")
        fundo.save(caminho_fundo)

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    bg = Image.open(caminho_fundo).convert("RGB")
    qr_img = qr_img.resize((330, 330))

    x = bg.width - qr_img.width - 370
    y = bg.height - qr_img.height - 200

    bg.paste(qr_img, (x, y))
    bg.save(caminho_saida)  # Salva só no caminho final
    return caminho_saida