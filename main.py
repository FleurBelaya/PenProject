from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.main_screen import MainScreen
from screens.profile_screen import ProfileScreen
from screens.challenges_screen import ChallengesScreen
from screens.exercises_screen import ExercisesScreen
from screens.articles_screen import ArticlesScreen


class PenApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(ChallengesScreen(name="challenges"))
        sm.add_widget(ExercisesScreen(name="exercises"))
        sm.add_widget(ArticlesScreen(name="articles"))
        return sm


if __name__ == "__main__":
    PenApp().run()
