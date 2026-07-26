# 🧴 Skincare Expiry Notifier - Setup Guide

A free automated system to remind your girlfriend about expiring skincare products via email.

## Features
✅ **Free** - Uses free Google Sheets + GitHub Actions  
✅ **Flexible** - Custom reminder times for each product (1d, 1h, 30m, 1w, etc.)  
✅ **Automatic** - Runs daily without manual intervention  
✅ **Email Reminders** - Sends beautiful HTML emails  

---

## Step 1: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet
2. Rename it to something like "Skincare Tracker"
3. Set up columns with these exact headers in row 1:
   - A: `Product Name`
   - B: `Expiry Date`
   - C: `Reminder Time`
   - D: `Category`
   - E: `Notes`

### Example Data:
```
Product Name          | Expiry Date | Reminder Time | Category      | Notes
Moisturizer Deluxe    | 2026-12-15  | 1d            | Moisturizer   | Daily use
Vitamin C Serum       | 2026-09-20  | 3d            | Serum         | Morning routine
Face Cleanser         | 2027-03-10  | 1w            | Cleanser      | 
```

**Reminder Time Format:**
- `1m` = 1 minute before expiry
- `1h` = 1 hour before expiry
- `1d` = 1 day before expiry
- `1w` = 1 week before expiry
- `30m` = 30 minutes before expiry
- `2d` = 2 days before expiry

4. Copy the Sheet ID from the URL (it's the long string between `/d/` and `/edit`)
   - Example: `https://docs.google.com/spreadsheets/d/**1A2B3C4D5E6F**`
   - Your ID: `1A2B3C4D5E6F`

---

## Step 2: Set Up Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or use existing one)
   - Click "Select a Project" → "New Project"
   - Name it "Skincare Notifier"
3. Enable Google Sheets API:
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create Service Account:
   - Go to "Credentials" on the left
   - Click "Create Credentials" → "Service Account"
   - Name: `skincare-notifier`
   - Skip optional steps, click "Create and Continue"
5. Create a Key:
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Select "JSON"
   - A JSON file will download - **save this somewhere safe**
6. Share your Google Sheet with the service account email:
   - Open the JSON file and copy the `client_email` value
   - Go back to your Google Sheet
   - Click "Share" (top right)
   - Paste the service account email
   - Give it "Editor" access
   - Click "Share"

---

## Step 3: Set Up Gmail for Sending Emails

1. Your girlfriend needs a Gmail account (or you can use yours)
2. Enable 2-Factor Authentication:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Find "2-Step Verification" and enable it
3. Create an App Password:
   - After enabling 2FA, go back to Security settings
   - Find "App passwords" (appears after 2FA is enabled)
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password - **copy this**

---

## Step 4: Fork & Set Up GitHub Repository

1. Go to [this repository](https://github.com/bryanimon/skincare-notifier) (you'll need to create it)
   - Or manually create files as shown below

2. Create a new GitHub repository named `skincare-notifier`

3. Create these files in your repo:

**File 1: `.github/workflows/notifier.yml`**
```yaml
name: Skincare Notifier

on:
  schedule:
    - cron: '0 9 * * *'  # Runs daily at 9 AM UTC (adjust to your timezone)
  workflow_dispatch:  # Allow manual trigger

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
      
      - name: Run Notifier
        env:
          GOOGLE_SHEET_ID: ${{ secrets.GOOGLE_SHEET_ID }}
          GOOGLE_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_SERVICE_ACCOUNT_JSON }}
          RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
          SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
          SENDER_PASSWORD: ${{ secrets.SENDER_PASSWORD }}
        run: python skincare_notifier.py
```

**File 2: `skincare_notifier.py`**
- Copy the content from the script provided

4. Add Secrets to GitHub:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret" and add these:

| Secret Name | Value |
|------------|-------|
| `GOOGLE_SHEET_ID` | The Sheet ID you copied earlier |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | The entire JSON content from Step 2 (as a string) |
| `RECIPIENT_EMAIL` | Your girlfriend's email address |
| `SENDER_EMAIL` | Gmail address for sending emails |
| `SENDER_PASSWORD` | The 16-character App Password from Step 3 |

**Important:** When adding `GOOGLE_SERVICE_ACCOUNT_JSON`, copy the entire JSON content as one line (or just paste it all).

---

## Step 5: Test It Out

1. In your GitHub repository, go to "Actions"
2. Click on "Skincare Notifier"
3. Click "Run workflow" → "Run workflow"
4. Wait a few seconds and check if:
   - The workflow runs (you'll see a ✅ or ❌)
   - Your girlfriend receives a test email

---

## Adjusting the Schedule

Edit the cron time in `.github/workflows/notifier.yml`:

```yaml
cron: '0 9 * * *'  # Runs at 9 AM UTC
```

**Timezone Conversions:**
- `0 9 * * *` = 9 AM UTC
- `0 1 * * *` = 1 AM UTC (8 AM Manila time)
- `0 5 * * *` = 5 AM UTC (1 PM Manila time)

[Cron Time Converter](https://crontab.guru/)

---

## Troubleshooting

**Email not sending?**
- Check Gmail app password is correct
- Make sure 2FA is enabled
- Check GitHub Actions logs for errors

**No products showing up?**
- Check column headers match exactly (capitals matter)
- Make sure service account email has access to the sheet
- Check date format: `YYYY-MM-DD` or `MM/DD/YYYY`

**Script errors?**
- Check GitHub Actions logs
- Make sure all secrets are set correctly
- Test the date parsing with your date format

---

## That's it! 🎉

Your girlfriend can now:
1. Add products to the Google Sheet
2. Set custom reminder times
3. Receive automatic email reminders

No more expired skincare products! 💅✨
