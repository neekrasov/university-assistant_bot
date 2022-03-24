import abc
from deeppavlov import train_model
from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector

from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill
from nltk.corpus import stopwords
from deeppavlov.core.common.file import read_json

from .configs.settings import PERCENTAGE_CONFIDENCE_FOR_ANSWER


class Bot(abc.ABC):

    @abc.abstractmethod
    def ask(self, question: str) -> str:
        pass


class CastomHighestConfidenceSelector(HighestConfidenceSelector):

    def __call__(self, utterances: list, batch_history: list, *responses: list) -> tuple:
        responses, confidences = zip(*[zip(*r) for r in responses])
        indexes = [c.index(max(c)) for c in zip(*confidences)]
        if confidences[indexes[0]][0] <= PERCENTAGE_CONFIDENCE_FOR_ANSWER:
            with open('questions.txt', 'a') as f:
                f.write(utterances[0] + '\n')
        result = [responses[i] for i, *responses in zip(indexes, *responses)]
        return result[0], confidences[indexes[0]]


class ChatBot(Bot):
    def __init__(
            self, config_path: str = "core/configs/faq/tfidf_logreg_autofaq.json",
            data_path: str = None,
            save_load_path: str = "core/model",
            train: bool = False
    ):

        model_config = read_json(config_path)
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
        fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'],
                                        default_confidence=PERCENTAGE_CONFIDENCE_FOR_ANSWER)

        self._dialog = []
        self._agent = DefaultAgent([hello, bye, faq, fallback],
                                   skills_processor=CastomHighestConfidenceSelector())

    def ask(self, question: str):
        answers, confidence = self._agent([question], [0])
        answers = answers.capitalize()
        self._dialog.append((question, answers))
        return answers, confidence

    def get_dialog(self) -> list:
        return self._dialog
