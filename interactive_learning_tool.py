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


def add_question(questionnaire, n=0):
    prompt = input('Your question: ')
    question_type = input('Choose the type of question, either "free-form" or "choice": ').strip().lower()

    if question_type == 'choice':
        choices = get_question_choices()
        answer = input('Answer: ')
        question = Question(n, prompt, answer, choices=choices)
    else:
        answer = input('Answer: ')
        question = Question(n, prompt, answer)
    
    questionnaire.add_question(question)

    if input('Would you like to enter another question? ').lower() in ['yes', 'y']:
        add_question(n+1)
    else:
        questionnaire.write_questions()
        return


def get_question_choices():
    options = []
    while True:
        option = input("Enter a choice (or type 'done' to finish options): ")
        if option.lower() == 'done':
            break
        options.append(option)
    return options


class Question:
    def __init__(self, question_id, prompt, answer, enabled=True, choices=[]):  
        self.question_id = question_id
        self.enabled = enabled
        self.prompt = prompt
        self._question_type = None
        self.choices = choices
        self.answer = answer

    def get_question_type(self):    
        return self._question_type
    
    def set_question_type(self, question_type):
        if question_type not in ['free-form', 'choice']:
            raise ValueError('Invalid question type.')
        self._question_type = question_type


class Questionnaire:
    def __init__(self, csv_file='questions.csv'):
        self.csv_file = csv_file
        self.questions = []
        self.load_questions()
        self.points = 0

    def add_question(self, question):
        self.questions.append(question)

    def ask_question(self, question):
        print(f'{question.question_id}. {question.prompt}')
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
            field_names = ['id', 'enabled', 'prompt', 'question_type', 'choices', 'answer']
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(self.questions)

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
                print("Options:", ', '.join(q['options']))
            print("Answer:", q['answer'])
            print()


if __name__ == '__main__':
    main()