from .chat_bot import ChatBot
from .configs.settings import dataset_data_path

bot = ChatBot(
    data_path=dataset_data_path,
    # train=True
)