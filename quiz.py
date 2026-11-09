# ==========================================================
# quiz.py : 퀴즈 "한 문제"를 만드는 설계도(클래스)가 들어 있는 파일
#
# 쉽게 말하면, 붕어빵 틀 같은 거예요.
# 이 틀(Quiz 클래스)로 문제 붕어빵(퀴즈 객체)을 여러 개 찍어 낼 수 있어요.
# ==========================================================


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    # __init__ : 새 문제를 만들 때 "제일 먼저 자동으로" 실행되는 준비 단계
    # self     : 지금 만들어지고 있는 "바로 그 문제 자신"을 가리키는 말
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 글 (예: "교향곡 9번 '합창'을 작곡한 사람은?")
        self.choices = choices    # 보기 4개를 담은 목록(list)
        self.answer = answer      # 정답 번호 (1, 2, 3, 4 중 하나)

    # 문제를 화면에 보여주는 기능
    def display(self, number):
        """문제와 선택지를 화면에 출력한다. number는 '몇 번째 문제'인지."""
        print("-" * 40)                # 구분선: "-"를 40개 이어서 그려요
        print(f"[문제 {number}]")       # 예: [문제 1]
        print(self.question)            # 문제 글을 보여줘요
        print()                         # 한 줄 띄우기
        # 보기 4개를 1번부터 번호를 붙여서 하나씩 보여줘요
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")     # 예: 1. 모차르트
        print()

    # 정답인지 확인하는 기능
    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 돌려준다."""
        # 고른 번호와 정답 번호가 같으면 True(맞음), 다르면 False(틀림)
        return user_answer == self.answer

    # 파일에 저장하기 좋은 모양(dict)으로 바꾸는 기능
    def to_dict(self):
        """JSON 파일에 저장할 수 있도록 dict(사전) 형태로 바꾼다."""
        # dict(사전)는 "이름표: 내용" 짝으로 정리한 모양이에요
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    # 파일에서 읽은 내용(dict)을 다시 문제(Quiz)로 바꾸는 기능
    # @staticmethod : 문제를 만들기 전에도 쓸 수 있는 기능이라는 표시
    @staticmethod
    def from_dict(data):
        """JSON에서 읽은 dict를 Quiz 객체로 되돌린다. 형식이 이상하면 ValueError."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        # 내용이 이상하면 오류를 알려요
        # → 그러면 main.py가 "파일이 손상됐다"고 판단하고 기본 퀴즈로 복구해요

        # 1) 문제 글은 비어 있지 않은 글자(str)여야 해요
        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제 형식이 올바르지 않습니다.")

        # 2) 보기는 4개짜리 목록(list)이고, 4개 모두 비어 있지 않은 글자여야 해요
        #    (직접 입력할 때와 똑같은 기준이에요)
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지 형식이 올바르지 않습니다.")
        for choice in choices:
            if not isinstance(choice, str) or choice.strip() == "":
                raise ValueError("선택지 형식이 올바르지 않습니다.")

        # 3) 정답은 "진짜 정수(int)"이고 1~4 사이여야 해요
        #    type(answer) is int : 2.0(소수)이나 True(참/거짓)는 정수로 치지 않아요
        #    (파이썬은 2.0 == 2 를 같다고 보기 때문에 이렇게 정확히 확인해요)
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호 형식이 올바르지 않습니다.")
        return Quiz(question, choices, answer)