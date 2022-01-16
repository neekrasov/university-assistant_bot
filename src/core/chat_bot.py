import abc
from deeppavlov import train_model
from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector

from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill
from nltk.corpus import stopwords
from deeppavlov.core.common.file import read_json


class Bot(abc.ABC):

    @abc.abstractmethod
    def ask(self, question: str) -> str:
        pass


class FallbackMessage:
    def __init__(self, threshold: float, message="Пожалуйста, перефразируйте вопрос."):
        if threshold > 1.0:
            threshold = 1
        if threshold < 0.0:
            threshold = 0
        self.threshold = threshold
        self.message = message


class ChatBot(Bot):
    def __init__(
            self, config_path: str = "src/core/configs/faq/tfidf_logreg_autofaq.json",
            data_path: str = None,
            save_load_path: str = "src/core/model",
            train: bool = False
    ):
        stop_words = stopwords.words('russian')
        stop_words.extend(
            ['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])

        model_config = read_json(config_path)
        if data_path:
            model_config["dataset_reader"]["data_path"] = data_path
            model_config["dataset_reader"]["data_url"] = None
        if train:
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
        fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'],
                                        default_confidence=0.3)

        self._dialog = []
        self._agent = DefaultAgent([hello, bye, faq, fallback],
                                   skills_selector=HighestConfidenceSelector())

    def ask(self, question: str):
        answers = self._agent([question], [0])
        self._dialog.append((question, answers[0]))
        return answers

    def get_dialog(self) -> list:
        return self._dialog
