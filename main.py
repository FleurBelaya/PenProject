from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import sqlite3
from screens.main_screen import MainScreen
from screens.profile_screen import ProfileScreen
from screens.challenges_screen import ChallengesScreen
from screens.exercises_screen import ExercisesScreen
from screens.articles_screen import ArticlesScreen
from screens.article_from_screen import ArticleFormScreen
from screens.article_detail_screen import ArticleDetailScreen
from screens.shop_screen import ShopScreen
from screens.auth_screen import AuthScreen
from screens.profile_view_screen import ProfileViewScreen


class PenApp(App):
    current_user_id = None

    def build(self):
        return


if __name__ == '__main__':
    PenApp().run()





