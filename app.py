>>> from flask import Flask, render_template, request, redirect, url_for
... import pandas as pd
... import random
... import string
... from openpyxl import load_workbook
... import os
... 
... app = Flask(__name__)
... 
... EXCEL_FILE = "seva_data.xlsx"
... 
... # Utility: Generate referral code
... def generate_referral():
...     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
... 
... # Utility: Save booking to Excel
... def save_to_excel(data):
...     if not os.path.exists(EXCEL_FILE):
...         df = pd.DataFrame(columns=["BookingID","Name","Phone","Email","Address","SevaName","Date","Amount","ReferralCode","PaymentStatus"])
...         df.to_excel(EXCEL_FILE, index=False)
... 
...     df = pd.read_excel(EXCEL_FILE)
...     booking_id = len(df) + 1
...     data["BookingID"] = booking_id
...     df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
...     df.to_excel(EXCEL_FILE, index=False)
... 
... @app.route('/')
... def index():
...     return render_template("index.html")
... 
... @app.route('/book', methods=['GET','POST'])
... def book():
...     if request.method == 'POST':
...         name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        seva = request.form['seva']
        date = request.form['date']
        amount = request.form['amount']
        
        referral = generate_referral()

        save_to_excel({
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Address": address,
            "SevaName": seva,
            "Date": date,
            "Amount": amount,
            "ReferralCode": referral,
            "PaymentStatus": "Pending"
        })

        return redirect(url_for('success'))

    return render_template("booking.html")

@app.route('/success')
def success():
    return "✅ Booking Saved Successfully! You will receive an OTP for next time."

if __name__ == "__main__":
