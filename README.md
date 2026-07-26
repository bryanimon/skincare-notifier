# 🧴 Skincare Expiry Notifier

An automated system that sends email reminders when your skincare products are about to expire.

## ✨ Features

- ✅ **Free** - Uses Google Sheets + GitHub Actions
- ✅ **Simple Setup** - 5 steps to get started
- ✅ **Smart Reminders** - Set custom reminder dates for each product
- ✅ **Single Email** - All reminders in one beautiful table (no spam!)
- ✅ **Automatic** - Runs daily without manual intervention
- ✅ **No Code Needed** - Just add products to Google Sheet

## 📧 How Emails Work

### When Multiple Products Need Reminders:

**You get ONE email with a clean table:**

```
Subject: ⏰ Skincare Reminders: 3 product(s) need attention!

You have 3 product(s) to check:

┌─────────────────┬──────────────┬─────────────┬──────────────┐
│ Product Name    │ Category     │ Expiry Date │ Days Left    │
├─────────────────┼──────────────┼─────────────┼──────────────┤
│ Moisturizer     │ Moisturizer  │ 2026-12-15  │ 1 day        │
│ Vitamin C Serum │ Serum        │ 2026-09-20  │ 3 days       │
│ Face Cleanser   │ Cleanser     │ 2027-03-10  │ 10 days      │
└─────────────────┴──────────────┴─────────────┴──────────────┘
```

### When No Products Need Reminders:

**No email sent** - Completely silent, no spam! ✅

The script logs "No reminders for today - no emails sent."

---

## 🔧 How It Works

1. **You Add Products** to Google Sheet with:
   - Product Name
   - Expiry Date (YYYY-MM-DD)
   - Reminder Date (when to be reminded)
   - Category
   - Notes

2. **GitHub Actions Runs Daily** at your set time

3. **Script Checks** if today matches any reminder date

4. **If Matches:**
   - Collects all products to remind about
   - Creates ONE email with table format
   - Sends email to girlfriend

5. **If No Matches:**
   - No email sent (saves inbox clutter!)

---

## 📋 Google Sheet Setup

| Column | Example | Format |
|--------|---------|--------|
| Product Name | Moisturizer | Text |
| Expiry Date | 2026-12-15 | YYYY-MM-DD |
| Reminder Date | 2026-12-14 | YYYY-MM-DD |
| Category | Moisturizer | Text |
| Notes | Daily use | Text |

**Reminder Date Calculation:**
- Product expires: 2026-12-15
- Want reminder 1 day before? Set to: 2026-12-14
- Want reminder 3 days before? Set to: 2026-12-12
- Want reminder 1 week before? Set to: 2026-12-08

---

## 🚀 Quick Start

1. Create Google Sheet with headers
2. Enable Google Sheets API in Cloud Console
3. Create Service Account and download JSON
4. Enable 2FA on Gmail + create app password
5. Create GitHub repo and add files
6. Add 5 secrets to GitHub
7. Test by running workflow manually

**Full Setup Guides:**
- `THOROUGH_SETUP.md` - Ultra detailed (every click explained)
- `QUICK_START.md` - Quick reference
- `SETUP_GUIDE.md` - Standard walkthrough
- `STEP_BY_STEP.md` - Detailed steps

---

## 📁 Files Included

- `skincare_notifier.py` - Main automation script
- `notifier-workflow.yml` - GitHub Actions workflow
- Setup guides and documentation

---

## 🔒 Security

- All secrets encrypted in GitHub
- Service account only reads Google Sheet (can't modify)
- App password only sends emails (can't access other services)
- No passwords in code or logs

---

## 🛠 Troubleshooting

**No email received?**
- Check Actions logs for errors
- Verify all 5 secrets are added
- Make sure sheet is shared with service account

**Workflow shows red X?**
- Check GitHub Actions logs
- Common issues: wrong secrets, API not enabled, sheet not shared

**Getting too many emails?**
- Adjust Reminder Date column to space them out
- Script only sends when reminder date matches

---

## 💡 Tips

- **Test with today's date:** Set Reminder Date to today to test immediately
- **No products today?** No email will be sent (smart!)
- **Change time:** Edit cron in `.github/workflows/notifier.yml`
- **Add products:** Just add rows to Google Sheet, no code changes needed

---

🎉 **Enjoy expired-product-free skincare!**
