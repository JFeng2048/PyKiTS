# -*- coding:utf-8 -*-
"""
二维码生成器
pip install qrcode
pip install Pillow
"""
from io import BytesIO
import base64
import qrcode

def pay_alipay_qr_code(payment_url: str):
    """生成支付二维码工具"""
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payment_url)
    qr.make(fit=True)

    # 创建二维码图片
    img = qr.make_image(fill_color="black", back_color="white")

    # 将图片保存到内存中
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return img_str

if __name__ == '__main__':
    print(pay_alipay_qr_code('uuu'))