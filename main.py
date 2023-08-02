import datetime
import json
import os
import random

from habit import Habit
from habittracker import HabitTracker, predefined_habits_data
from habittracker import view_predefined_habit_data

def generate_random_completions():
    start_date = datetime.datetime(2023, 7, 2)
    for habit_data in predefined_habits_data:
        current_date = start_date
        for _ in range(28):
            if habit_data["periodicity"] == "weekly" and current_date.weekday() == 6:
                habit_data["completions"].append(current_date.strftime('%Y-%m-%d %H:%M:%S'))
            elif habit_data["periodicity"] == "daily":
                if random.random() < 0.7:
                    habit_data["completions"].append(current_date.strftime('%Y-%m-%d %H:%M:%S'))
            current_date += datetime.timedelta(days=1)

def main():
    tracker = HabitTracker()

    # Load habits from the file
    tracker.load_from_file('habit_data.json')

    # Generate random completions for predefined habits
    generate_random_completions()


    while True:
        print("\nHabit Tracker Menu:")
        print("1. Add Habit")
        print("2. Delete Habit")
        print("3. Complete Habit Task")
        print("4. View All Habits")
        print("5. View Habits by Periodicity")
        print("6. View Longest Streak")
        print("7. View Longest Streak for a Habit")
        print("8. Save to File")
        print("9. View Sample Data")
        print("10. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            name = input("Enter habit name: ")
            description = input("Enter habit description: ")
            periodicity = input("Enter habit periodicity (daily/weekly): ").lower()
            habit = Habit(name, description, periodicity)
            tracker.add_habit(habit)
            print(f"{name} habit added and saved to the file.")

        elif choice == '2':
            name = input("Enter habit name to delete: ")
            tracker.delete_habit(name)
            print(f"{name} habit deleted.")

        elif choice == '3':
            name = input("Enter habit name to complete the task: ")
            habit = next((habit for habit in tracker.habits if habit.name == name), None)
            if habit:
                if habit.complete_task():
                    print(f"Task for {name} habit completed.")
                else:
                    print(f"You have already completed the task for {datetime.date.today()}.")
            else:
                print(f"{name} habit not found.")

        elif choice == '4':
            print("All Habits:")
            habits = tracker.get_all_habits()  # Load habits from the file
            for habit in habits:
                print(habit)

        elif choice == '5':
            periodicity = input("Enter periodicity (daily/weekly): ").lower()
            habits = tracker.get_habits_by_periodicity(periodicity)
            print(f"Habits with {periodicity} periodicity:")
            for habit in habits:
                print(habit)

        elif choice == '6':
            longest_streak = tracker.get_longest_streak()
            print(f"Longest streak: {longest_streak} days")

        elif choice == '7':
            name = input("Enter habit name: ")
            longest_streak = tracker.get_longest_streak_for_habit(name)
            print(f"Longest streak for {name}: {longest_streak} days")

        elif choice == '8':
            tracker.save_to_file('habit_data.json')
            print("Data saved to file.")

        elif choice == '9':
            view_predefined_habit_data()

        elif choice == '10':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
