import getch
import csv
import random
import ast
from datetime import datetime
from question import Question


class Questionnaire():
    def __init__(self, questions_csv='questions.csv', statistics_csv='statistics.csv'):
        self.questions_csv = questions_csv
        self.questions = []
        self.load_questions()
        self.points = 0

    def add_question(self, question):
        self.questions.append(question)

    def input_question(self):
        question_text = input('Your question: ').capitalize()
        question_id = self.get_new_id()

        question = Question(question_id, question_text)
        question.question_type = input('Choose the type of question, either "free-form(F)" or "choice(C)": ')

        if question.question_type == 'c':
            question.get_choices()
            question.get_answer()
        else:
            question.get_answer()

        question = question.convert_to_dict()
        self.add_question(question)

    def input_multiple_questions(self):
        while True:
            self.input_question()
            while True:
                answer = self.yes_no('Would you like to add another question?')
                if  answer:
                    break
                else:
                    self.write_questions()
                    return

    def ask_question(self, id):
        q = {}
        for question in self.questions:
            if id == int(question['question_id']):
                q = question
        print(f'{q["question_id"]}. {q["question_text"]}')
        if q['question_type'] =='c':
            for choice in q['choices']:
                print(f'- {choice}')
            user_choice = input('Your choice: ').lower()
            if user_choice == q['answer'].lower():
                print('Correct!')
                return True
            else:
                print('That is not right!')
                return False

    def ask_more_questions(self, sequence):
        points = 0
        for number in sequence:
            if self.ask_question(number):
                points += 1
        return points

    def get_points(self):
        return self.points

    def load_questions(self):
        try:
            with open(self.questions_csv, "r") as file:
                reader = csv.DictReader(file)
                for question in reader:
                    question['question_id'] = int(question['question_id'])
                    question['enabled'] = bool(question['enabled'])
                    question['choices'] = ast.literal_eval(question['choices'])
                    question['guessed'] = int(question['guessed'])
                    question['correct'] = int(question['correct'])
                    self.questions.append(question)
        except FileNotFoundError:
            # This will just create an empty CSV file
            with open(self.questions_csv, 'w', newline='') as file:
                pass

    def write_questions(self):
        with open(self.questions_csv, "w", newline='') as file:
            field_names = ['question_id', 'enabled', 'question_text', 'question_type', 'choices', 'answer', 'guessed', 'corect']
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for question in self.questions:
                writer.writerow(question)

    def reset_questions(self):
        if self.yes_no('Are you sure you want to reset all questions?'):
            with open(self.questions_csv, 'w') as file:
                file.write('')
            self.questions.clear()
            print('Question reset completed.')
        else:
            print('Question reset cancelled.')

    def get_new_id(self):
        return len(self.questions) + 1

    def is_enabled(self):
        while True:
            try:
                id = int(input('Question id: '))
                if id-1 >= self.get_new_id():
                    raise ValueError
                break
            except ValueError:
                print('"Id" must be a valid integer in scope.')
        for q in self.questions:
            if id == int(q['question_id']):
                return id, q['enabled']

    def enabled_count(self):
        count = 0
        for q in self.questions:
            if q['enabled'] == True:
                count += 1
        return count

    def enable_disable(self):
        id, status = self.is_enabled()
        print(f"Debug: id={id}, status={status}")
        q = self.questions[id-1]
        print(f"Debug: q={q}")

        print(f'Question: {q["question_text"]}')
        if q['question_type'] == 'c':
            print('Choices:')
            for index, choice in enumerate(q['choices'], start=1):
                print(f'{index}. {choice}')
        print(f'Answer: {q["answer"]}')

        if status:
            if self.yes_no('Question is enabled. Do you want to disable it?'):
                q['enabled'] = False
        else:
            if self.yes_no('Question is disabled. Do you want to enable it?'):
                q['enabled'] = True

    def enable_disable_mode(self):
        while True:
            self.enable_disable()
            answer = self.yes_no('Do you wish to change the state of another question?')
            if not answer:
                self.write_questions()
                break

    def yes_no(self, prompt):
        while True:
            answer = input(f'{prompt}\n[Yes/No] ').strip().lower()
            if  answer in ['yes', 'y']:
                return True
            elif answer in ['no', 'n']:
                return False

    def test_mode(self):
        available_questions = self.enabled_count()

        if available_questions < 5:
            print('Not enough questions. Minimum: 5')
            wait_for_keypress()
            return
        print(f'Available questions for test mode: {available_questions}')

        question_number = 0
        while True:
            try:
                question_number = int(input('How many questions do you want to take? '))
                if question_number > available_questions:
                    raise ValueError
                break
            except ValueError:
                print('Enter an integer lesser than total questions available.')
        
        ids = list(range(1, available_questions+1))
        random.shuffle(ids)
        sequence = ids[:question_number]
        points = self.ask_more_questions(sequence)

        result = f'{points}/{question_number}'
        self.write_result(result)

        print(f'You have answered {points} questions correctly.')
        wait_for_keypress()

    def write_result(self, result):
        write_date = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')

        with open('results.txt', 'a') as file:
            file.write(','.join([result, write_date]) + '\n')
        

def wait_for_keypress():
    print("Press any key to continue...")
    getch.getch()  # Wait for a keypress
