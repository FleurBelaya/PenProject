from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class ArticleDetailScreen(Screen):
    article_text = StringProperty('')

    def set_article_text(self, text):
        self.article_text = text
