import pytest
from question import Question
from questionnaire import Questionnaire


def main():
    test_yes_no()
    test_convert_to_dict()
    test_enabled_questions()


@pytest.fixture
def questionnaire():
    return Questionnaire(questions_csv='test_questions.csv')


def test_enabled_questions(questionnaire):
    assert questionnaire.enabled_questions() == [1, 2]


def test_yes_no(questionnaire, monkeypatch):
    user_input = "yes"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = questionnaire.yes_no("Do you like ice cream?")
    assert result == True

    user_input = "no"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = questionnaire.yes_no("Is it raining outside?")
    assert result == False


def test_convert_to_dict():
    q = Question(1, 'what?', 'c', answer='here')
    q.choices = ['here', 'there', 'somewhere']

    assert q.convert_to_dict() == {
        'question_id': 1,
        'enabled': True,
        'question_text': 'what?',
        'question_type': 'c',
        'choices': ['here', 'there', 'somewhere'],
        'answer': 'here',
        'guessed': 0,
        'correct': 0,
    }


if __name__ == '__main__':
    main()
