# 클래식 음악 퀴즈 게임 - 프로그램 시작 파일


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


class QuizGame:
    """게임 전체(메뉴, 진행)를 관리하는 클래스"""

    MENU_COUNT = 5  # 메뉴 개수 (1~5)

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()
        print("=" * 40)
        print("       🎻 클래식 음악 퀴즈 게임 🎻")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def read_number(self, prompt, min_value, max_value):
        """min_value~max_value 사이의 숫자를 받을 때까지 계속 다시 묻는다."""
        while True:
            raw = input(prompt).strip()  # strip(): 앞뒤 공백 제거

            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue

            try:
                number = int(raw)  # 글자 -> 숫자 변환 (실패하면 ValueError)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def run(self):
        """메뉴를 보여주고, 사용자가 종료를 고를 때까지 반복한다."""
        while True:
            self.show_menu()
            choice = self.read_number("선택: ", 1, self.MENU_COUNT)

            if choice == 1:
                print("\n(퀴즈 풀기 기능은 준비 중입니다.)")
            elif choice == 2:
                print("\n(퀴즈 추가 기능은 준비 중입니다.)")
            elif choice == 3:
                print("\n(퀴즈 목록 기능은 준비 중입니다.)")
            elif choice == 4:
                print("\n(점수 확인 기능은 준비 중입니다.)")
            else:
                print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 종료 시 에러 화면 대신 안내 후 종료
        print("\n\n⚠️ 입력이 중단되어 게임을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()