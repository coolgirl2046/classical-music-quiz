# ==========================================================
# main.py : 클래식 음악 퀴즈 게임을 "시작"하는 파일
#
# 이 파일에는 게임 전체를 움직이는 진행자(QuizGame 클래스)가 들어 있어요.
# 진행자는 메뉴 보여주기, 문제 내기, 점수 세기, 저장하기를 맡아요.
# 문제 한 개를 만드는 설계도(Quiz 클래스)는 quiz.py에 따로 있어요.
# ==========================================================

# import : 파이썬이 미리 만들어 둔 도구 상자를 꺼내 오는 것
import json    # JSON 파일을 읽고 쓰는 도구
import os      # 파일이 어디 있는지, 있는지 없는지 확인하는 도구
import random  # 순서를 무작위로 섞는 도구 (랜덤 출제에 사용)

from quiz import Quiz  # quiz.py에서 Quiz 설계도를 가져와요

# 저장 파일(state.json)의 위치 : main.py와 같은 폴더
# 변수 이름을 대문자로 쓴 건 "프로그램 내내 바뀌지 않는 값"이라는 약속이에요
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")



class QuizGame:
    """게임 전체(메뉴, 진행, 저장)를 관리하는 클래스"""

    MENU_COUNT = 5  # 메뉴 개수 (1~5)

    # 게임이 처음 만들어질 때 자동으로 실행되는 준비 단계
    def __init__(self):
        self.quizzes = []        # 퀴즈들을 담을 빈 목록(list)으로 시작
        self.best_score = None   # 최고 점수 (None = 아직 기록이 "없음")
        self.load_state()        # 저장해 둔 파일이 있으면 불러오기

    # 처음 실행할 때 쓸 기본 문제 5개
    def create_default_quizzes(self):
        """처음 실행할 때 쓸 기본 퀴즈 5개를 만들어 돌려준다."""
        # Quiz(문제, [보기 4개], 정답 번호) 모양으로 문제를 하나씩 만들어요
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
    # 게임을 껐다 켜도 문제와 점수가 남아 있게 해 주는 부분이에요.
    # 공책(state.json)에 적어 두었다가, 다음에 다시 펼쳐 읽는 것과 같아요.

    def load_state(self):
        """state.json을 읽어 퀴즈와 최고 점수를 불러온다. 문제가 있으면 기본 데이터로 시작."""
        # 1) 공책(파일)이 아예 없으면 → 기본 문제 5개로 시작
        if not os.path.exists(STATE_FILE):
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            return

        # 2) 공책이 있으면 읽어 보기
        # try : "일단 해 봐!"  /  except : "하다가 문제가 생기면 이렇게 해!"
        try:
            # 파일을 읽기("r") 모드로 열기. utf-8은 한글이 깨지지 않게 하는 설정
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)  # 파일 내용을 파이썬이 쓰는 모양(dict)으로 바꾸기
            # 저장된 문제들을 하나씩 Quiz로 되살리기
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best = data.get("best_score")
            # 최고 점수가 숫자가 아니면 이상한 파일이라고 판단
            if best is not None and type(best) is not int:
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
            self.best_score = best
            best_text = "없음" if best is None else f"{best}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")
        # 3) 공책이 찢어졌거나(내용이 망가졌거나) 읽다가 오류가 나면
        #    → 프로그램이 멈추지 않고, 기본 문제로 다시 시작해요
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        # 저장할 내용을 "이름표: 내용" 모양(dict)으로 정리
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            # 파일을 쓰기("w") 모드로 열고 내용을 적어요
            # ensure_ascii=False : 한글을 그대로 저장 / indent=4 : 보기 좋게 줄 맞춤
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True   # 저장 성공을 알려 줘요
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다. 이번 변경 내용은 저장되지 않았습니다.")
            return False  # 저장 실패를 알려 줘요

    # ---------- 화면 / 입력 ----------

    # 메뉴판 보여주기
    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()
        print("=" * 40)   # "="를 40개 이어 그린 줄
        print("       🎻 클래식 음악 퀴즈 게임 🎻")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # 숫자를 제대로 입력할 때까지 계속 물어보는 기능
    # 메뉴(1~5)와 정답(1~4)에 같은 기능을 다시 써요 → 범위만 바꿔서 넘겨 줘요
    def read_number(self, prompt, min_value, max_value):
        """min_value~max_value 사이의 숫자를 받을 때까지 계속 다시 묻는다."""
        # while True : 올바른 답이 나올 때까지 "계속 반복"
        while True:
            raw = input(prompt).strip()  # 입력받고, 앞뒤 빈칸은 지우기

            # 아무것도 안 쓰고 Enter만 누른 경우
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue  # continue : 처음으로 돌아가 다시 물어보기

            # 글자를 숫자로 바꿔 보기 ("abc"처럼 숫자가 아니면 실패)
            try:
                number = int(raw)  # 글자 -> 숫자 변환 (실패하면 ValueError)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            # 숫자이긴 한데 범위 밖인 경우 (예: 메뉴에서 9)
            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number  # 통과! 올바른 숫자를 돌려주고 반복 끝

    # 글자를 빈칸 없이 입력할 때까지 계속 물어보는 기능 (문제, 보기 입력에 사용)
    def read_text(self, prompt):
        """빈 칸이 아닌 글자를 입력받을 때까지 계속 다시 묻는다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 빈 칸은 입력할 수 없습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 게임 기능 ----------

    # [메뉴 1] 퀴즈 풀기
    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        # 문제가 하나도 없으면 안내만 하고 끝
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)  # 전체 문제 수
        correct_count = 0          # 맞힌 개수를 세는 계산기 (0부터 시작)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        # 카드 섞기처럼 문제 순서를 섞어요 (보너스: 랜덤 출제)
        questions = self.quizzes[:]  # 원본은 그대로 두고 복사본을 만들어서
        random.shuffle(questions)    # 복사본만 무작위로 섞기

        # for : 섞은 문제를 처음부터 끝까지 "하나씩" 꺼내며 반복
        for number, quiz in enumerate(questions, start=1):
            quiz.display(number)                                # 문제 보여주기
            user_answer = self.read_number("정답 입력: ", 1, 4)  # 답 받기 (1~4)

            # 맞았는지 확인
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct_count += 1  # 맞힌 개수 1 늘리기
            else:
                # 틀리면 정답을 알려줘요 (목록은 0번부터 세서 1을 빼요)
                right = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{right}'입니다.\n")

        # 점수 계산 : 맞힌 개수 ÷ 전체 × 100 (반올림)
        score = round(correct_count / total * 100)  # 100점 만점으로 환산
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        self.update_best_score(score)  # 최고 점수와 비교
        print("=" * 40)

    # [메뉴 2] 퀴즈 추가
    def add_quiz(self):
        """사용자에게 문제, 선택지 4개, 정답 번호를 받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")

        # 보기 4개를 하나씩 입력받아 목록에 차곡차곡 넣기
        choices = []
        for i in range(1, 5):  # i가 1, 2, 3, 4로 바뀌며 4번 반복
            choice = self.read_text(f"선택지 {i}: ")
            choices.append(choice)  # append : 목록 맨 뒤에 추가

        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

        # 입력받은 내용으로 새 문제를 만들어 목록에 넣고, 바로 저장
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()  # 추가하자마자 파일에 저장
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 총 {len(self.quizzes)}개)")

    # [메뉴 3] 퀴즈 목록 보기
    def show_quiz_list(self):
        """등록된 퀴즈의 문제만 번호와 함께 보여준다."""
        if len(self.quizzes) == 0:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        # 문제마다 [1], [2]... 번호를 붙여 보여주기
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    # 최고 점수 바꾸기 (퀴즈를 다 풀 때마다 실행)
    def update_best_score(self, score):
        """이번 점수가 최고 점수보다 높으면 최고 점수를 바꾸고 저장한다."""
        # 기록이 없거나, 이번 점수가 더 높으면 → 새 기록!
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()  # 새 최고 점수를 파일에 저장
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"(최고 점수는 {self.best_score}점입니다.)")

    # [메뉴 4] 점수 확인
    def show_best_score(self):
        """최고 점수를 보여준다. 아직 안 풀었으면 안내한다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 먼저 풀어보세요!")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

    # 게임 진행 : 메뉴를 보여주고, 고른 번호에 맞는 기능을 실행
    def run(self):
        """메뉴를 보여주고, 사용자가 종료를 고를 때까지 반복한다."""
        while True:  # 5번(종료)을 고를 때까지 계속 반복
            self.show_menu()
            choice = self.read_number("선택: ", 1, self.MENU_COUNT)

            # if / elif / else : 고른 번호에 따라 갈림길처럼 다른 길로 가요
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            else:
                # [메뉴 5] 종료 : 저장하고 반복을 멈춰요
                self.save_state()
                print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
                break  # break : 반복문 밖으로 나가기


# 프로그램의 출발점
def main():
    game = QuizGame()  # 게임 진행자를 만들고
    try:
        game.run()     # 게임 시작!
    except (KeyboardInterrupt, EOFError):
        # 게임 도중 Ctrl+C를 누르거나 입력이 끊겨도
        # 갑자기 꺼지지 않고, 저장한 다음 안내하고 종료해요
        # save_state()가 돌려주는 값(True/False)으로 실제 저장 결과를 알려 줘요
        saved = game.save_state()
        if saved:
            print("\n\n⚠️ 입력이 중단되어 데이터를 저장하고 안전하게 종료합니다.")
        else:
            print("\n\n⚠️ 입력이 중단되어 종료합니다. (데이터는 저장되지 못했습니다)")


# 이 파일을 직접 실행했을 때(python main.py)만 게임을 시작하라는 뜻
if __name__ == "__main__":
    main()