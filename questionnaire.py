import csv
import random
import ast
import json
from datetime import datetime
import numpy
import getch
from question import Question


def wait_for_keypress():
    print("Press any key to continue...")
    getch.getch()  # Wait for a keypress


class Questionnaire():
    def __init__(self, questions_csv='questions.csv', statistics_csv='statistics.csv'):
        self.questions_csv = questions_csv
        self.questions = []
        self.load_questions()

    def add_question(self, question):
        self.questions.append(question)

    def input_question(self):
        """Prompts user to input a question"""
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
        """
        Asks user a question.
        Adds +1 to question guessed times.
        Adds +1 to question correct key if answered right.

        Args:
            question_id(int)
        
        Returns:
            Bool value whether user answer was correct.
        """
        q = ''
        for index, question in enumerate(self.questions):
            if id == question['question_id']:
                q = self.questions[index]
                break

        print(f'\n{q["question_text"]}')
        if q['question_type'] =='c':
            for choice in q['choices']:
                print(f'- {choice}')
        user_answer = input('Your answer: ').lower()
        if user_answer == q['answer'].lower():
            q['guessed'] += 1
            q['correct'] += 1
            return True
        else:
            q['guessed'] += 1
            return False

    def ask_more_questions(self, sequence):
        """Asks questions in a given sequence  and tracks points for correct aswers"""
        points = 0
        for number in sequence:
            if self.ask_question(number):
                points += 1
        return points

    def load_questions(self):
        """Takes question data from csv file, parses it into required data types and loads into questions[]"""
        try:
            with open(self.questions_csv, "r") as file:
                reader = csv.DictReader(file)
                for question in reader:
                    question['question_id'] = int(question['question_id'])
                    question['enabled'] = json.loads(question['enabled'].lower())
                    question['choices'] = ast.literal_eval(question['choices'])
                    question['guessed'] = int(question['guessed'])
                    question['correct'] = int(question['correct'])
                    self.questions.append(question)
        except FileNotFoundError:
            # This will just create an empty CSV file
            with open(self.questions_csv, 'w', newline='') as file:
                pass

    def write_questions(self):
        """Writes questions to a csv file"""
        with open(self.questions_csv, "w", newline='') as file:
            field_names = ['question_id', 'enabled', 'question_text', 'question_type', 'choices', 'answer', 'guessed', 'correct']
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for question in self.questions:
                # if question['enabled']: question['enabled'] = 1 else: question['enabled'] = 0
                writer.writerow(question)

    def reset_questions(self):
        """Clears all questions available in stack and in questions.csv"""
        if self.yes_no('Are you sure you want to reset all questions?'):
            with open(self.questions_csv, 'w') as file:
                file.write('')
            self.questions.clear()
            print('Question reset completed.')
        else:
            print('Question reset cancelled.')

    def get_new_id(self):
        return len(self.questions) + 1

    def enabled_questions(self):
        """"Returns enabled questions ids list"""
        enabled = []
        for q in self.questions:
            if q['enabled'] == True:
                enabled.append(q['question_id'])
        return enabled

    def print_out_question(self, index):
        question = self.questions[index]
        print(f'Question: {question["question_text"]}')
        if question['question_type'] == 'c':
            print('Choices:')
            for index, choice in enumerate(question['choices'], start=1):
                print(f'{index}. {choice}')
        print(f'Answer: {question["answer"]}')

    def enable_disable(self):
        """Asks for question id, if valid, asks if user wants to change enabled status"""
        id = None
        try:
            id = int(input('Question id: '))
        except ValueError:
            print('"Id" must be an integer.')

        for index, question in enumerate(self.questions):
            if id == question['question_id']:
                self.print_out_question(index)
                if id in self.enabled_questions():
                    if self.yes_no('Question is enabled. Do you want to disable it?'):
                        question['enabled'] = False
                        return
                else:
                    if self.yes_no('Question is disabled. Do you want to enable it?'):
                        question['enabled'] = True
                        return
        print('Question not found.')

    def enable_disable_mode(self):
        while True:
            self.enable_disable()
            answer = self.yes_no('Disable/enable another question?')
            if not answer:
                self.write_questions()
                break

    def yes_no(self, prompt):
        """
        Promts user to choose [Yes/No]
        
        Returns:
            bool value of the answer
        """
        while True:
            answer = input(f'{prompt}\n[Yes/No] ').strip().lower()
            if  answer in ['yes', 'y']:
                return True
            elif answer in ['no', 'n']:
                return False

    def test_mode(self):
        """Asks user the amount of questions requested in a randomized order from enabled questions"""
        available_questions = len(self.enabled_questions())

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
        self.write_questions()

        print(f'You have answered {points} questions correctly.')
        wait_for_keypress()

    def write_result(self, result):
        """Writes test mode results, date, time to a txt file."""
        write_date = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')

        with open('results.txt', 'a') as file:
            file.write(','.join([result, write_date]) + '\n')

    def view_statistics(self):
        """Prints out condensed information about all available questions"""
        print('Statistics:\n')
        for q in self.questions:
            print(f'ID: {q["question_id"]} | Enabled: {q["enabled"]}\nQuestion: {q["question_text"]}')
            if q['question_type'] == 'c':    
                print('Choices:', ' | '.join(q['choices']))
            print(f'Question asked: {q["guessed"]} | Answered correctly: {q["correct"]}\n')
        wait_for_keypress()

    def question_weight(self, id):
        for q in self.questions:
            if id == q['question_id']:
                x = float(q['correct'])
                y = float(q['guessed'])
                try:
                    weight = x/y
                    return weight
                except ZeroDivisionError:
                    return 1

    def practice(self):
        """Asks questions randomly with inverse weighed choice"""
        print('Practice mode. To exit mode enter "ctrl + d"')
        try:
            available_questions = len(self.enabled_questions())

            if available_questions < 5:
                print('Not enough questions. Minimum: 5')
                wait_for_keypress()
                return
            
            while True:
                weights = []
                for question in self.enabled_questions():
                    weights.append(self.question_weight(question))
                
                weights = numpy.reciprocal(weights)
                weights = weights / numpy.sum(weights)

                random_choice = numpy.random.choice(self.enabled_questions(), p=weights)
                self.ask_question(random_choice)
        except EOFError:
            self.write_questions()
