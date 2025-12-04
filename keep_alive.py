from threading import Thread
from flask import Flask
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot đang chạy Polling 24/7. Thân gửi từ Render!"

def run():
    # Chạy máy chủ Flask trên cổng 8080 (Render sẽ cung cấp PORT này)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

def keep_alive():
    # Chạy máy chủ Flask trên một luồng riêng
    t = Thread(target=run)

    t.start()
