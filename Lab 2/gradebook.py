"""
GradeBook Analyzer
Author: Anant Kumar
Date: 10 Nov 2025
Title: Analysing and Reporting Student Grades
"""

import csv
import statistics

# ---------------------------
# Task 1: Project Setup & Menu
# ---------------------------

def display_menu():
    print("\n========== GradeBook Analyzer ==========")
    print("1. Enter student data manually")
    print("2. Load student data from CSV file")
    print("3. Exit")
    print("========================================")

# ---------------------------
# Task 2: Data Entry or CSV Import
# ---------------------------

def get_manual_data():
    marks = {}
    n = int(input("Enter number of students: "))
    for i in range(n):
        name = input(f"Enter name of student {i+1}: ")
        score = float(input(f"Enter marks for {name}: "))
        marks[name] = score
    return marks

def get_csv_data():
    marks = {}
    filename = input("Enter CSV filename (with .csv): ")
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                if len(row) >= 2:
                    name, score = row[0], float(row[1])
                    marks[name] = score
        print(f"Loaded data from {filename}")
    except FileNotFoundError:
        print("File not found. Try again.")
    return marks

# ---------------------------
# Task 3: Statistical Functions
# ---------------------------

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    return max(marks_dict.items(), key=lambda x: x[1])

def find_min_score(marks_dict):
    return min(marks_dict.items(), key=lambda x: x[1])

# ---------------------------
# Task 4: Grade Assignment
# ---------------------------

def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        grades[name] = grade
    return grades

def grade_distribution(grades_dict):
    distribution = {'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
    for grade in grades_dict.values():
        distribution[grade] += 1
    return distribution

# ---------------------------
# Task 5: Pass/Fail Filter
# ---------------------------

def pass_fail_lists(marks_dict):
    passed = [name for name, score in marks_dict.items() if score >= 40]
    failed = [name for name, score in marks_dict.items() if score < 40]
    return passed, failed

# ---------------------------
# Task 6: Results Table & Loop
# ---------------------------

def display_results(marks_dict, grades_dict):
    print("\nName\t\tMarks\tGrade")
    print("---------------------------------")
    for name, score in marks_dict.items():
        print(f"{name:<15}{score:<10}{grades_dict[name]}")
    print("---------------------------------")

def export_to_csv(marks_dict, grades_dict):
    choice = input("Do you want to export results to CSV? (y/n): ").lower()
    if choice == 'y':
        with open("final_gradebook.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Marks", "Grade"])
            for name, marks in marks_dict.items():
                writer.writerow([name, marks, grades_dict[name]])
        print("Results saved as final_gradebook.csv")

# ---------------------------
# Main CLI Loop
# ---------------------------

def main():
    print("Welcome to the GradeBook Analyzer!")
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            marks = get_manual_data()
        elif choice == '2':
            marks = get_csv_data()
        elif choice == '3':
            print("Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
            continue

        if marks:
            avg = calculate_average(marks)
            med = calculate_median(marks)
            max_score = find_max_score(marks)
            min_score = find_min_score(marks)

            print("\n=== Statistical Summary ===")
            print(f"Average Marks: {avg:.2f}")
            print(f"Median Marks: {med:.2f}")
            print(f"Highest Score: {max_score[0]} ({max_score[1]})")
            print(f"Lowest Score: {min_score[0]} ({min_score[1]})")

            grades = assign_grades(marks)
            dist = grade_distribution(grades)

            print("\n=== Grade Distribution ===")
            for grade, count in dist.items():
                print(f"{grade}: {count}")

            passed, failed = pass_fail_lists(marks)
            print("\n=== Pass/Fail Summary ===")
            print(f"Passed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
            print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")

            display_results(marks, grades)
            export_to_csv(marks, grades)

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
