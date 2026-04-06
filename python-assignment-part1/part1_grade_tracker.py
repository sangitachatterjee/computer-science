# Task 1 — Data Parsing & Profile Cleaning (5 marks)
print("Task 1 — Data Parsing & Profile Cleaning (5 marks)")
raw_students = [
    {"name": "  ayesha SHARMA  ", "roll": "101", "marks_str": "88, 72, 95, 60, 78"},
    {"name": "ROHIT verma",       "roll": "102", "marks_str": "55, 68, 49, 72, 61"},
    {"name": "  Priya Nair  ",    "roll": "103", "marks_str": "91, 85, 88, 94, 79"},
    {"name": "karan MEHTA",       "roll": "104", "marks_str": "40, 55, 38, 62, 50"},
    {"name": " Sneha pillai ",    "roll": "105", "marks_str": "75, 80, 70, 68, 85"},
]

cleaned_students = []

for raw in raw_students:
    name = raw["name"].strip().title()
    roll = int(raw["roll"])
    marks = [int(m) for m in raw["marks_str"].split(", ")]
    cleaned_students.append({"name": name, "roll": roll, "marks": marks})

for student in cleaned_students:
    words = student["name"].split()
    valid = all(word.isalpha() for word in words)
    print("Valid name" if valid else "Invalid name")
    print(f"""================================
Student : {student["name"]}
Roll No : {student["roll"]}
Marks   : {student["marks"]}
================================""")

roll_103 = next(s for s in cleaned_students if s["roll"] == 103)
n = roll_103["name"]
print(n.upper())
print(n.lower())

# Task 2 — Marks Analysis Using Loops & Conditionals (8 marks)

print("\n\nTask 2 — Marks Analysis Using Loops & Conditionals (8 marks)")
student_name = "Ayesha Sharma"
subjects     = ["Math", "Physics", "CS", "English", "Chemistry"]
marks        = [88, 72, 95, 60, 78]


def grade_label(score):
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    return "F"


print(f"\n{student_name} — subject marks and grades")
for subject, mark in zip(subjects, marks):
    print(f"  {subject}: {mark} — {grade_label(mark)}")

total_marks = sum(marks)
average_marks = round(total_marks / len(marks), 2)
highest = max(zip(subjects, marks), key=lambda pair: pair[1])
lowest = min(zip(subjects, marks), key=lambda pair: pair[1])

print(f"\nTotal marks: {total_marks}")
print(f"Average marks: {average_marks}")
print(f"Highest scoring subject: {highest[0]} ({highest[1]})")
print(f"Lowest scoring subject: {lowest[0]} ({lowest[1]})")

all_subjects = list(subjects)
all_marks = list(marks)
new_subject_count = 0

print("\n--- Add more subjects (type 'done' as subject name to finish) ---")
while True:
    name_in = input("Subject name: ").strip()
    if name_in.lower() == "done":
        break

    marks_in = input("Marks (0-100): ").strip()
    try:
        m = int(marks_in)
    except ValueError:
        print("Warning: marks must be a whole number between 0 and 100. Entry skipped.")
        continue

    if m < 0 or m > 100:
        print("Warning: marks must be between 0 and 100. Entry skipped.")
        continue

    all_subjects.append(name_in)
    all_marks.append(m)
    new_subject_count += 1

updated_average = round(sum(all_marks) / len(all_marks), 2)
print(f"\nNew subjects added: {new_subject_count}")
print(f"Updated average (all subjects): {updated_average}")

# Task 3 — Class Performance Summary (7 marks)
print("\n\nTask 3 — Class Performance Summary (7 marks)")

class_data = [(s["name"], s["marks"]) for s in cleaned_students]

NAME_COL = 18
report_rows = []

print(f"{'Name':<{NAME_COL}}| Average | Status")
print("-" * 40)

for name, scores in class_data:
    average = round(sum(scores) / len(scores), 2)
    status = "Pass" if average >= 60 else "Fail"
    report_rows.append((name, average, status))
    print(f"{name:<{NAME_COL}}|  {average:>5.2f}  | {status}")

pass_count = sum(1 for _, _, s in report_rows if s == "Pass")
fail_count = sum(1 for _, _, s in report_rows if s == "Fail")
topper_name, topper_avg, _ = max(report_rows, key=lambda row: row[1])
class_average = round(sum(r[1] for r in report_rows) / len(report_rows), 2)

print()
print(f"Number of students who passed: {pass_count}")
print(f"Number of students who failed: {fail_count}")
print(f"Class topper: {topper_name} ({topper_avg:.2f})")
print(f"Class average: {class_average:.2f}")

# Task 4 — String Manipulation Utility (5 marks)
print("\n\nTask 4 — String Manipulation Utility (5 marks)")

essay = "  python is a versatile language. it supports object oriented, functional, and procedural programming. python is widely used in data science and machine learning.  "

# Step 1 — strip; all later steps use this string
clean_essay = essay.strip()
print("\nStep 1 — Stripped essay (clean_essay):")
print(clean_essay)

print("\nStep 2 — Title Case:")
print(clean_essay.title())

print("\nStep 3 — Count of 'python' (case-insensitive):")
print(clean_essay.count("python"))

print("\nStep 4 — Replace 'python' with 'Python 🐍':")
print(clean_essay.replace("python", "Python 🐍"))

sentences = clean_essay.split(". ")
print("\nStep 5 — Sentences (split on '. '):")
print(sentences)

print("\nStep 6 — Numbered sentences:")
for i, sentence in enumerate(sentences, start=1):
    line = sentence if sentence.endswith(".") else sentence + "."
    print(f"{i}. {line}")
