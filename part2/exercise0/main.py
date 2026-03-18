import random
import time
import os
from multiprocessing import Process, Queue
from queue import Empty

class Student:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.examiner = None
        self.t_start = None
        self.t_end = None
    def __repr__(self):
        return self.name

class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.current_student = None
        self.total_students = 0
        self.failed = 0
        self.work_time = 0.0
        self.is_on_lunch = False
        self.lunch_taken = False
        self.lunch_end_time = None
        self.exam_end_time = None
        self.pending_passed = None
    def __repr__(self):
        return self.name

class Question:
    def __init__(self, text):
        self.text = text
        self.success_count = 0
    def __repr__(self):
        return self.text

# *********GOLDEN RATION part of choice question
def golden(n):
    rem = 1.0
    phi = 1.618
    numb = []
    temp = 0

    for i in range(n - 1):
        temp = rem / phi
        rem = rem - temp
        numb.append(temp)
         # print('i= ',i,'temp= ',temp,'numb= ',numb,)
    numb.append(rem)
    return numb
# print(golden_probs(3))

# ********GET RANDOM INDEX
def rand_choice(numb):
    temp = 0
    r = random.random()
    # print('r= ',r)
    for i in range(len(numb)):
        temp = temp + numb[i]
        if r <= temp:
            return i
    return len(numb) - 1

# *****GET WORD FROM WITH RANDOM GOLDEN RATION
def student_word_choice(student, question):
    words = question.text.split()
    n = len(words)
    probs = golden(n)
    idx = rand_choice(probs)

    if student.gender == "М":
        return words[idx]
    else:
        return words[n - 1 - idx]

# *******CHOISE EXAMINER WORDS
def examiner_correct_words(question):
    words = question.text.split()
    correct = set()
    w = random.choice(words)
    correct.add(w)
    while len(correct) < len(words):
        r = random.random()
        if r < 1/3:
            remaining = [word for word in words if word not in correct]
            w = random.choice(remaining)
            correct.add(w)
        else:
            break
    return correct        

# *******CHECK OF TRUE 1 ANSWER FROM STUDENT 
def check_question(student, question):
    is_correct = False
    student_word = student_word_choice(student, question)
    correct_set = examiner_correct_words(question)
    if student_word in correct_set:
        is_correct = True
    return is_correct, student_word, correct_set   

# *******EXAM OF STUDENT WITH 3 QUESTION
def exam_three_questions(student, questions):
    correct_count = 0
    wrong_count = 0
    successful_questions = []

    selected_questions = random.sample(questions, 3)

    for question in selected_questions:
        is_correct, student_word, correct_set = check_question(student, question)

        if is_correct:
            correct_count += 1
            successful_questions.append(question.text)
        else:
            wrong_count += 1
    # ******mood of examiner 
    # [0,0 ; 0,125)-bad
    # [0,125 ; 0,375)-good
    # [0,375 ; 1.0)-neutral
    mood_value = random.random()

    if mood_value < 1 / 8:
        passed = False
    elif mood_value < 3 / 8:
        passed = True
    else:
        passed = correct_count > wrong_count
    
    selected_question_texts = [question.text for question in selected_questions]

    return correct_count, wrong_count, passed, selected_question_texts, successful_questions

# *********TIME OF EXAM
def exam_time(examiner):
    name_length = len(examiner.name)
    return random.uniform(name_length - 1, name_length + 1)     

# ********PRINTABLE FUNCTION DURING EXAM 
def print_students_table(students):
    print("Во время работы")
    sorted_students = sorted(
        students,
        key=lambda s: 0 if s.status == "Очередь" else 1 if s.status == "Сдал" else 2
    )
    print("+------------+----------+")
    print("| Студент    |  Статус  |")
    print("+------------+----------+")
    for student in sorted_students:
        print(f"| {student.name:<10} | {student.status:<8} |")
    print("+------------+----------+")

def print_examiners_table(examiners):
    print("+-------------+-----------------+-----------------+---------+--------------+")
    print("| Экзаменатор | Текущий студент | Всего студентов | Завалил | Время работы |")
    print("+-------------+-----------------+-----------------+---------+--------------+")
    for examiner in examiners:
        if examiner.is_on_lunch:
            current = "-"
        else:    
            current = examiner.current_student if examiner.current_student is not None else "-"
        print(
            f"| {examiner.name:<11} "
            f"| {current:<15} "
            f"| {examiner.total_students:<15} "
            f"| {examiner.failed:^7} "
            f"| {examiner.work_time:^12.2f} |"
        )
    print("+-------------+-----------------+-----------------+---------+--------------+")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# *********FINAL PRINTABLE FUNCTION 
