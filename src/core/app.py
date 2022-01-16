from .chat_bot import ChatBot
from .configs.settings import dataset_data_path

ai_assistant = ChatBot(
    data_path=dataset_data_path,
    # train=True
)