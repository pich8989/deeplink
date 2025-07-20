from flask import Flask, request, render_template_string
import qrcode
app = Flask(__name__)

# Google Analytics Config
GA_MEASUREMENT_ID = 'G-4Q9LVZB1XK'

APP_SCHEME = "http://mis.ncdd.gov.kh/isaf/"
IOS_APP_ID = "1485492588"
ANDROID_PACKAGE_NAME = "kh.gov.ncdd.isaf"

IOS_STORE_URL = f"https://apps.apple.com/kh/app/isaf-cambodia/id{IOS_APP_ID}"
ANDROID_STORE_URL = f"https://play.google.com/store/apps/details?id={ANDROID_PACKAGE_NAME}&hl=en"

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
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{GA_MEASUREMENT_ID}');
        </script>

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
                let didOpen = false;

                window.location = "{APP_SCHEME}";

                document.addEventListener('visibilitychange', function () {{
                    if (document.hidden) {{
                        didOpen = true;
                    }}
                }});

                setTimeout(function () {{
                    if (!didOpen) {{
                        document.getElementById("message").innerText = "App not found. Redirecting to store...";
                        window.location = "{store_url}";
                    }} else {{
                        document.getElementById("message").innerText = "App opened successfully 🎉";
                    }}
                }}, 2500);
            }}
        </script>
    </head>
    <body>
        <h1 align="center">ISAF App Launcher</h1>
        <div align="center">
            <button onclick="openApp()">Open App</button>
        </div>
        <div id="message"></div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # Only generate QR code once when the script starts
    qr_url = "http://127.0.0.1:5000/open#" #our live domain
    qr_img = qrcode.make(qr_url)
    qr_img.save("render_isaf_qr1.png")
    print("✅ QR saved as render_isaf_qr.png")
    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
