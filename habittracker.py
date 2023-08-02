import datetime
import json
import os

from habit import Habit


class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)
        self.save_to_file('habit_data.json')  # Save the updated list of habits to the file

    def delete_habit(self, habit_name):
        self.habits = [habit for habit in self.habits if habit.name != habit_name]
        self.save_to_file('habit_data.json')  # Save the updated list of habits to the file

    def get_all_habits(self):
        self.load_from_file('habit_data.json')  # Load habits from the file before returning them
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_streak(self):
        return max(habit.streak() for habit in self.habits)

    def get_longest_streak_for_habit(self, habit_name):
        habit = next((habit for habit in self.habits if habit.name == habit_name), None)
        if habit:
            return habit.streak()
        return 0




    def save_to_file(self, file_path):
        with open(file_path, 'w') as f:
            data = [{"name": habit.name, "description": habit.description, "periodicity": habit.periodicity,
                     "created_date": habit.created_date.strftime('%Y-%m-%d'),
                     "completions": [c.strftime('%Y-%m-%d %H:%M:%S') for c in habit.completions]} for habit in
                    self.habits]
            json.dump(data, f, indent=2)

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.habits = []
                for entry in data:
                    habit = Habit(entry["name"], entry["description"], entry["periodicity"])
                    habit.created_date = datetime.datetime.strptime(entry["created_date"], '%Y-%m-%d').date()
                    habit.completions = [datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S') for c in
                                         entry["completions"]]
                    # Check if the last completion is for today, if not, reset completions to break the streak
                    today = datetime.date.today()
                    if habit.completions and habit.completions[-1].date() < today:
                        habit.completions = []
                    self.habits.append(habit)

            if not self.habits:  # Check if the list is empty
                # Add predefined habits to the tracker only when the list is empty
                for habit_data in predefined_habits_data:
                    habit = Habit(habit_data["name"], habit_data["description"], habit_data["periodicity"])
                    habit.created_date = datetime.datetime.strptime(habit_data["created_date"], '%Y-%m-%d').date()
                    habit.completions = [datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S') for c in
                                         habit_data["completions"]]
                    self.habits.append(habit)

                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            data = json.load(f)



# Predefined habits and their example tracking data
predefined_habits_data = [
    {
        "name": "Drink Water",
        "description": "Drink 8 glasses of water daily.",
        "periodicity": "daily",
        "created_date": "2023-07-02",
        "completions": []
    },
    {
        "name": "Exercise",
        "description": "Exercise for 30 minutes daily.",
        "periodicity": "daily",
        "created_date": "2023-07-02",
        "completions": []
    },
    {
        "name": "Reading",
        "description": "Read for 1 hour daily.",
        "periodicity": "daily",
        "created_date": "2023-07-02",
        "completions": []
    },
    {
        "name": "Learn a new Language",
        "description": "Spend 2 hours weekly on learning a new language",
        "periodicity": "weekly",
        "created_date": "2023-07-02",
        "completions": []
    },
    {
        "name": "Gratitude Journaling",
        "description": "Write in your gratitude journal for 15 minutes daily.",
        "periodicity": "daily",
        "created_date": "2023-07-02",
        "completions": []
    }
]
def view_predefined_habit_data():
    print("\nPredefined Habit Data:")
    for habit_data in predefined_habits_data:
        print(f"Name: {habit_data['name']}")
        print(f"Description: {habit_data['description']}")
        print(f"Periodicity: {habit_data['periodicity']}")
        print(f"Created Date: {habit_data['created_date']}")
        print(f"Completions: {habit_data['completions']}")
        print("------------------------------")

