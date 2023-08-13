from questionnaire import Questionnaire


def main():
    # modes with access shorteners in a list
    modes = [
                ['1', 'Add questions', 'A'],
                ['2','View statistics', 'V'],
                ['3','Disable/enable questions', 'D'],
                ['4','Practice', 'P'],
                ['5','Test', 'T'],
                ['6','Reset', 'R'],
                ['7','Quit', 'Q'],
            ]

    print('Hi, this is your interactive learning tool.')
    questionnaire = Questionnaire()

    while True:
        display_menu(modes)

        mode = get_choice(modes, promt='Mode: ')

        if mode == 0:
            questionnaire.input_multiple_questions()
        elif mode == 1:
            questionnaire.view_statistics()
        elif mode == 2:
            questionnaire.enable_disable_mode()
        elif mode == 3:
            questionnaire.practice()
        elif mode == 4:
            questionnaire.test_mode()
        elif mode == 5:
            questionnaire.reset_questions()
        elif mode == 6:
            print('Exiting the program.')
            break


def display_menu(options):
    print('Please choose from the following modes:\n')
    for option in options:
        print(f'{option[0]}. {option[1]}({option[2]})')
    print()


def get_choice(choices, promt='Your choice'):
    answer = input(promt).lower().capitalize()
    for idx, choice in enumerate(choices):
        if answer in choice:
            print()
            return idx
    # If no match was found, prompt the user again
    return get_choice(choices, promt)


if __name__ == '__main__':
    main()