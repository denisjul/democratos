import datetime
from haystack import indexes
from CreateYourLaws.models import LawArticle, Explaination, Proposition
from CreateYourLaws.models import Posopinion, Negopinion, Question, CYL_user


class LawIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField((document=True, use_template=True))
    text_law = indexes.TextField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return LawArticle

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.order_by('approval_factor')
