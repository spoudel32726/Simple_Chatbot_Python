```markdown
# Terminal Chat Bot

A simple terminal chat client powered by Django and ChatterBot.

## Overview
This project features a Django management command for a chatbot, trained on the English corpus and stored in SQLite.

## Requirements
- Python 3.8+
- Git

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/spoudel32726/Simple_Chatbot_Python.git
   cd terminal_chat
   ```
2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the bot:
   ```
   python manage.py chat
   ```
   - First run trains the bot (a few minutes).
   - Type "quit" to exit.

## Usage
- Enter messages after the "user:" prompt.
- Example:
  ```
  user: Good morning! How are you?
  bot: I am doing well, thank you!
  user: quit
  bot: Goodbye!
  ```

## Files
- `requirements.txt`: Project dependencies.
- `terminal_chat/`: Django project folder.
- `chatbot/`: Bot application.

## Notes
- Ignore the `NotOpenSSLWarning`; it doesn’t affect functionality.
- Retrain with `python manage.py chat --retrain` if needed.


```
