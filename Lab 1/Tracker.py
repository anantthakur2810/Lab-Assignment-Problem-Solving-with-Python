# Project Title: Daily Calorie Tracker CLI #
# Author: Anant Kumar #
# Date: 10th November 2025 #


import datetime

#Task 1: Introduction#
print("="*60)
print(" Welcome to the Daily Calorie Tracker CLI ")
print("="*60)
print("This tool helps you log your meals and track total calorie intake.")
print("You can compare it against your daily limit and even save a report.")

#Task 2: Data Collection#
meals = []
calories = []

num_meals = int(input("How many meals did you have today? "))

for i in range(num_meals):
    meal_name = input(f"\nEnter name of meal {i+1}: ")
    calorie_value = float(input(f"Enter calories for {meal_name}: "))
    meals.append(meal_name)
    calories.append(calorie_value)

#Task 3: Calorie Calculations#
total_calories = sum(calories)
average_calories = total_calories / len(calories)

daily_limit = float(input("\nEnter your daily calorie limit: "))

#Task 4: Warning System#
if total_calories > daily_limit:
    status_message = " You have exceeded your daily calorie limit! "
else:
    status_message = " Great! You are within your daily calorie limit. "

#Task 5: Formatted Output#
print(" Daily Summary ")
print(f"{'Meal Name':<20}{'Calories'}")
print("-" * 35)

for meal, cal in zip(meals, calories):
    print(f"{meal:<20}{cal}")

print("-" * 35)
print(f"{'Total:':<20}{total_calories}")
print(f"{'Average:':<20}{average_calories:.2f}")
print("-" * 35)
print(status_message)

#Task 6 (Bonus): Save to File# 
save = input("Would you like to save this report? (yes/no): ").strip().lower()

if save == "yes":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"calorie_log_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(" DAILY CALORIE TRACKER REPORT ")
        f.write(f"Date & Time: {datetime.datetime.now()}\n\n")
        f.write(f"{'Meal Name':<20}{'Calories'}\n")
        f.write("-" * 35 + "\n")
        for meal, cal in zip(meals, calories):
            f.write(f"{meal:<20}{cal}\n")
        f.write("-" * 35 + "\n")
        f.write(f"{'Total:':<20}{total_calories}\n")
        f.write(f"{'Average:':<20}{average_calories:.2f}\n")
        f.write("-" * 35 + "\n")
        f.write(f"Status: {status_message}\n")


    print(f"\n💾 Report saved successfully as '{filename}'!\n")
else:
    print("\nReport not saved. Thank you for using the tracker! 😊")

#End of Program#
