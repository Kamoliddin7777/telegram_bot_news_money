# Telegram Bot

This is a **Telegram bot** built with Python using **pyTelegramBotAPI**.  
It provides various interactive features, including daily facts, weather information, news, event categories, and currency exchange rates.  
The bot is modular and easy to extend.

---

## 🛠 Features

- **Event Categories**: Browse different events and categories.  
- **Daily Fact**: Get a random fact every day.  
- **Weather Info**: Check current weather for a specified city.  
- **News**: Get the latest news with additional functionalities.  
- **Currency Exchange Rates**: Check current currency rates.  
- **Interactive Buttons**: Navigate bot functions easily using inline buttons.

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `base_curse.py` | Base functionality for handling bot commands. |
| `buttons.py` | Defines all inline buttons and keyboard layouts. |
| `config.py` | Bot configuration, API tokens, and settings. |
| `event_categories.py` | Logic for event categories. |
| `events.py` | Handles events and related functionalities. |
| `main.py` | Main entry point of the bot. Initializes and runs the bot. |
| `news.py` | Fetches news and additional functionalities. |
| `requirements.txt` | Python dependencies required to run the bot. |
| `weather_info.py` | Fetches weather data for given cities. |

---

## ⚡ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/Kamoliddin7777/your-repo-name.git
cd your-repo-name
Create a virtual environment:

bash

python -m venv venv
Activate the virtual environment:

Windows:

bash

venv\Scripts\activate
Linux / MacOS:

bash

source venv/bin/activate
Install dependencies:

bash

pip install -r requirements.txt
Set up your Telegram Bot Token in config.py
(Get your own key from @BotFather to activate the bot)

🚀 Running the Bot
bash

python main.py
The bot will now be live and responsive in Telegram.
