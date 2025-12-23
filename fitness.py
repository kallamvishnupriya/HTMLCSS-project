import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from datetime import datetime
import json

# ------------------- OOP CLASSES ------------------- #
class Activity:
    def __init__(self, date, steps, calories, workout):
        self.date = date
        self.steps = steps
        self.calories = calories
        self.workout = workout

    def to_dict(self):
        return {
            "date": self.date,
            "steps": self.steps,
            "calories": self.calories,
            "workout": self.workout
        }

class User:
    def __init__(self, name):
        self.name = name
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)
        self.save_data()

    def load_data(self):
        try:
            with open(f"{self.name}_data.json", "r") as f:
                data = json.load(f)
                for item in data:
                    self.activities.append(Activity(**item))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(f"{self.name}_data.json", "w") as f:
            json.dump([a.to_dict() for a in self.activities], f, indent=4)

    def get_weekly_data(self):
        return self.activities[-7:]

    def get_monthly_data(self):
        return self.activities[-30:]

# ------------------- MODERN UI APP ------------------- #
class FitnessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fitness Tracker App")
        self.root.geometry("550x600")
        self.root.configure(bg="#f0f4f7")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=8)
        style.configure("TLabel", font=("Arial", 12), background="#f0f4f7")
        style.configure("TEntry", padding=5)

        self.card_bg = "#ffffff"
        self.card_border = "#d4d4d4"

        self.user = User("default_user")
        self.user.load_data()

        self.build_ui()
        self.root.mainloop()

    # Create card container
    def create_card(self, parent):
        frame = tk.Frame(parent, bg=self.card_bg, highlightbackground=self.card_border,
                         highlightthickness=1, bd=0)
        frame.pack(pady=10, padx=20, fill="x")
        return frame

    # UI ELEMENTS
    def build_ui(self):
        header = tk.Label(self.root, text="🏋️ Fitness Tracking App", font=("Arial", 20, "bold"), bg="#f0f4f7")
        header.pack(pady=15)

        form_card = self.create_card(self.root)

        ttk.Label(form_card, text="Steps:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.steps_entry = ttk.Entry(form_card, width=25)
        self.steps_entry.grid(row=0, column=1, pady=8)

        ttk.Label(form_card, text="Calories:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.calories_entry = ttk.Entry(form_card, width=25)
        self.calories_entry.grid(row=1, column=1, pady=8)

        ttk.Label(form_card, text="Workout Type:").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.workout_entry = ttk.Entry(form_card, width=25)
        self.workout_entry.grid(row=2, column=1, pady=8)

        ttk.Button(self.root, text="➕ Add Activity", command=self.add_activity).pack(pady=10)

        graph_card = self.create_card(self.root)
        ttk.Button(graph_card, text="📊 Weekly Stats", command=self.show_weekly_graph).pack(pady=5, fill="x")
        ttk.Button(graph_card, text="📈 Monthly Stats", command=self.show_monthly_graph).pack(pady=5, fill="x")

        ttk.Button(self.root, text="📜 View All Activities", command=self.show_all_activities).pack(pady=10)

    # Add activity
    def add_activity(self):
        try:
            steps = int(self.steps_entry.get())
            calories = int(self.calories_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Steps and calories must be numbers!")
            return

        workout = self.workout_entry.get()
        date = datetime.now().strftime("%Y-%m-%d")

        activity = Activity(date, steps, calories, workout)
        self.user.add_activity(activity)

        messagebox.showinfo("Success", "Activity added successfully!")
        self.steps_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.workout_entry.delete(0, tk.END)

    # Show weekly graph
    def show_weekly_graph(self):
        data = self.user.get_weekly_data()
        if not data:
            messagebox.showerror("Error", "No data to show!")
            return

        dates = [a.date for a in data]
        steps = [a.steps for a in data]
        calories = [a.calories for a in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, steps, marker='o', label='Steps')
        plt.plot(dates, calories, marker='o', label='Calories')
        plt.xticks(rotation=45)
        plt.title("Weekly Fitness Stats")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Show monthly graph
    def show_monthly_graph(self):
        data = self.user.get_monthly_data()
        if not data:
            messagebox.showerror("Error", "No data to show!")
            return

        dates = [a.date for a in data]
        steps = [a.steps for a in data]
        calories = [a.calories for a in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, steps, marker='o', label='Steps')
        plt.plot(dates, calories, marker='o', label='Calories')
        plt.xticks(rotation=45)
        plt.title("Monthly Fitness Stats")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Show all activities
    def show_all_activities(self):
        activity_window = tk.Toplevel(self.root)
        activity_window.title("All Activities")
        activity_window.geometry("400x450")
        activity_window.configure(bg="#f0f4f7")

        text_box = tk.Text(activity_window, wrap="word", font=("Arial", 12))
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        for a in self.user.activities:
            text_box.insert(tk.END, f"📅 Date: {a.date}\n🚶 Steps: {a.steps}\n🔥 Calories: {a.calories}\n🏋️ Workout: {a.workout}\n---------------------------\n")

# Run the app
if __name__ == "__main__":
    FitnessApp()
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fitness Tracker App")
        self.root.geometry("450x500")

        self.user = User("default_user")
        self.user.load_data()

        self.build_ui()
        self.root.mainloop()

    # UI ELEMENTS
    def build_ui(self):
        tk.Label(self.root, text="Fitness Tracking App", font=("Arial", 18, "bold")).pack(pady=10)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Steps
        tk.Label(form_frame, text="Steps:").grid(row=0, column=0, sticky="w")
        self.steps_entry = tk.Entry(form_frame)
        self.steps_entry.grid(row=0, column=1)

        # Calories
        tk.Label(form_frame, text="Calories:").grid(row=1, column=0, sticky="w")
        self.calories_entry = tk.Entry(form_frame)
        self.calories_entry.grid(row=1, column=1)

        # Workout
        tk.Label(form_frame, text="Workout (name):").grid(row=2, column=0, sticky="w")
        self.workout_entry = tk.Entry(form_frame)
        self.workout_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add Activity", command=self.add_activity, width=20).pack(pady=10)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        tk.Button(self.root, text="Show Weekly Stats", command=self.show_weekly_graph, width=25).pack(pady=5)
        tk.Button(self.root, text="Show Monthly Stats", command=self.show_monthly_graph, width=25).pack(pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        tk.Button(self.root, text="Show All Activities", command=self.show_all_activities, width=25).pack(pady=5)

    # Add activity
    def add_activity(self):
        try:
            steps = int(self.steps_entry.get())
            calories = int(self.calories_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Steps and calories must be numbers!")
            return

        workout = self.workout_entry.get()
        date = datetime.now().strftime("%Y-%m-%d")

        activity = Activity(date, steps, calories, workout)
        self.user.add_activity(activity)

        messagebox.showinfo("Success", "Activity added successfully!")
        self.steps_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.workout_entry.delete(0, tk.END)

    # Show weekly graph
    def show_weekly_graph(self):
        data = self.user.get_weekly_data()
        if not data:
            messagebox.showerror("Error", "No data to show!")
            return

        dates = [a.date for a in data]
        steps = [a.steps for a in data]
        calories = [a.calories for a in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, steps, marker='o', label='Steps')
        plt.plot(dates, calories, marker='o', label='Calories')
        plt.xticks(rotation=45)
        plt.title("Weekly Fitness Stats")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Show monthly graph
    def show_monthly_graph(self):
        data = self.user.get_monthly_data()
        if not data:
            messagebox.showerror("Error", "No data to show!")
            return

        dates = [a.date for a in data]
        steps = [a.steps for a in data]
        calories = [a.calories for a in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, steps, marker='o', label='Steps')
        plt.plot(dates, calories, marker='o', label='Calories')
        plt.xticks(rotation=45)
        plt.title("Monthly Fitness Stats")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Show all activities
    def show_all_activities(self):
        activity_window = tk.Toplevel(self.root)
        activity_window.title("All Activities")
        activity_window.geometry("400x400")

        text_box = tk.Text(activity_window, wrap="word")
        text_box.pack(fill="both", expand=True)

        for a in self.user.activities:
            text_box.insert(tk.END, f"Date: {a.date}\nSteps: {a.steps}\nCalories: {a.calories}\nWorkout: {a.workout}\n-------------------\n")

# Run the app
if __name__ == "__main__":
    FitnessApp()
