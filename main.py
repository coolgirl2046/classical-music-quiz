# 클래식 음악 퀴즈 게임 - 프로그램 시작 파일

import json
import os

from quiz import Quiz

# state.json 위치: main.py가 있는 폴더(프로젝트 루트)
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")



class QuizGame:
    """게임 전체(메뉴, 진행, 저장)를 관리하는 클래스"""

    MENU_COUNT = 5  # 메뉴 개수 (1~5)

    def __init__(self):
        self.quizzes = []        # 퀴즈 목록 (list)
        self.best_score = None   # 최고 점수 (아직 안 풀었으면 None)
        self.load_state()        # 시작할 때 state.json에서 불러오기

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

    # ---------- 파일 저장 / 불러오기 ----------

    def load_state(self):
        """state.json을 읽어 퀴즈와 최고 점수를 불러온다. 문제가 있으면 기본 데이터로 시작."""
        if not os.path.exists(STATE_FILE):
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best = data.get("best_score")
            if best is not None and not isinstance(best, int):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
            self.best_score = best
            best_text = "없음" if best is None else f"{best}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다. 이번 변경 내용은 저장되지 않았습니다.")

    # ---------- 화면 / 입력 ----------

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

    def read_text(self, prompt):
        """빈 칸이 아닌 글자를 입력받을 때까지 계속 다시 묻는다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 빈 칸은 입력할 수 없습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 게임 기능 ----------

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
        self.update_best_score(score)
        print("=" * 40)

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
        self.save_state()  # 추가하자마자 파일에 저장
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

    def update_best_score(self, score):
        """이번 점수가 최고 점수보다 높으면 최고 점수를 바꾸고 저장한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()  # 새 최고 점수를 파일에 저장
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"(최고 점수는 {self.best_score}점입니다.)")

    def show_best_score(self):
        """최고 점수를 보여준다. 아직 안 풀었으면 안내한다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 먼저 풀어보세요!")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

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
                self.show_best_score()
            else:
                self.save_state()
                print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 종료 시: 저장 후 안내하고 종료
        game.save_state()
        print("\n\n⚠️ 입력이 중단되어 데이터를 저장하고 안전하게 종료합니다.")


if __name__ == "__main__":
    main()