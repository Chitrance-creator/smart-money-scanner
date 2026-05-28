from nsepython import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import os
import json

# ---- GOOGLE SHEETS CONNECTION ---- #

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

google_creds = os.environ.get("GOOGLE_CREDENTIALS")
if not google_creds:
    raise RuntimeError("GOOGLE_CREDENTIALS env var set nahi hai (GitHub Actions secret/env check karo)")

creds_dict = json.loads(google_creds)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

# ---- GOOGLE SHEET ---- #

sheet = client.open("Nex day target").sheet1

# ---- STOCK LIST ---- #

stocks = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "EICHERMOT",
    "TATAMOTORS",
    "SBIN"
]

row = 2

for symbol in stocks:
    try:
        print(f"Fetching data for {symbol}")

        quote = nse_quote(symbol)

        ltp = quote.get("priceInfo", {}).get("lastPrice", 0)
        volume = quote.get("preOpenMarket", {}).get("totalTradedVolume", 0)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = [[current_time, symbol, ltp, volume]]

        sheet.update(f"A{row}:D{row}", data)

        print(f"{symbol} updated successfully")

        row += 1
        time.sleep(2)

    except Exception as e:
        print(f"Error in {symbol}: {e}")

print("All Stocks Updated Successfully")
