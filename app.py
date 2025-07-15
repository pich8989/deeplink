from flask import Flask, request, render_template_string
import qrcode

app = Flask(__name__)

# App config
APP_SCHEME = "isaf://"
IOS_APP_ID = "1485492588"
ANDROID_PACKAGE_NAME = "kh.gov.ncdd.isaf"

IOS_STORE_URL = f"https://apps.apple.com/kh/app/isaf-cambodia/id{IOS_APP_ID}"
ANDROID_STORE_URL = f"https://play.google.com/store/apps/details?id={ANDROID_PACKAGE_NAME}&hl=en"

# Flask route
@app.route('/open')
def open_app():
    user_agent = request.headers.get('User-Agent', '').lower()

    if 'iphone' in user_agent or 'ipad' in user_agent:
        store_url = IOS_STORE_URL
    elif 'android' in user_agent:
        store_url = ANDROID_STORE_URL
    else:
        store_url = "#"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Open ISAF App</title>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
                margin-top: 100px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 18px;
            }}
        </style>
        <script>
            function openApp() {{
                var now = Date.now();
                window.location = "{APP_SCHEME}";
                setTimeout(function () {{
                    if (Date.now() - now < 2500) {{
                        window.location = "{store_url}";
                    }}
                }}, 2000);
            }}
        </script>
    </head>
    <body>
        <h1>Open the ISAF App</h1>
        <p>If you have the app installed, click below to open it.</p>
        <button onclick="openApp()">Open App</button>
        <p style="margin-top:20px;">If nothing happens, <a href="{store_url}">click here to install the app</a>.</p>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # Only generate QR code once when the script starts
    url = "http://10.59.17.246:5000/open"  # Replace with your IP/domain
    qr = qrcode.make(url)
    qr.save("isaf_qr.png")
    print("✅ QR code saved as isaf_qr.png")

    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
