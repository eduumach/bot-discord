from flask import Flask
import threading
import bot  # Importe o módulo do seu bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo à minha aplicação web!"

def run_bot():
    bot.run()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    app.run(host='0.0.0.0', port=8080)