def print_final_students_table(students):
    print("После работы")
    sorted_students = sorted(
        students,
        key=lambda s: (0 if s.status == "Сдал" else 1)
    )
    print("+------------+----------+")
    print("| Студент    |  Статус  |")
    print("+------------+----------+")
    for student in sorted_students:
        print(f"| {student.name:<10} | {student.status:^8} |")
    print("+------------+----------+")

def print_final_examiners_table(examiners):
    print("+-------------+-----------------+---------+--------------+")
    print("| Экзаменатор | Всего студентов | Завалил | Время работы |")
    print("+-------------+-----------------+---------+--------------+")
    for examiner in examiners:
        print(
            f"| {examiner.name:<11} "
            f"| {examiner.total_students:^15} "
            f"| {examiner.failed:^7} "
            f"| {examiner.work_time:^12.2f} |"
        )
    print("+-------------+-----------------+---------+--------------+")

# **********THE BEST STATISTICS
def get_best_students(students):
    passed_students = [
        s for s in students
        if s.status == "Сдал" and s.t_start is not None and s.t_end is not None
    ]

    if not passed_students:
        return []

    best_time = min(s.t_end - s.t_start for s in passed_students)    
    return [
        s.name
        for s in passed_students
        if (s.t_end - s.t_start) == best_time
    ]

def get_best_examiners(examiners):
    active_examiners = [e for e in examiners if e.total_students > 0]

    if not active_examiners:
        return []

    best_ratio = min(e.failed / e.total_students for e in active_examiners)    
    return [
        e.name
        for e in active_examiners
        if (e.failed / e.total_students) == best_ratio
    ]

def get_expelled_students(students):
    failed_students = [
        s for s in students
        if s.status == "Провалил" and s.t_start is not None and s.t_end is not None
    ]

    if not failed_students:
        return []

    min_duration = min(s.t_end - s.t_start for s in failed_students)
    return [
        s.name
        for s in failed_students
        if (s.t_end - s.t_start) == min_duration
    ]

def get_best_questions(questions):
    if not questions:
        return []

    best_count = max(q.success_count for q in questions)
    return [q.text for q in questions if q.success_count == best_count]

def get_exam_result(students):
    if not students:
        return "экзамен не удался"

    passed_count = sum(1 for s in students if s.status == "Сдал")
    ratio = passed_count / len(students)
    return "экзамен удался" if ratio > 0.85 else "экзамен не удался"

def examiner_worker(examiner_name, examiner_gender, student_queue, result_queue, event_queue, questions, t0):
    total_students = 0
    failed = 0
    work_time = 0.0
    lunch_taken = False

    examiner = Examiner(examiner_name, examiner_gender)

    while True:
        try:
            student_data = student_queue.get_nowait()
        except Empty:
            break

        student = Student(student_data["name"], student_data["gender"])

        student_start = time.time() - t0

        event_queue.put({
            "type": "exam_started",
            "examiner_name": examiner_name,
            "student_name": student.name,
            "t_start": student_start
        })

        duration = exam_time(examiner)

        correct_count, wrong_count, passed, selected_questions, successful_questions = exam_three_questions(student, questions)

        time.sleep(duration)

        student_end = time.time() - t0

        event_queue.put({
            "type": "exam_finished",
            "examiner_name": examiner_name,
            "student_name": student.name,
            "status": "Сдал" if passed else "Провалил",
            "t_end": student_end,
            "duration": student_end - student_start
        })

        total_students += 1
        work_time += student_end - student_start

        if not passed:
            failed += 1

        result_queue.put({
            "type": "student_result",
            "student_name": student.name,
            "status": "Сдал" if passed else "Провалил",
            "examiner_name": examiner_name,
            "t_start": student_start,
            "t_end": student_end,
            "successful_questions": successful_questions,
            "selected_questions": selected_questions,
            "correct_count": correct_count,
            "wrong_count": wrong_count
        })

        # Обед только после завершения текущего студента
        now = time.time() - t0
        if now >= 30 and not lunch_taken:
            lunch_duration = random.uniform(12, 18)

            event_queue.put({
                "type": "lunch_started",
                "examiner_name": examiner_name
            })

            time.sleep(lunch_duration)
            lunch_taken = True

            event_queue.put({
                "type": "lunch_finished",
                "examiner_name": examiner_name
            })

    result_queue.put({
        "type": "examiner_summary",
        "examiner_name": examiner_name,
        "total_students": total_students,
        "failed": failed,
        "work_time": work_time
    })

