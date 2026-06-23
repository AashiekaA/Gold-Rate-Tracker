import requests
import re
import pandas as pd
import gspread
import smtplib
import os
from email.mime.text import MIMEText
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path

def update_google_sheet(date, scheme, rate, investment, grams, diff_text):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("GRT Gold Tracker").sheet1

    records = sheet.get_all_values()

    yesterday_rate = None

    if len(records) > 1:

        last_row = records[-1]

        if len(last_row) > 2 and last_row[0] != date:

            yesterday_rate = int(last_row[2])

        found_row = None

        for idx, row in enumerate(records[1:], start=2):

            if len(row) > 0 and row[0] == date:
                found_row = idx
                break

        values = [
        date,
        scheme,
        rate,
        investment,
        grams,
        diff_text
    ]

        if found_row:

            sheet.update(
                [values],
                f"A{found_row}:F{found_row}"  
            )

            print("Google Sheet row updated")

        else:

            sheet.append_row(values)

            print("Google Sheet row added")

        return yesterday_rate

def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(NOTIFICATION_EMAILS)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_USER,
            NOTIFICATION_EMAILS,
            msg.as_string()
        )

    print("Email sent")


# -----------------------------
# CONFIGURATION
# -----------------------------
with open("config.json", "r") as f:
    config = json.load(f)


INVESTMENT_AMOUNT = config["current_investment_amount"]
SCHEME_NAME = config["scheme_name"]
NOTIFICATION_EMAILS = config["notification_emails"]

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

CSV_FILE = "gold_tracker.csv"

# -----------------------------
# FETCH GRT WEBSITE
# -----------------------------
url = "https://www.grtjewels.com/"

response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch website")
    exit()

html = response.text

# -----------------------------
# EXTRACT 22K RATE
# -----------------------------
match = re.search(
    r'GOLD\s+22\s+KT/1g\s*-\s*₹\s*(\d+)',
    html
)

if not match:
    print("22K gold rate not found")
    exit()

rate = int(match.group(1))

# -----------------------------
# CALCULATE GRAMS
# -----------------------------
grams = round(INVESTMENT_AMOUNT / rate, 4)

today = datetime.now().strftime("%Y-%m-%d")

new_row = {
    "Date": today,
    "Rate": rate,
    "Investment": INVESTMENT_AMOUNT,
    "Grams": grams
}

# -----------------------------
# CREATE / UPDATE CSV
# -----------------------------
if Path(CSV_FILE).exists():

    df = pd.read_csv(CSV_FILE)

    if today in df["Date"].astype(str).values:

        df.loc[
            df["Date"].astype(str) == today,
            ["Rate", "Investment", "Grams"]
        ] = [
            rate,
            INVESTMENT_AMOUNT,
            grams
        ]

        print("Today's record updated")

    else:

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        print("New record added")

else:

    df = pd.DataFrame([new_row])

    print("Tracker file created")

# Save file
df.to_csv(CSV_FILE, index=False)


yesterday_rate = update_google_sheet(
    today,
    SCHEME_NAME,
    rate,
    INVESTMENT_AMOUNT,
    grams,
    "N/A"
)

if yesterday_rate is not None:

    rate_difference = rate - yesterday_rate

    if rate_difference > 0:
        diff_text = f"+₹{rate_difference}"
    elif rate_difference < 0:
        diff_text = f"-₹{abs(rate_difference)}"
    else:
        diff_text = "₹0"

else:

    diff_text = "N/A"
    yesterday_rate = "N/A"

update_google_sheet(
    today,
    SCHEME_NAME,
    rate,
    INVESTMENT_AMOUNT,
    grams,
    diff_text
)


# -----------------------------
# MONTHLY ANALYSIS
# -----------------------------
month_low = df["Rate"].min()
month_high = df["Rate"].max()

best_grams = round(INVESTMENT_AMOUNT / month_low, 4)

email_body = f"""
Date: {today}

22K Gold Rate: ₹{rate}

Yesterday's Rate: ₹{yesterday_rate}
Difference from Yesterday: {diff_text}

Investment Amount: ₹{INVESTMENT_AMOUNT}

Weight Acquired: {grams} g

Monthly Low Rate: ₹{month_low}
Monthly High Rate: ₹{month_high}

Best Possible Grams: {best_grams} g
"""

# -----------------------------
# OUTPUT
# -----------------------------
print("\n----------------------------------")
print(f"Today's Date      : {today}")
print(f"22K Gold Rate     : ₹{rate}")
print(f"Yesterday Rate    : ₹{yesterday_rate}")
print(f"Day Change        : {diff_text}")
print(f"Investment Amount : ₹{INVESTMENT_AMOUNT}")
print(f"Weight Acquired   : {grams} g")
print("----------------------------------")
print(f"Monthly Low Rate  : ₹{month_low}")
print(f"Monthly High Rate : ₹{month_high}")
print(f"Best Possible Gms : {best_grams} g")
print("----------------------------------")

if rate == month_low:
    print("✅ Today's rate is the MONTHLY LOW")
else:
    difference = rate - month_low
    print(f"₹{difference} above monthly low")

print("EMAIL FUNCTION STARTING")

send_email(
    f"GRT Gold Tracker - {today}",
    email_body
)