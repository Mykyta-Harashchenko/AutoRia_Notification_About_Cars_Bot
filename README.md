# AutoRia Telegram Bot

Overview
This is a Telegram bot built using Aiogram that monitors car auctions on AutoRia and notifies users about new listings, price changes, and removed listings.

Features
- Start the bot and receive a welcome message.
- Set up reminders for specific AutoRia auctions.
- Scrape AutoRia for car listings and track them.
- Notify users of new cars added to the auction.
- Notify users of price changes for tracked cars.
- Notify users when a tracked car has been removed from the auction.
- Store sent car notifications to prevent duplicate alerts.

Installation

Prerequisites
- Python 3.8+
- A Telegram bot token (obtained from BotFather)
- AutoRia parser script (`parsers.py`)
- Required dependencies in `requirements.txt`

Setup
1. Clone the repository:
   git clone https://github.com/your-repo/auto-ria-bot.git
   cd auto-ria-bot

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
   pip install -r requirements.txt

4. Create a `.env` file and add your Telegram bot token:
   BOT_TOKEN=your_telegram_bot_token

5. Run the bot:
   python bot.py

Usage
1. Start the bot by sending `/start`.
2. Use the "Поставити нагадування" button to set an auction reminder.
3. Send the AutoRia auction link to track a car.
4. The bot will notify you about any updates, including:
   - New listings
   - Price changes
   - Removed cars

Configuration
- The bot checks for updates every 15 minutes (`CHECK_INTERVAL = 900` seconds).
- Sent cars are stored in `sent_cars.json`.
- Logging is enabled to track errors and updates.

Dependencies
- `aiogram`
- `asyncio`
- `python-dotenv`
- `logging`
- `json`

License
This project is licensed under the MIT License.

Author
Your Name - Harashchenko Mykyta

