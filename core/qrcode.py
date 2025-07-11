import qrcode

def qrcode(url, user):
    qr = qrcode.QRCode(
        version=1,  # tamanho do QR Code (1 é o menor)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # tamanho de cada caixa do QR
        border=4,  # borda do QR
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"media/qr/qr_{user}.png")
    