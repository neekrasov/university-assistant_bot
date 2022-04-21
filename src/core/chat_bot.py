import abc

import aiohttp
import requests
from deeppavlov import train_model
from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector

from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill
from nltk.corpus import stopwords
import nltk
from deeppavlov.core.common.file import read_json

from .configs.settings import PERCENTAGE_CONFIDENCE_FOR_ANSWER

from loguru import logger

question_url = "question/"
HOST = 'db_api'

nltk.download('stopwords')

def create_url(url: str, any_id=None):
    if any_id is None:
        any_id = list()
    return f'http://{HOST}:8001/{url.format(*any_id)}'


def simple_post_request(url: str, any_id: list = None, data: dict = None) -> dict():
    if any_id is None:
        any_id = list()
    if data is None:
        data = dict()

    return requests.post(url=create_url(url=url, any_id=any_id), json=data).json()


def save_question(question):
    logger.debug({'question': question})
    return simple_post_request(url=question_url,
                               data={'question': question})


class Bot(abc.ABC):

    @abc.abstractmethod
    def ask(self, question: str) -> str:
        pass


class CastomHighestConfidenceSelector(HighestConfidenceSelector):

    def __call__(self, utterances: list, batch_history: list, *responses: list) -> tuple:
        responses, confidences = zip(*[zip(*r) for r in responses])
        indexes = [c.index(max(c)) for c in zip(*confidences)]
        if confidences[indexes[0]][0] <= PERCENTAGE_CONFIDENCE_FOR_ANSWER:
            logger.debug(utterances[0])
            logger.debug(save_question(utterances[0]))
        result = [responses[i] for i, *responses in zip(indexes, *responses)]
        logger.debug(result[0])
        return result[0], confidences[indexes[0]]


class ChatBot(Bot):
    def __init__(
            self, config_path: str = "core/configs/faq/tfidf_logreg_autofaq.json",
            data_path: str = None,
            save_load_path: str = "core/model",
            train: bool = False
    ):

        model_config = read_json(config_path)
        logger.debug(train)
        if data_path:
            model_config["dataset_reader"]["data_path"] = data_path
            model_config["dataset_reader"]["data_url"] = None
        if train:
            stop_words = stopwords.words('russian')
            stop_words.extend(
                ['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на'])
            model_config["chainer"]["pipe"][4]["warm_start"] = True
            model_config["chainer"]["pipe"][0]["stopwords"] = stop_words
            train_model(model_config)

        faq = SimilarityMatchingSkill(data_path=None,
                                      x_col_name='Question',
                                      y_col_name='Answer',
                                      save_load_path=save_load_path,
                                      config_type='tfidf_logreg_autofaq',
                                      edit_dict={},
                                      train=False)

        hello = PatternMatchingSkill(responses=['Привет', 'Приветствую'],
                                     patterns=['Привет', 'Здравствуйте'])
        bye = PatternMatchingSkill(responses=['Пока', 'Всего доброго'],
                                   patterns=['Пока', 'До свидания'])
        # fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'],
        #                                 default_confidence=0.8)
        fallback = PatternMatchingSkill(responses=["/"],
                                        default_confidence=PERCENTAGE_CONFIDENCE_FOR_ANSWER)

        self._dialog = []
        self._agent = DefaultAgent([hello, bye, faq, fallback],
                                   skills_processor=CastomHighestConfidenceSelector())

    def ask(self, question: str):
        answers, confidence = self._agent([question], [0])
        answer = answers.capitalize()
        self._dialog.append((question, answer))
        return answer

    def get_dialog(self) -> list:
        return self._dialog
