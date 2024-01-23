import random

names = [
    "Bibek","Shah","Shankhar","Alice", "Bob", "Charlie", "David", "Emily", "Frank", "Grace", "Henry", "Isabella", "Jack",  # Add more names as needed
]
courses = ["Data Science", "DEVOPS", "Web Development", "Machine Learning", "AI","Data Analyst","Technician"]
grades = ["S","A", "B", "C", "D", "F"]

statements = [
    f"""cursor.execute('''Insert Into STUDENT values('{random.choice(names)}', '{random.choice(courses)}', '{random.choice(grades)}', {random.randint(50, 100)})''')"""
    for _ in range(500)
]

print(*statements, sep="\n")  # Print each statement on a separate line
