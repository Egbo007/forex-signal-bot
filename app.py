from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Paste your Telegram details here
TELEGRAM_TOKEN = '8444942829:AAGl0IeUA56KEgALw5VloUyuoNGaWcD4Rjw'  # Replace with your token from Step 2
TELEGRAM_CHAT_ID = '-1002994734036'  # Replace with your chat ID from Step 2

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

    event = data.get('event')
    direction = data.get('direction')
    pair = data.get('pair')
    entry = data.get('entry')
    price = data.get('price')
    pips = data.get('pips')
    tf = data.get('tf')
    time = data.get('time')

    if event == 'entry':
        msg = f"📢 New Forex Signal\n────────────────\n📊 Pair: {pair}\n⏱️ Timeframe: {tf}\n{'🟢' if direction == 'BUY' else '🔴'} Signal: {direction}\n💰 Entry: {entry}\n⏰ Time: {time}"
    elif 'tp' in event:
        msg = f"🎯 TP {event.upper()} Hit!\n────────────────\n📊 Pair: {pair}\n⏱️ Timeframe: {tf}\n{'🟢' if direction == 'BUY' else '🔴'} Direction: {direction}\n💰 Entry: {entry}\n🎯 Price: {price}\n📈 Pips: +{pips}\n⏰ Time: {time}"
    elif event == 'sl':
        msg = f"❌ SL Hit ({data.get('sl_type')})\n────────────────\n📊 Pair: {pair}\n⏱️ Timeframe: {tf}\n{'🟢' if direction == 'BUY' else '🔴'} Direction: {direction}\n💰 Entry: {entry}\n❌ Price: {price}\n📉 Pips: {pips}\n⏰ Time: {time}"
    elif event == 'expired':
        msg = f"⏳ Signal Expired\n────────────────\n📊 Pair: {pair}\n⏱️ Timeframe: {tf}\n{'🟢' if direction == 'BUY' else '🔴'} Direction: {direction}\n💰 Entry: {entry}\n⏳ After: {data.get('valid_hours')} hours\n⏰ Time: {time}"
    else:
        msg = f"Unknown event: {json.dumps(data)}"

    send_to_telegram(msg)

    # No Sheets logging for now - we'll add a simple file log later if needed

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
