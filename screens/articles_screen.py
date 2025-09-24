from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import sqlite3

class ArticlesScreen(Screen):

    def on_enter(self):
        self.load_articles()

    def load_articles(self):
        container = self.ids.articles_container
        container.clear_widgets()

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM articles')
        articles = cursor.fetchall()
        conn.close()

        for article_id, title in articles:
            btn = Button(text=title, size_hint_y=None, height=40)
            btn.bind(on_press=lambda btn, id=article_id: self.open_article(id))
            container.add_widget(btn)

    def open_article(self, article_id):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM articles WHERE id=?', (article_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            content = result[0]
            article_detail_screen = self.manager.get_screen('article_detail')
            article_detail_screen.set_article_text(content)
            self.manager.current = 'article_detail'

