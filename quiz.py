# Quiz 클래스: 퀴즈 한 문제를 표현한다


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제와 선택지를 화면에 출력한다. number는 '몇 번째 문제'인지."""
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 돌려준다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 파일에 저장할 수 있도록 dict(사전) 형태로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """JSON에서 읽은 dict를 Quiz 객체로 되돌린다. 형식이 이상하면 ValueError."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not isinstance(choices, list) \
                or len(choices) != 4 or answer not in (1, 2, 3, 4):
            raise ValueError("퀴즈 형식이 올바르지 않습니다.")
        return Quiz(question, choices, answer)