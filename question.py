class Question:
    """Question class for handling single question handling and input"""
    def __init__(self, question_id, question_text, question_type=None, answer='', enabled=True):
        self.question_id = question_id
        self.enabled = enabled
        self.question_text = question_text
        self._question_type = question_type
        self.choices = []
        self.answer = answer
        self.guessed = 0
        self.correct = 0

    @property
    def question_type(self):    
        return self._question_type
    
    @question_type.setter
    def question_type(self, question_type):
        question_type = question_type.strip().lower()
        types = ['free-form', 'f', 'choice', 'c']
        if question_type not in types:
            raise ValueError('Invalid question type.')
        elif question_type in types[:2]:
            self._question_type = 'f'
        else:
            self._question_type = 'c'
        

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

    def convert_to_dict(self):
        return {
                    'question_id': self.question_id,
                    'enabled': self.enabled,
                    'question_text': self.question_text,
                    'question_type': self._question_type,
                    'choices': self.choices,
                    'answer': self.answer,
                    'guessed': self.guessed,
                    'correct': self.correct,
                }
    