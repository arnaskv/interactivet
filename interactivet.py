from question import Question


def main():
    modes = ['Adding questions', 'Statistics viewing', 'Disable/enable questions', 'Practice', 'Test', 'Quit']
    
    print('Hi, this is an interactive learning tool.')

    while True:
        display_menu(modes)

        mode = get_choice(modes, promt='Mode: ')

        if mode == modes[0]:
            add_questions()
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

    for idx, option in enumerate(options):
        print(f'{idx+1}. {option}')
    print()


def get_choice(choices, promt='Your choice'):
    choice = input(promt).capitalize()
    if choice in choices:
        return choice
    else:
        return get_choice(choices, promt)


def add_questions(questions=None):
    if questions is None:
        questions = Question()

    text = input('Your question: ')
    question_type = input('Choose the type of question, either "free-form" or "choice": ')

    if question_type == 'choice':
        options = get_choice_options()
        answer = input('Answer: ')
        questions.add_question(question_text=text, question_type=question_type, options=options, answer=answer)
    else:
        answer = input('Answer: ')
        questions.add_question(question_text=text, question_type=question_type, answer=answer)

    if input('Would you like to enter another question? ').lower() in ['yes', 'y']:
        add_questions(questions)
    else:
        questions.write_questions()
        return


def get_choice_options():
    options = []
    while True:
        option = input("Enter an option (or type 'done' to finish options): ")
        if option.lower() == 'done':
            break
        options.append(option)
    return options


if __name__ == '__main__':
    main()