def apply_event(event, students_by_name, examiners_by_name):
    etype = event["type"]

    if etype == "exam_started":
        examiner = examiners_by_name[event["examiner_name"]]
        student = students_by_name[event["student_name"]]

        examiner.current_student = student.name
        student.examiner = examiner.name
        student.t_start = event["t_start"]

    elif etype == "exam_finished":
        examiner = examiners_by_name[event["examiner_name"]]
        student = students_by_name[event["student_name"]]

        examiner.current_student = None
        student.status = event["status"]
        student.t_end = event["t_end"]

        examiner.total_students += 1
        if event["status"] == "Провалил":
            examiner.failed += 1
        examiner.work_time += event["duration"]

    elif etype == "lunch_started":
        examiner = examiners_by_name[event["examiner_name"]]
        examiner.current_student = None
        examiner.is_on_lunch = True

    elif etype == "lunch_finished":
        examiner = examiners_by_name[event["examiner_name"]]
        examiner.is_on_lunch = False


def main():
    with open("students.txt", "r", encoding="utf-8") as f:
        students = list(map(lambda line: Student(*line.strip().split()), filter(str.strip, f)))

    with open("examiners.txt", "r", encoding="utf-8") as f:
        examiners = list(map(lambda line: Examiner(*line.strip().split()), filter(str.strip, f)))

    with open("questions.txt", "r", encoding="utf-8") as f:
        questions = list(map(lambda line: Question(line.strip()), filter(str.strip, f)))

    student_queue = Queue()
    result_queue = Queue()
    event_queue = Queue()

    for student in students:
        student_queue.put({
            "name": student.name,
            "gender": student.gender
        })

    t0 = time.time()
    processes = []

    for examiner in examiners:
        p = Process(
            target=examiner_worker,
            args=(
                examiner.name,
                examiner.gender,
                student_queue,
                result_queue,
                event_queue,
                questions,
                t0
            )
        )
        processes.append(p)
        p.start()

    students_by_name = {student.name: student for student in students}
    examiners_by_name = {examiner.name: examiner for examiner in examiners}

    while any(p.is_alive() for p in processes) or not event_queue.empty():
        while not event_queue.empty():
            event = event_queue.get()
            apply_event(event, students_by_name, examiners_by_name)

        clear_screen()
        print_students_table(students)
        print()
        print_examiners_table(examiners)
        print()
        remaining = sum(1 for s in students if s.status == "Очередь")
        print(f"Осталось в очереди: {remaining} из {len(students)}")
        print(f"Время с момента начала экзамена: {time.time() - t0:.2f}")

        time.sleep(0.2)

    for p in processes:
        p.join()

    while not event_queue.empty():
        event = event_queue.get()
        apply_event(event, students_by_name, examiners_by_name)    

    collect_results(students, examiners, questions, result_queue)
    clear_screen()
    print_final_results(students, examiners, questions)



def print_final_results(students, examiners, questions):
    print_final_students_table(students)
    print()
    print_final_examiners_table(examiners)
    print()

    total_time = max(
        (student.t_end for student in students if student.t_end is not None),
        default=0.0
    )

    best_students = get_best_students(students)
    best_examiners = get_best_examiners(examiners)
    expelled_students = get_expelled_students(students)
    best_questions = get_best_questions(questions)
    exam_result = get_exam_result(students)

    print(f"Время с момента начала экзамена и до момента и его завершения: {total_time:.2f}")
    print(f"Имена лучших студентов: {', '.join(best_students) if best_students else '-'}")
    print(f"Имена лучших экзаменаторов: {', '.join(best_examiners) if best_examiners else '-'}")
    print(f"Имена студентов, которых после экзамена отчислят: {', '.join(expelled_students) if expelled_students else '-'}")
    print(f"Лучшие вопросы: {', '.join(best_questions) if best_questions else '-'}")
    print(f"Вывод: {exam_result}")

def collect_results(students, examiners, questions, result_queue):
    students_by_name = {student.name: student for student in students}
    examiners_by_name = {examiner.name: examiner for examiner in examiners}
    questions_by_text = {question.text: question for question in questions}

    while not result_queue.empty():
        result = result_queue.get()

        if result["type"] == "student_result":
            student = students_by_name[result["student_name"]]
            student.status = result["status"]
            student.examiner = result["examiner_name"]
            student.t_start = result["t_start"]
            student.t_end = result["t_end"]

            for question_text in result["successful_questions"]:
                questions_by_text[question_text].success_count += 1

        elif result["type"] == "examiner_summary":
            examiner = examiners_by_name[result["examiner_name"]]
            examiner.total_students = result["total_students"]
            examiner.failed = result["failed"]
            examiner.work_time = result["work_time"]


if __name__ == "__main__":
    main()