### Telegram Weather Bot
Telegram bot providing the currency excahge of BYN to USD and EUR and the current wrather forecust for the provided city.

## How to run the service (in Powershell) ?
- Execeute the command `Set-ExecutionPolicy RemoteSigned -Scope Process`
- Activat Python environemnt `.\env\Scripts\activate`
- Set environment variable `$env:FLASK_APP='app.py'`
- Set environment variable for Telegram Bot token `$env:TELERAM_BOT_TOKEN='(PLEASE_INSERT_YOUR_TOKEN)'`
- Set environment variable for Python Bot token `$env:TELERAM_BOT_TOKEN='(PLEASE_INSERT_YOUR_TOKEN)'` 
- Execute the command `flask run`