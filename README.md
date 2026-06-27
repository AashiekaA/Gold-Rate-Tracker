## 🔗 Gold-Rate-Tracker

## Automated Python-based gold rate monitoring system that tracks daily 22K gold prices, calculates investment weight acquisition, updates Google Sheets, and sends email notifications with trend analysis.

## 🔗 Overview

This project demonstrates an end-to-end automation workflow using Python, GitHub Actions, Google Sheets, and email notifications to monitor daily 22K gold rates from GRT Jewellers.

The application extracts the latest 22K gold rate, calculates the gold weight acquired for a predefined investment amount, stores historical records in Google Sheets, analyzes day-over-day price movements, calculates monthly high and low rates directly from historical data, and automatically sends email notifications with daily investment insights.

The entire workflow is cloud-hosted and executes automatically through GitHub Actions without requiring manual intervention. The project was enhanced to perform day-over-day price comparison using historical Google Sheets data, providing additional trend visibility for investment tracking.

---

## 🔗 Objectives

- Track daily 22K gold rates automatically
- Calculate gold weight acquired for a fixed investment amount
- Maintain historical gold rate records
- Monitor monthly high and low prices
- Track day-over-day rate changes
- Automate reporting through Google Sheets and email notifications

---

## 🔗 Key Metrics

- Daily 22K Gold Rate
- Investment Amount
- Weight Acquired (grams)
- Monthly Low Rate
- Monthly High Rate
- Best Possible Grams
- Day-over-Day Price Difference

---

## 🔗 Project Workflow

1. Fetches the latest 22K gold rate from the GRT Jewellers website
2. Extracts the current gold rate using Python and Regular Expressions
3. Calculates the gold weight acquired for the configured investment amount
4. Updates Google Sheets with the latest daily record
5. Retrieves historical data from Google Sheets
6. Calculates day-over-day price differences
7. Performs monthly low/high analysis using Google Sheets history
8. Sends an automated email summary
9. Runs automatically every day using GitHub Actions

---

## 🔗 Screenshots

### Google Sheets Output
*(Add screenshot here)*

### Email Notification
*(Add screenshot here)*

### GitHub Actions Workflow
![GitHub Actions Workflow](images/github-actions.png)

---

## 🔗 Features

- Automated daily tracking of GRT 22K gold rates
- Calculates gold weight acquired for a fixed investment amount
- Uses Google Sheets as the single source of truth for historical data
- Sends automated email notifications
- Tracks day-over-day price movement
- Identifies monthly low and monthly high rates
- Calculates best possible grams based on monthly low
- Fully automated using GitHub Actions

---

## 🔗 Architecture

GRT Jewellers Website
          │
          ▼
Python Web Scraper
          │
          ▼
Google Sheets (Historical Data)
          │
    ┌─────┴─────┐
    ▼           ▼
Yesterday    Monthly Analysis
Difference   (Low / High)
    │           │
    └─────┬─────┘
          ▼
Email Notification
          │
          ▼
GitHub Actions (Daily Automation)

---

## 🔗 Tools Used

- Python
- Pandas
- Requests
- Regular Expressions (re)
- Google Sheets API (gspread)
- Gmail SMTP
- GitHub Actions
- JSON Configuration
---

## 🔗 Configuration

The application is configured through:

- `config.json` for investment amount, scheme name, and notification emails
- GitHub Secrets for secure email authentication
- Google Service Account credentials for Google Sheets integration

This design allows configuration changes without modifying the source code.

## 🔗 Data Sources

- GRT Jewellers Website
- Google Sheets

---

## 🔗 Key Insights

- Tracks daily fluctuations in 22K gold prices
- Identifies monthly low-rate opportunities for investment decisions
- Calculates gold weight acquired for a fixed investment amount
- Monitors day-over-day price movements and trends
- Provides cloud-based automated monitoring through GitHub Actions
- Eliminates manual tracking and data entry

---

## 🔗 How to Use

1. Clone the repository
2. Configure Google Sheets credentials
3. Add GitHub Secrets for email and Google authentication
4. Update the investment amount in `config.json`
5. Run `main.py` locally or trigger the GitHub Actions workflow
6. Review daily updates in Google Sheets and automated email notifications
