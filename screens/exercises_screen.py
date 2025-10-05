from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3

class ExercisesScreen(Screen):
    def on_pre_enter(self):
        self.apply_color_upgrade()

    def apply_color_upgrade(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_upgrades (
                user_id INTEGER NOT NULL,
                upgrade_id INTEGER NOT NULL,
                PRIMARY KEY(user_id, upgrade_id)
            )
        ''')
        cursor.execute('SELECT upgrade_id FROM user_upgrades WHERE user_id = ?', (user_id,))
        upgrades = {row[0] for row in cursor.fetchall()}
        conn.close()
        if 5 in upgrades:
            for bid in ['three_btn', 'poetic_btn', 'why_btn']:
                if bid in self.ids:
                    self.ids[bid].background_color = (0.9, 0.9, 0.4, 1)
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
