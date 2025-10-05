from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3
import random


class ExercisesScreen(Screen):
    def on_exercise_selected(self, exercise_type):
        self.current_exercise_type = exercise_type
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()

        if exercise_type == 'three_in_row':
            cursor.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 3')
            words = [row[0] for row in cursor.fetchall()]
            prompt = ' '.join(words)
        elif exercise_type == 'poetic_trace':
            cursor.execute('SELECT line FROM poems ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            prompt = row[0] if row else ''
        elif exercise_type == 'why':
            cursor.execute('SELECT question FROM questions ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            prompt = row[0] if row else ''
        else:
            prompt = ''

        conn.close()
        self.ids.exercise_prompt.text = f"{prompt}\nПридумайте сюжет:"
        self.ids.exercise_input.text = ''

    def on_exercise_submitted(self):
        app = App.get_running_app()
        main_screen = self.manager.get_screen('main')
        main_screen.add_points(10)
        if hasattr(self, 'current_exercise_type'):
            self.on_exercise_selected(self.current_exercise_type)
