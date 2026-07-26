#!/usr/bin/env python3
"""
Skincare Product Expiry Notifier
Sends email reminders for expiring skincare products based on custom reminder times
"""
 
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
 
# Configuration
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Set this in GitHub Actions secrets
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")  # Set this in GitHub Actions secrets
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Your girlfriend's email
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # Gmail address for sending
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Gmail app password
 
def parse_reminder_date(reminder_str):
    """
    Parse reminder date string (e.g., '2026-12-15')
    Returns None if parsing fails
    """
    return parse_date(reminder_str)
 
def get_sheet_data():
    """Read data from Google Sheet"""
    try:
        # Authenticate with service account
        creds = Credentials.from_service_account_info(
            eval(SERVICE_ACCOUNT_JSON),
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
 
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
 
        # Read all data from the sheet
        result = sheet.values().get(spreadsheetId=SHEET_ID, range='Sheet1!A:G').execute()
        values = result.get('values', [])
 
        return values
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return None
 
def parse_date(date_str):
    """Parse date string in multiple formats"""
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%d-%m-%Y', '%m-%d-%Y']
 
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
 
    return None
 
def send_email_batch(products_list):
    """Send a single email with all reminders in a table"""
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"⏰ Skincare Reminders: {len(products_list)} product(s) need attention!"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
 
        # Build table rows
        table_rows = ""
        for product in products_list:
            table_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
              <td style="padding: 12px; border-right: 1px solid #ddd;">{product['name']}</td>
              <td style="padding: 12px; border-right: 1px solid #ddd;">{product['category']}</td>
              <td style="padding: 12px; border-right: 1px solid #ddd;">{product['expiry_date']}</td>
              <td style="padding: 12px; color: #e91e63; font-weight: bold;">{product['days_until']} days</td>
            </tr>
            """
 
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #e91e63;">🧴 Skincare Product Expiration Reminders</h2>
 
            <p>You have <strong>{len(products_list)} product(s)</strong> to check:</p>
 
            <table style="width: 100%; border-collapse: collapse; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
              <thead>
                <tr style="background-color: #e91e63; color: white;">
                  <th style="padding: 12px; text-align: left; border-right: 1px solid #ddd;">Product Name</th>
                  <th style="padding: 12px; text-align: left; border-right: 1px solid #ddd;">Category</th>
                  <th style="padding: 12px; text-align: left; border-right: 1px solid #ddd;">Expiry Date</th>
                  <th style="padding: 12px; text-align: left;">Days Until Expiry</th>
                </tr>
              </thead>
              <tbody>
                {table_rows}
              </tbody>
            </table>
 
            <p style="margin-top: 20px; padding: 15px; background-color: #fff3e0; border-left: 4px solid #ff9800; border-radius: 4px;">
              ⏰ <strong>Don't forget to use these products before they expire!</strong>
            </p>
 
            <p style="color: #999; font-size: 12px; margin-top: 20px;">
              This is an automated reminder from your Skincare Notifier.
            </p>
          </body>
        </html>
        """
 
        msg.attach(MIMEText(html_body, 'html'))
 
        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
 
        print(f"✅ Email sent with {len(products_list)} product(s)")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
 
def check_and_notify():
    """Main function to check expiry dates and send notifications"""
    print("🔍 Checking skincare products...")
 
    # Get sheet data
    values = get_sheet_data()
    if not values or len(values) < 2:
        print("❌ No data found in sheet or sheet is empty")
        return
 
    # Parse header
    headers = values[0]
    print(f"Headers: {headers}")
 
    # Find column indices
    try:
        product_idx = headers.index('Product Name')
        expiry_idx = headers.index('Expiry Date')
        reminder_idx = headers.index('Reminder Date')
        category_idx = headers.index('Category') if 'Category' in headers else None
    except ValueError as e:
        print(f"❌ Missing required column: {e}")
        return
 
    now = datetime.now()
    products_to_notify = []
 
    # Check each product and collect those that need reminders today
    for row in values[1:]:
        if len(row) <= max(product_idx, expiry_idx, reminder_idx):
            continue
 
        product_name = row[product_idx].strip()
        expiry_date_str = row[expiry_idx].strip()
        reminder_date_str = row[reminder_idx].strip() if reminder_idx < len(row) else None
        category = row[category_idx].strip() if category_idx and category_idx < len(row) else ""
 
        # Skip if product name is empty
        if not product_name or product_name.lower() == 'product name':
            continue
 
        # Parse expiry date
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            print(f"⚠️  Could not parse expiry date for {product_name}: {expiry_date_str}")
            continue
 
        # Parse reminder date
        reminder_date = parse_reminder_date(reminder_date_str)
        if not reminder_date:
            print(f"⚠️  Could not parse reminder date for {product_name}: {reminder_date_str}")
            continue
 
        days_until_expiry = (expiry_date - now).days
 
        # Check if today is the reminder date or past it
        if now.date() >= reminder_date.date():
            products_to_notify.append({
                'name': product_name,
                'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                'days_until': days_until_expiry,
                'category': category
            })
 
    # Only send emails if there are products to notify about
    if products_to_notify:
        print(f"📧 Found {len(products_to_notify)} product(s) to notify about:")
        for product in products_to_notify:
            print(f"   - {product['name']} (expires {product['expiry_date']})")
 
        # Send a single email with all products in a table
        if send_email_batch(products_to_notify):
            print(f"\n✅ Notifier completed. Email sent with {len(products_to_notify)} reminder(s).")
        else:
            print(f"\n❌ Notifier completed with errors.")
    else:
        print(f"✅ Notifier completed. No reminders for today - no emails sent.")
 
if __name__ == "__main__":
    if not all([SHEET_ID, SERVICE_ACCOUNT_JSON, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD]):
        print("❌ Missing required environment variables!")
        print("Required: GOOGLE_SHEET_ID, GOOGLE_SERVICE_ACCOUNT_JSON, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD")
        exit(1)
 
    check_and_notify()
