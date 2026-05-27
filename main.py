from nsepython import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import os
import json

# ---------------- GOOGLE SHEETS CONNECTION ---------------- #

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from GitHub Secret

google_creds = os.environ["GOOGLE_CREDENTIALS"]

creds_dict = json.loads(google_creds)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

# ---------------- GOOGLE SHEET ---------------- #

# IMPORTANT:
# Replace with your exact Google Sheet name

sheet = client.open("Nex day target").sheet1

# ---------------- STOCK LIST ---------------- #

stocks = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "EICHERMOT",
    "TATAMOTORS",
    "SBIN"
]

# ---------------- START ROW ---------------- #

row = 2

# ---------------- FETCH DATA ---------------- #

for symbol in stocks:

    try:

        print(f"Fetching data for {symbol}")

        # NSE Quote Fetch
        quote = nse_quote(symbol)

        # Safe price fetch
        ltp = quote.get('priceInfo', {}).get('lastPrice', 0)

        # Safe volume fetch
        volume = quote.get('preOpenMarket', {}).get('totalTradedVolume', 0)

        # Current Time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Data Row
        data = [[
            current_time,
            symbol,
            ltp,
            volume
        ]]

        # Update Sheet
        sheet.update(f"A{row}:D{row}", data)

        print(f"{symbol} updated successfully")

        row += 1

        # Delay to avoid NSE blocking
        time.sleep(2)

    except Exception as e:

        print(f"Error in {symbol}: {e}")

print("All Stocks Updated Successfully")
