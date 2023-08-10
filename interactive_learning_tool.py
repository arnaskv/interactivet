import csv


def main():
    modes = ['Add questions', 'View statistics', 'Disable/enable questions', 'Practice', 'Test', 'Quit']
    
    print('Hi, this is your interactive learning tool.')

    while True:
        display_menu(modes)

        mode = get_choice(modes, promt='Mode: ')

        if mode == modes[0]:
            questionnaire = Questionnaire()
            add_question(questionnaire)
        elif mode == modes[1]:
            pass
        elif mode == modes[2]:
            pass
        elif mode == modes[3]:
            pass
        elif mode == modes[4]:
            pass
        elif mode == modes[5]:
            print('Exiting the program.')
            break


def display_menu(options):
    print('Please choose from the following modes:\n')
    for idx, option in enumerate(options, start=1):
        print(f'{idx}. {option}')
    print()


def get_choice(choices, promt='Your choice'):
    choice = input(promt).capitalize()
    if choice in choices:
        return choice
    else:
        return get_choice(choices, promt)


def add_question(questionnaire, n=1):
    question_text = input('Your question: ')
    question_type = input('Choose the type of question, either "free-form" or "choice": ').strip().lower()

    question = Question(n, question_text, question_type)

    question = Question(n, question_text, question_type)

    if question_type == 'choice':
        question.get_choices()
        question.get_answer()
        question.get_choices()
        question.get_answer()
    else:
        question.get_answer()

        question.get_answer()

    
    questionnaire.add_question(question)

    if input('Would you like to add another question? ').lower() in ['yes', 'y']:
        add_question(questionnaire, n+1)
    else:
        questionnaire.write_questions()
        return


class Question:
    def __init__(self, question_id, question_text, question_type, answer='', enabled=True, choices=[]):  
        self.question_id = question_id
        self.enabled = enabled
        self.question_text = question_text
        self._question_type = question_type
        self.choices = choices
        self.answer = answer

    @property
    def question_type(self):    
        return self._question_type
    
    @question_type.setter
    def question_type(self, question_type):
        if question_type not in ['free-form', 'choice']:
            raise ValueError('Invalid question type.')
        self._question_type = question_type

    def add_choice(self, choice):
        self.choices.append(choice)

    def get_choices(self):
        while True:
            choice = input("Enter a choice (or type 'done' to finish): ")
            if choice.lower() == 'done' and len(self.choices) > 1:
                break
            self.add_choice(choice)

    def get_answer(self):
        self.answer = input('Answer: ')

    def add_choice(self, choice):
        self.choices.append(choice)

    def get_choices(self):
        while True:
            choice = input("Enter a choice (or type 'done' to finish): ")
            if choice.lower() == 'done' and len(self.choices) > 1:
                break
            self.add_choice(choice)

    def get_answer(self):
        self.answer = input('Answer: ')


class Questionnaire:
    def __init__(self, csv_file='questions.csv'):
        self.csv_file = csv_file
        self.questions = []
        self.load_questions()
        self.points = 0

    def add_question(self, question):
        self.questions.append(question)

    def input_question(self):
        pass

    def input_question(self):
        pass

    def ask_question(self, question):
        print(f'{question.question_id}. {question.question_text}')
        print(f'{question.question_id}. {question.question_text}')
        if question.question_type =='choice':
            for choice in question.choices:
                print(f'- {choice}')
            user_choice = input('Your choice: ').strip().lower()
            if user_choice == question.answer:
                print('Correct!')
                return True
            else:
                print('That is not right!')
                return False

    def ask_all(self):
        self.points = 0
        for _ in self.questions:
            if self.ask_question():
                self.points += 1

    def get_points(self):
        return self.points

    def load_questions(self):
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.questions.append(row)

    def write_questions(self):
        with open(self.csv_file, "w", newline='') as file:
            field_names = ['question_id', 'enabled', 'question_text', 'question_type', 'choices', 'answer']
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            
            for q in self.questions:
                row_dict ={
                    'question_id': q.question_id,
                    'enabled': q.enabled,
                    'question_text': q.question_text,
                    'question_type': q._question_type,
                    'choices': q.choices,
                    'answer': q.answer,
                }
                writer.writerow(row_dict)

    def reset_questions(self):
        with open(self.csv_file, 'w') as file:
            file.write('')
        self.questions.clear()

    def question_enabled(self):
        pass

    def display_questions(self):
        for i, q in enumerate(self.questions, start=1):
            print(f"{i}. {q['question_text']}")
            if q['question_type'] == 'choice':
                print("Choices:", ', '.join(q['choices']))
                print("Choices:", ', '.join(q['choices']))
            print("Answer:", q['answer'])
            print()


if __name__ == '__main__':
    main()