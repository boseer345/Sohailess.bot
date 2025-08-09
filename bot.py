import requests
import time

# Your Telegram Bot API token and Chat ID
BOT_TOKEN = "8456776121:AAFrF4U4FR9YJQpw68dFWsKd6wrbSz43MeI"
CHAT_ID = "5446816321"  # personal chat ID or group ID

# Dexscreener API URL for latest pairs
DEX_API = "https://api.dexscreener.com/latest/dex/tokens"

# Keep track of tokens already sent
sent_tokens = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

def check_new_tokens():
    try:
        response = requests.get(DEX_API)
        data = response.json()
        for pair in data.get("pairs", []):
            token_address = pair.get("baseToken", {}).get("address", "")
            token_name = pair.get("baseToken", {}).get("name", "Unknown")
            token_symbol = pair.get("baseToken", {}).get("symbol", "")
            price_usd = pair.get("priceUsd", "N/A")

            if token_address not in sent_tokens:
                sent_tokens.add(token_address)
                message = (
                    f"🚀 New Token Listed!\n\n"
                    f"Name: {token_name} ({token_symbol})\n"
                    f"Price: ${price_usd}\n"
                    f"Chart: {pair.get('url', '')}"
                )
                send_message(message)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        check_new_tokens()
        time.sleep(60)  # check every 1 minute
