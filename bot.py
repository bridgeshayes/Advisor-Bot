import os
from discord import Client
from discord import Intents as DiscordIntents
from dotenv import load_dotenv
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.classifiers.bow import BagOfWords
from train import load_classifier
from modules.contexts.context import Context
from modules.states.conversation.initiation import Initiation
import modules.states.conversation.course as course
import modules.states.conversation.directory as directory


class Bot(Client):

    def __init__(self, debug=False, classifier: IntentClassifier = BagOfWords("advisor")):
        discord_intents = DiscordIntents.default()
        discord_intents.message_content = True
        super().__init__(intents=discord_intents)
        self.debug: bool = debug
        self.context = Context("Default", classifier)
        self.context.state = Initiation("Initiation", self.context)
        self.classifier = classifier

    async def on_ready(self):
        for guild in self.guilds:
            print("Users:")
            for m in guild.members:
                print("{}".format(m.display_name))

    async def on_message(self, message):
        if message.author == self.user:
            return

        next_state = self.context.parse_response(message.content)
        await message.channel.send(self.context.message)
        self.context.state = next_state
        if isinstance(next_state, course.DisplayCourse) or isinstance(next_state, directory.DisplayDirectory):
            await message.channel.send(next_state.message)

    def get_response(self, sentence: str) -> tuple[str, str]:
        return self.classifier.get_response(sentence, debug=False)


if __name__ == "__main__":
    if load_dotenv():
        TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        CLASSIFICATION_MODEL = os.getenv('CLASSIFICATION_MODEL')

        # This function comes from the training file; it works the same for classifying
        classifier = load_classifier(CLASSIFICATION_MODEL=CLASSIFICATION_MODEL, channel_name="advisor")

        client = Bot(classifier=classifier)
        client.run(TOKEN)

