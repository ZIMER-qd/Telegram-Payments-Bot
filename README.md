# Telegram-Payment-Bot with FastAPI
### Description:
- This is a test bot that has paid features, subscription functionality,  
  and the ability to purchase a link to a private channel.
### Functions:
- /primelink - Test paid feature;
- /game - Test paid feature;
- /secretphoto - Test paid feature;
- /sub_mode - A feature that is available by subscription.;
- /profile - User profile;
### Requirements:
- Python 3.11+
- aiogram
- SQLAlchemy
- pydantic-settings
- pydantic
- fastapi
- uvicorn
- httpx
- asyncpg
- alembic
### Installation:
#### 1. Clone the repository:  
git clone https://github.com/ZIMER-qd/Telegram-Payments-Bot.git  
cd Telegram-Payments-Bot  
#### 2. Create a virtual environment and activate it:  
python -m venv .venv  
source .venv/bin/activate - Linux / Mac  
.venv\Scripts\activate - Windows  
#### 3. Install dependencies:  
pip install -r requirements.txt  
#### 4. Configure the .env file with the bot token:  
BOT_TOKEN=token  
PROVIDER_TOKEN=provider_token (You can find it in BotFather in the Payments section after connecting a payment provider.)  
POSTGRE_PASS=password (Your password for working with PostgreSQL, before running the program, you need to create a database, this can be done through pgAdmin)  
#### 5. Run the bot:  
python run.py