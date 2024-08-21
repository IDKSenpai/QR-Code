from flask import Flask, send_file
import qrcode
import PIL
from PIL import Image, ImageColor
import datetime
import io

app = Flask(__name__)

@app.route('/generate-qr', methods=['GET'])
def generate_qr():
    # Define the base URL of your server-side script
    base_url = 'https://www.facebook.com/thina.oek?mibextid=ZbWKwL'

    # Set expiration date
    expiration_date = datetime.datetime(2024, 8, 22)

    # Create a unique identifier or token
    unique_token = 'userTokeWork1122'  # Replace with a secure unique token

    # Create the URL with expiration date and token
    url_with_token = f'{base_url}?token={unique_token}&expiry={expiration_date.strftime("%Y-%m-%d")}'

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url_with_token)
    qr.make(fit=True)


    # Use ImageColor.getrgb() to ensure the color is interpreted correctly
    fill_color = ImageColor.getrgb('blue')
    back_color = ImageColor.getrgb('white')
    
    # Generate QR code image with the specified colors
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # Load the logo
    logo = Image.open('Doc1.png')  # Replace with your logo file

    # Calculate logo size and position
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width / 2)
    logo = logo.resize((logo_size, logo_size), PIL.Image.Resampling.LANCZOS)
    logo_x = (qr_width - logo_size) // 2
    logo_y = (qr_height - logo_size) // 2

    # Paste logo onto QR code
    qr_img.paste(logo, (logo_x, logo_y), logo)

    # Save QR code to a bytes buffer
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qr_code_with_logo.png')

if __name__ == '__main__':
    app.run(debug=True)
