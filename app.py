# from flask import Flask, request, render_template_string
# import qrcode
# app = Flask(__name__)

# # Google Analytics Config

# GA_MEASUREMENT_ID = 'G-4Q9LVZB1XK'

# APP_SCHEME = "http://saft" # That url for can open the app if app is installed on the device
# IOS_APP_ID = "1485492588" # This is the App Store ID for iOS
# ANDROID_PACKAGE_NAME = "kh.gov.ncdd.isaf" # This is the package name for Android

# IOS_STORE_URL = f"https://apps.apple.com/kh/app/isaf-cambodia/id{IOS_APP_ID}" # This is the App Store URL for iOS
# ANDROID_STORE_URL = f"https://play.google.com/store/apps/details?id={ANDROID_PACKAGE_NAME}&hl=en" # This is the Play Store URL for Android

# @app.route('/open')
# def open_app():
#     user_agent = request.headers.get('User-Agent', '').lower()

#     if 'iphone' in user_agent or 'ipad' in user_agent:
#         store_url = IOS_STORE_URL
#     elif 'android' in user_agent:
#         store_url = ANDROID_STORE_URL
#     else:
#         store_url = "#"

#     return render_template_string(f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Open ISAF App</title>
#         <!-- Google tag (gtag.js) -->
#         <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
#         <script>
#           window.dataLayer = window.dataLayer || [];
#           function gtag(){{dataLayer.push(arguments);}}
#           gtag('js', new Date());

#           gtag('config', '{GA_MEASUREMENT_ID}');
#         </script>

#         <style>
#         body {{
#             font-family: sans-serif;
#             text-align: center;
#             padding-top: 50px;
#         }}
#         #message {{
#             margin-top: 30px;
#             font-size: 18px;
#             color: #333;
#         }}
#         button {{
#             padding: 10px 20px;
#             font-size: 18px;
#         }}
#         </style>

#         <script>
#             function openApp() {{
#                 const now = Date.now();
#                 let didOpen = false;

#                 window.location = "{APP_SCHEME}";

#                 document.addEventListener('visibilitychange', function () {{
#                     if (document.hidden) {{
#                         didOpen = true;
#                     }}
#                 }});

#                 setTimeout(function () {{
#                     if (!didOpen) {{
#                         document.getElementById("message").innerText = "App not found. Redirecting to store...";
#                         window.location = "{store_url}";
#                     }} else {{
#                         document.getElementById("message").innerText = "App opened successfully 🎉";
#                     }}
#                 }}, 2500);
#             }}
#         </script>
#     </head>
#     <body>
#         <h1 align="center">ISAF App Launcher</h1>
#         <div align="center">
#             <button onclick="openApp()">Open App</button>
#         </div>
#         <div id="message"></div>
#     </body>
#     </html>
#     """)

# if __name__ == "__main__":
#     # Only generate QR code once when the script starts
#     qr_url = "http://10.219.243.246:5000/open" #our live domain
#     qr_img = qrcode.make(qr_url)
#     qr_img.save("render_isaf_qr.png")
#     print("✅ QR saved as render_isaf_qr.png")
#     # Start Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, render_template_string
import qrcode
app = Flask(__name__)

# App config
APP_SCHEME = "isaf://"  # Must be correct for app to open
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
        store_url = "#"  # fallback

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
    
url = "http://10.219.243.246:5000/open"  # Replace with your IP or domain

qr = qrcode.make(url)
qr.save("isaf_qr.png")
print("QR code saved as isaf_qr.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
