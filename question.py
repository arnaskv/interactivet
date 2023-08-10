import csv


class Question:
    def __init__(self):
        self.questions = []

    def add_question(self, question_text, question_type, options=None, answer=None):
        """
        Add a question to the list.

        Args:
            question_text (str): The text of the question.
            question_type (str): The type of question, either 'free_form' or 'choice'.
            options (list): List of options for choice questions (optional).
            answer (str): Answer for both free-form and choice questions (optional).
        """
        if question_type not in ['free-form', 'choice']:
            raise ValueError("Invalid question type. Use 'free-form' or 'choice'.")

        if question_type == 'choice' and not options:
            raise ValueError("Options are required for choice questions.")

        self.questions.append({
            'id': len(self.questions) + 1,
            'enabled': True,
            'question_text': question_text,
            'question_type': question_type,
            'options': options,
            'answer': answer
        })

    def write_questions(self):
        csv_file_path = 'questions.csv'

        with open(csv_file_path, "w", newline='') as csv_file:
            field_names = ['id', 'enabled', 'question_text', 'question_type', 'options', 'answer']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            writer.writerows(self.questions)

        print('Question added successfully.')

    def get_questions():
        pass

    def display_questions(self):
        for i, q in enumerate(self.questions, start=1):
            print(f"{i}. {q['question_text']}")
            if q['question_type'] == 'choice':
                print("Options:", ', '.join(q['options']))
            print("Answer:", q['answer'])
            print()