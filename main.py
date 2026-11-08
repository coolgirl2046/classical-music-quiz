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

    def __init__(self):
        self.quizzes = self.create_default_quizzes()  # 퀴즈 목록 (list)
        self.best_score = None  # 최고 점수 (아직 안 풀었으면 None)

    def create_default_quizzes(self):
        """처음 실행할 때 쓸 기본 퀴즈 5개를 만들어 돌려준다."""
        return [
            Quiz("교향곡 9번 '합창'을 작곡한 사람은?",
                 ["모차르트", "베토벤", "바흐", "하이든"], 2),
            Quiz("비발디의 '사계'는 어떤 악기가 주인공인 협주곡일까?",
                 ["피아노", "첼로", "바이올린", "플루트"], 3),
            Quiz("'음악의 아버지'라고 불리는 작곡가는?",
                 ["바흐", "헨델", "슈베르트", "브람스"], 1),
            Quiz("오페라 '마술피리'를 작곡한 사람은?",
                 ["베르디", "푸치니", "바그너", "모차르트"], 4),
            Quiz("다음 중 차이콥스키의 발레 음악이 아닌 것은?",
                 ["백조의 호수", "호두까기 인형", "잠자는 숲속의 미녀", "봄의 제전"], 4),
        ]
    
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
    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)  # 전체 문제 수
        correct_count = 0          # 맞힌 문제 수
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = self.read_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct_count += 1
            else:
                right = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{right}'입니다.\n")

        score = round(correct_count / total * 100)  # 100점 만점으로 환산
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        print("=" * 40)
    def read_text(self, prompt):
        """빈 칸이 아닌 글자를 입력받을 때까지 계속 다시 묻는다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 빈 칸은 입력할 수 없습니다. 다시 입력하세요.")
                continue
            return text

    def add_quiz(self):
        """사용자에게 문제, 선택지 4개, 정답 번호를 받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):  # 1, 2, 3, 4
            choice = self.read_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 총 {len(self.quizzes)}개)")
    def show_quiz_list(self):
        """등록된 퀴즈의 문제만 번호와 함께 보여준다."""
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def run(self):
        """메뉴를 보여주고, 사용자가 종료를 고를 때까지 반복한다."""
        while True:
            self.show_menu()
            choice = self.read_number("선택: ", 1, self.MENU_COUNT)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
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