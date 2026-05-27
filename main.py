from nsepython import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import time

# ---------------- GOOGLE SHEETS CONNECTION ---------------- #

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

# GOOGLE SHEET NAME

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

        quote = nse_quote(symbol)

        ltp = quote['priceInfo']['lastPrice']

        volume = quote['securityWiseDP']['quantityTraded']

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = [
            [
                current_time,
                symbol,
                ltp,
                volume
            ]
        ]

        sheet.update(f"A{row}:D{row}", data)

        print(f"{symbol} updated successfully")

        row += 1

        time.sleep(2)

    except Exception as e:

        print(f"Error in {symbol}: {e}")

print("All Stocks Updated Successfully")
