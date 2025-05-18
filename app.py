import json
import os
from flask import Flask, request
from utils.trading import trade_logic
from utils.discord import send_discord_alert
from utils.logger import log_trade
from utils.watchdog import restart_on_error
from ui.main_ui import launch_ui

app = Flask(__name__)

# Read config file
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Initialize the trade profile
profile = config["profile"]

# Start the UI
launch_ui(profile)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")

    if data["type"] == "buy":
        result = trade_logic("buy", profile)
        log_trade(result)
        send_discord_alert(result)
        return "Buy trade executed", 200

    elif data["type"] == "sell":
        result = trade_logic("sell", profile)
        log_trade(result)
        send_discord_alert(result)
        return "Sell trade executed", 200

    return "Invalid type", 400

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        restart_on_error(e)
