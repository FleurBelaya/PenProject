from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
import sqlite3
from kivy.app import App


class MainScreen(Screen):
    goal_done = BooleanProperty(False)

    def toggle_goal(self):
        self.goal_done = not self.goal_done
        goal_btn = self.ids.goal_button
        if self.goal_done:
            goal_btn.text = "Цель выполнена"
            goal_btn.background_color = (1, 0.6, 0.8, 1)
            self.add_points(50)
        else:
            goal_btn.text = "Цель не выполнена"
            goal_btn.background_color = (1, 1, 1, 1)

    def add_points(self, points):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if user_id:
            conn = sqlite3.connect('articles.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, user_id))
            conn.commit()
            conn.close()
            try:
                profile = self.manager.get_screen('profile')
                if hasattr(profile, 'load_user_data'):
                    profile.load_user_data()
            except Exception:
                pass

    def go_to_profile(self):
        self.manager.current = 'profile'

