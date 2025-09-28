from django.core.management.base import BaseCommand
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.conf import settings
import os

class Command(BaseCommand):
    """
    A Django management command to run a terminal-based chat client with a ChatterBot instance.
    On first run, it trains the bot using the English corpus. Subsequent runs use the persisted SQLite database.
    Usage: python manage.py chat
    Type 'quit' to exit the conversation.
    """
    help = 'Run the terminal chat bot'

    def add_arguments(self, parser):
        # Optional argument to force retraining (for debugging)
        parser.add_argument('--retrain', action='store_true', help='Force retrain the bot with corpus data')

    def handle(self, *args, **options):
        # Define the bot name and storage path (uses Django's BASE_DIR for portability)
        bot_name = 'TerminalBot'
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')  # ChatterBot defaults to this for Django projects

        # Check if the database exists; if not, or if --retrain, train the bot
        if options['retrain'] or not os.path.exists(db_path):
            self.stdout.write(self.style.SUCCESS('Training the bot with English corpus... This may take a few minutes.'))
            bot = ChatBot(
                bot_name,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=f'sqlite:///{db_path}',
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
                    'chatterbot.logic.MathematicalEvaluation',  # Optional: Handles math queries
                ],
                preprocessors=[
                    'chatterbot.preprocessors.clean_whitespace',
                ]
            )
            trainer = ChatterBotCorpusTrainer(bot)
            trainer.train('chatterbot.corpus.english')  # Train on English conversations
            self.stdout.write(self.style.SUCCESS('Training complete!'))
        else:
            # Load the existing bot
            bot = ChatBot(
                bot_name,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=f'sqlite:///{db_path}',
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
                    'chatterbot.logic.MathematicalEvaluation',
                ],
                preprocessors=[
                    'chatterbot.preprocessors.clean_whitespace',
                ]
            )
            self.stdout.write(self.style.SUCCESS('Bot loaded from database.'))

        # Start the interactive chat loop
        self.stdout.write(self.style.WARNING('Chat started! Type your message (or "quit" to exit).'))
        while True:
            try:
                user_input = input("user: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.stdout.write(self.style.SUCCESS('Goodbye!'))
                    break

                if not user_input:
                    continue  # Skip empty inputs

                # Get bot response
                response = bot.get_response(user_input)
                print(f"bot: {response}")
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\nChat interrupted. Goodbye!'))
                break
            except Exception as e:
                self.stderr.write(f"Error: {e}")