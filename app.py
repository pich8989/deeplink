from flask import Flask, request, render_template_string
import qrcode

app = Flask(__name__)

# App config
APP_SCHEME = "http://mis.ncdd.gov.kh/isaf/"
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
                padding-top: 50px;
            }}
            #message {{
                margin-top: 30px;
                font-size: 18px;
                color: #333;
            }}
            button {{
                padding: 10px 20px;
                font-size: 18px;
            }}
        </style>
        <script>
            function openApp() {{
                const now = Date.now();
                document.getElementById('message').innerText = "Launching your app...";

                window.location = "isaf://";  // Use your real app scheme

                setTimeout(function () {{
                    const elapsed = Date.now() - now;
                    if (elapsed < 1500) {{
                        document.getElementById('message').innerText = "⚠️ No app found. Please install it first.";
                        // Optional: redirect to store
                        window.location = "{store_url}";
                    }}
                }}, 1200);
            }}
        </script>
    </head>
    <body>
        <h1>ISAF App Launcher</h1>
        <button onclick="openApp()">Open App</button>
        <div id="message"></div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # Only generate QR code once when the script starts
    url = "http://192.168.0.74:5000/open"  # Replace with your IP/domain
    qr = qrcode.make(url)
    qr.save("isaf_qr_deeplink1.png")
    print("✅ QR code saved as isaf_qr.png")

    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
