import streamlit as st
import json
import os

# =========================================================
# БЕТ БАПТАУЛАРЫ
# =========================================================

st.set_page_config(
    page_title="Ақылды дос",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ДЕРЕКТЕР ФАЙЛЫ
# =========================================================

DATA_FILE = "students.json"


def load_students():
    """Оқушылар нәтижесін жүктеу"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except Exception:
            return {}

    return {}


def save_students(data):
    """Оқушылар нәтижесін сақтау"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


students = load_students()

# =========================================================
# SESSION STATE
# =========================================================

if "name" not in st.session_state:
    st.session_state.name = ""

if "game_score" not in st.session_state:
    st.session_state.game_score = 0

if "game_index" not in st.session_state:
    st.session_state.game_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_checked" not in st.session_state:
    st.session_state.quiz_checked = False

if "student_logged" not in st.session_state:
    st.session_state.student_logged = False

# =========================================================
# ӘДЕМІ ДИЗАЙН
# =========================================================

st.markdown(
    """
<style>

/* =========================
   НЕГІЗГІ ФОН
========================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #ffffff 0%, transparent 20%),
        radial-gradient(circle at 90% 20%, #fff3e0 0%, transparent 22%),
        radial-gradient(circle at 20% 90%, #e8f5e9 0%, transparent 25%),
        linear-gradient(135deg, #e3f2fd, #f3e5f5, #e8f5e9);
}

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e3f2fd 0%,
        #f3e5f5 50%,
        #e8f5e9 100%
    );
}

[data-testid="stSidebar"] h2 {
    color: #1565c0 !important;
}

/* =========================
   ТАҚЫРЫПТАР
========================= */

h1 {
    color: #1565c0 !important;
    font-weight: 900 !important;
}

h2 {
    color: #1976d2 !important;
    font-weight: 800 !important;
}

h3 {
    color: #0d47a1 !important;
    font-weight: 750 !important;
}

p {
    color: #24445f;
}

/* =========================
   ОҚУШЫ АТЫ
========================= */

.stTextInput label {
    color: #0d47a1 !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}

.stTextInput input {
    color: #0d47a1 !important;
    background: white !important;
    border: 3px solid #64b5f6 !important;
    border-radius: 15px !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    padding: 13px !important;
}

.stTextInput input:focus {
    border: 3px solid #1976d2 !important;
    box-shadow: 0 0 10px rgba(33,150,243,0.25) !important;
}

.stTextInput input::placeholder {
    color: #90a4ae !important;
    font-size: 17px !important;
}

/* =========================
   HERO
========================= */

.hero {
    background:
        linear-gradient(
            135deg,
            #1976d2,
            #42a5f5,
            #7e57c2
        );
    padding: 40px 30px;
    border-radius: 30px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(21,101,192,0.25);
}

.hero h1 {
    color: white !important;
    font-size: 46px !important;
    margin-bottom: 10px;
}

.hero h2 {
    color: white !important;
    font-size: 32px !important;
}

.hero p {
    color: white !important;
    font-size: 21px !important;
}

/* =========================
   КАРТОЧКАЛАР
========================= */

.card {
    background: rgba(255,255,255,0.92);
    padding: 25px;
    border-radius: 22px;
    margin: 15px 0;
    box-shadow: 0 7px 20px rgba(0,0,0,0.08);
    border-left: 7px solid #42a5f5;
}

.rule {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 20px;
    margin: 14px 0;
    font-size: 19px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.07);
}

/* =========================
   ОЙЫН / СҰРАҚ
========================= */

.question {
    background: rgba(255,255,255,0.95);
    padding: 28px;
    border-radius: 25px;
    margin: 20px 0;
    box-shadow: 0 7px 20px rgba(0,0,0,0.08);
    border: 2px solid #bbdefb;
}

/* =========================
   НӘТИЖЕ
========================= */

.result {
    background:
        linear-gradient(
            135deg,
            #bbdefb,
            #e1f5fe,
            #e8eaf6
        );
    padding: 35px;
    border-radius: 28px;
    text-align: center;
    margin: 25px 0;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
}

.result h1 {
    font-size: 52px !important;
}

/* =========================
   РЕЙТИНГ КАРТОЧКАСЫ
========================= */

.rank-card {
    background: white;
    padding: 18px 22px;
    border-radius: 18px;
    margin: 10px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    font-size: 19px;
    font-weight: 700;
}

.rank-first {
    border-left: 8px solid #ffd700;
    background: linear-gradient(90deg, #fffde7, white);
}

.rank-second {
    border-left: 8px solid #b0bec5;
    background: linear-gradient(90deg, #eceff1, white);
}

.rank-third {
    border-left: 8px solid #cd7f32;
    background: linear-gradient(90deg, #fff3e0, white);
}

/* =========================
   FOOTER
========================= */

.footer {
    text-align: center;
    padding: 35px;
    margin-top: 45px;
    color: #1565c0;
    font-size: 16px;
    font-weight: 600;
}

/* =========================
   БАТЫРМАЛАР
========================= */

.stButton > button {
    border-radius: 15px !important;
    font-size: 17px !important;
    font-weight: 750 !important;
    min-height: 48px !important;
}

/* =========================
   METRIC
========================= */

[data-testid="stMetricValue"] {
    color: #1565c0 !important;
    font-weight: 900 !important;
}

/* =========================
   ЖҰМСАҚ АНИМАЦИЯ
========================= */

@keyframes float {
    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-7px);
    }

    100% {
        transform: translateY(0px);
    }
}

.robot {
    font-size: 70px;
    animation: float 3s ease-in-out infinite;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <div class="robot">🤖</div>
            <h2>Ақылды дос</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 👧 Оқушының аты-жөні")

    student_name = st.text_input(
        "Оқушының аты-жөні:",
        value=st.session_state.name,
        placeholder="Мысалы: Айдана Нұрланқызы",
        label_visibility="collapsed"
    )

    student_name = student_name.strip()

    if student_name:
        st.session_state.name = student_name
        st.session_state.student_logged = True

        st.success(
            f"👋 Сәлем, {student_name}!"
        )

    st.markdown("---")

    st.markdown("### 📚 Бөлімдер")

    page = st.radio(
        "Бөлімді таңда:",
        [
            "🏠 Басты бет",
            "🔐 Қауіпсіздік ережелері",
            "🎮 Қауіп пе, қауіпсіз бе?",
            "🧠 Тест",
            "🤖 Ақылды көмекші",
            "🏆 Менің нәтижем",
            "📊 Оқушылар рейтингі"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.info(
        "💡 Есіңде болсын:\n\n"
        "Интернетті қауіпсіз қолдан!"
    )

# =========================================================
# БАСТЫ БЕТ
# =========================================================

if page == "🏠 Басты бет":

    st.markdown(
        """
        <div class="hero">
            <div class="robot">🤖</div>
            <h1>«Ақылды дос»</h1>
            <p>Қауіпсіз интернетті бірге үйренейік!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.name:

        st.success(
            f"🌟 Сәлем, {st.session_state.name}! "
            f"Сенің Ақылды досың дайын!"
        )

    else:

        st.warning(
            "👈 Алдымен сол жақтағы «Оқушының аты-жөні» "
            "жеріне өз атыңды жаз."
        )

    st.markdown("## 🌈 Ақылды дос деген не?")

    st.markdown(
        """
        <div class="card">
        🤖 <b>Ақылды дос</b> — бастауыш сынып оқушыларына
        интернетті қауіпсіз қолдануды үйрететін
        қызықты оқу сайты.
        <br><br>
        Мұнда сен:
        <br>🔐 қауіпсіздік ережелерін үйренесің;
        <br>🎮 ойын ойнайсың;
        <br>🧠 тест тапсырасың;
        <br>🤖 Ақылды көмекшімен сөйлесесің;
        <br>🏆 өз нәтижеңді көресің;
        <br>📊 достарыңмен рейтингте жарысасың.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## ⭐ Біздің ұранымыз")

    st.markdown(
        """
        <div class="hero">
            <h2>
            🤖 Ақылды дос – қауіпсіз интернетке
            бастайтын көмекші!
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card" style="text-align:center;">
                <div style="font-size:45px;">🔐</div>
                <h3>Қауіпсіздік</h3>
                <p>Интернетте өзіңді қорғауды үйрен.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card" style="text-align:center;">
                <div style="font-size:45px;">🎮</div>
                <h3>Ойын</h3>
                <p>Қауіп пен қауіпсізді ажырат.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card" style="text-align:center;">
                <div style="font-size:45px;">🏆</div>
                <h3>Жетістік</h3>
                <p>Ұпай жинап, рейтингке көтеріл.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# ҚАУІПСІЗДІК ЕРЕЖЕЛЕРІ
# =========================================================

elif page == "🔐 Қауіпсіздік ережелері":

    st.markdown("## 🔐 Интернеттегі қауіпсіздік ережелері")

    st.write(
        "Интернет қызықты әлем. Бірақ әрқашан қауіпсіздік ережесін сақтау керек!"
    )

    rules = [
        (
            "🔑",
            "Құпиясөзіңді ешкімге айтпа!",
            "Құпиясөз — сенің жеке құпияң."
        ),
        (
            "👤",
            "Бейтаныс адамдармен сөйлеспе!",
            "Интернеттегі бейтаныс адамға сенбе."
        ),
        (
            "🔗",
            "Күмәнді сілтемені ашпа!",
            "Бейтаныс сілтемелер қауіпті болуы мүмкін."
        ),
        (
            "📷",
            "Жеке суретіңді жіберме!",
            "Сурет, мекенжай, телефон сияқты ақпаратты берме."
        ),
        (
            "🆘",
            "Қауіп болса, үлкен адамға айт!",
            "Ата-анаңа немесе мұғаліміңе бірден хабарла."
        )
    ]

    for icon, title, text in rules:

        st.markdown(
            f"""
            <div class="rule">
                <span style="font-size:30px;">{icon}</span>
                <b>{title}</b>
                <br><br>
                👉 {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success(
        "🌟 Ең басты ереже: күмәнді жағдай болса, "
        "үлкен адамнан көмек сұра!"
    )

# =========================================================
# ОЙЫН
# =========================================================

elif page == "🎮 Қауіп пе, қауіпсіз бе?":

    st.markdown("## 🎮 Қауіп пе, қауіпсіз бе?")

    if not st.session_state.name:

        st.warning(
            "👈 Ойынды бастау үшін алдымен "
            "оқушының аты-жөнін енгіз."
        )

    else:

        st.write(
            f"🌟 {st.session_state.name}, жағдайды оқып, дұрыс жауапты таңда!"
        )

        game_questions = [
            {
                "text": "👤 Бейтаныс адам сенен үйіңнің мекенжайын сұрады.",
                "answer": "Қауіпті"
            },
            {
                "text": "👨‍👩‍👧 Ата-анаңмен бірге балаларға арналған видео көрдің.",
                "answer": "Қауіпсіз"
            },
            {
                "text": "🔑 Бір адам сенен құпиясөзіңді сұрады.",
                "answer": "Қауіпті"
            },
            {
                "text": "👩‍🏫 Мұғалім берген қауіпсіз сайтқа кірдің.",
                "answer": "Қауіпсіз"
            },
            {
                "text": "🔗 Бейтаныс адам күмәнді сілтеме жіберді.",
                "answer": "Қауіпті"
            }
        ]

        index = st.session_state.game_index

        if index < len(game_questions):

            q = game_questions[index]

            st.markdown(
                f"""
                <div class="question">
                    <h3>🌟 Жағдай {index + 1} / 5</h3>
                    <p style="font-size:23px;">
                        {q["text"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🔴 ҚАУІПТІ",
                    use_container_width=True
                ):

                    if q["answer"] == "Қауіпті":

                        st.session_state.game_score += 1
                        st.success("🎉 Дұрыс жауап!")

                    else:

                        st.error(
                            "❌ Қате. Бұл жағдай қауіпсіз."
                        )

                    st.session_state.game_index += 1
                    st.rerun()

            with col2:

                if st.button(
                    "🟢 ҚАУІПСІЗ",
                    use_container_width=True
                ):

                    if q["answer"] == "Қауіпсіз":

                        st.session_state.game_score += 1
                        st.success("🎉 Дұрыс жауап!")

                    else:

                        st.error(
                            "❌ Қате. Бұл жағдай қауіпті."
                        )

                    st.session_state.game_index += 1
                    st.rerun()

        else:

            score = st.session_state.game_score

            st.markdown(
                f"""
                <div class="result">
                    <div style="font-size:55px;">🎉🏆🎉</div>
                    <h2>Ойын аяқталды!</h2>
                    <h1>{score} / 5</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            if score == 5:

                st.balloons()

                st.success(
                    "🌟 Керемет! Сен интернет қауіпсіздігін "
                    "өте жақсы білесің!"
                )

            elif score >= 3:

                st.success(
                    "👏 Жақсы нәтиже! Тағы да жаттығып көр!"
                )

            else:

                st.info(
                    "💪 Қауіпсіздік ережелерін қайта оқып көр!"
                )

            if st.button("💾 Нәтижені сақтау"):

                total_score = (
                    st.session_state.game_score +
                    st.session_state.quiz_score
                )

                old_score = students.get(
                    st.session_state.name,
                    {}
                ).get("total", -1)

                if total_score >= old_score:

                    students[st.session_state.name] = {
                        "game": st.session_state.game_score,
                        "quiz": st.session_state.quiz_score,
                        "total": total_score
                    }

                    save_students(students)

                    st.success(
                        "🏆 Нәтиже сақталды! "
                        "Енді рейтингтен көре аласың."
                    )

                else:

                    st.info(
                        "Бұл нәтижеден жоғары ұпайың бұрын сақталған."
                    )

            if st.button("🔄 Ойынды қайта бастау"):

                st.session_state.game_index = 0
                st.session_state.game_score = 0

                st.rerun()

# =========================================================
# ТЕСТ
# =========================================================

elif page == "🧠 Тест":

    st.markdown("## 🧠 Қауіпсіз интернет тесті")

    if not st.session_state.name:

        st.warning(
            "👈 Тест бастау үшін алдымен "
            "оқушының аты-жөнін енгіз."
        )

    else:

        st.write(
            f"🧠 {st.session_state.name}, "
            "әр сұраққа дұрыс жауапты таңда."
        )

        quiz_questions = [
            {
                "q": "1. Құпиясөзді кімге айтуға болады?",
                "options": [
                    "Бейтаныс адамға",
                    "Досыма",
                    "Ешкімге айтпау керек"
                ],
                "answer": "Ешкімге айтпау керек"
            },
            {
                "q": "2. Бейтаныс адам жазса не істеу керек?",
                "options": [
                    "Онымен сөйлесу",
                    "Үлкен адамға айту",
                    "Оған мекенжайымды жіберу"
                ],
                "answer": "Үлкен адамға айту"
            },
            {
                "q": "3. Күмәнді сілтеме келсе не істейміз?",
                "options": [
                    "Бірден ашамыз",
                    "Досымызға жібереміз",
                    "Ашпаймыз және үлкен адамға айтамыз"
                ],
                "answer": "Ашпаймыз және үлкен адамға айтамыз"
            },
            {
                "q": "4. Интернетте жеке ақпаратқа не жатады?",
                "options": [
                    "Мекенжай және телефон",
                    "Сүйікті түсім",
                    "Менің сүйікті ойыным"
                ],
                "answer": "Мекенжай және телефон"
            },
            {
                "q": "5. Интернетте қорқынышты жағдай болса не істейміз?",
                "options": [
                    "Жасырамыз",
                    "Ата-анаға немесе мұғалімге айтамыз",
                    "Тағы жалғастырамыз"
                ],
                "answer": "Ата-анаға немесе мұғалімге айтамыз"
            }
        ]

        answers = []

        for item in quiz_questions:

            st.markdown(
                f"""
                <div class="question">
                    <b style="font-size:20px;">
                        {item["q"]}
                    </b>
                </div>
                """,
                unsafe_allow_html=True
            )

            answer = st.radio(
                "Жауабы:",
                item["options"],
                key=item["q"]
            )

            answers.append(answer)

        if st.button(
            "✅ Тестті тексеру",
            use_container_width=True
        ):

            score = 0

            for i in range(len(quiz_questions)):

                if answers[i] == quiz_questions[i]["answer"]:

                    score += 1

            st.session_state.quiz_score = score
            st.session_state.quiz_checked = True

            total_score = (
                st.session_state.game_score +
                score
            )

            old_score = students.get(
                st.session_state.name,
                {}
            ).get("total", -1)

            if total_score >= old_score:

                students[st.session_state.name] = {
                    "game": st.session_state.game_score,
                    "quiz": score,
                    "total": total_score
                }

                save_students(students)

        if st.session_state.quiz_checked:

            score = st.session_state.quiz_score

            st.markdown(
                f"""
                <div class="result">
                    <div style="font-size:55px;">🧠⭐</div>
                    <h2>Сенің нәтижең</h2>
                    <h1>{score} / 5</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            if score == 5:

                st.balloons()

                st.success(
                    "🏆 Өте керемет! Барлық сұраққа дұрыс жауап бердің!"
                )

            elif score >= 3:

                st.success(
                    "👏 Жақсы! Сен қауіпсіздік ережелерін білесің."
                )

            else:

                st.info(
                    "📚 Ережелерді тағы бір рет қайталап көр."
                )

            st.info(
                "💾 Нәтиже автоматты түрде сақталды."
            )

# =========================================================
# АҚЫЛДЫ КӨМЕКШІ
# =========================================================

elif page == "🤖 Ақылды көмекші":

    st.markdown("## 🤖 Ақылды көмекші")

    st.markdown(
        """
        <div class="hero">
            <div class="robot">🤖</div>
            <h2>Сәлем! Мен — Ақылды көмекшімін!</h2>
            <p>Интернет қауіпсіздігі туралы сұрақ қой!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🔑 Құпиясөзімді айтуға бола ма?")

    with col2:
        st.info("👤 Бейтаныс адам жазса не істеймін?")

    with col3:
        st.info("🔗 Сілтемені ашуға бола ма?")

    question = st.text_input(
        "💬 Сұрағыңды жаз:",
        placeholder="Мысалы: Құпиясөзімді айтуға бола ма?"
    )

    if st.button(
        "🤖 Жауап алу",
        use_container_width=True
    ):

        q = question.lower()

        if "құпиясөз" in q or "пароль" in q:

            answer = """
🔐 Құпиясөзіңді ешкімге айтпа!

Құпиясөз — сенің жеке құпияң.

Егер біреу сұраса,
ата-анаңа немесе мұғаліміңе айт.
"""

        elif "бейтаныс" in q or "танымай" in q:

            answer = """
👤 Бейтаныс адаммен сөйлеспе!

Оған өзің туралы ақпарат берме.

Қажет болса, ата-анаңа немесе
мұғаліміңе айт.
"""

        elif "сілтеме" in q or "ссылка" in q:

            answer = """
🔗 Күмәнді сілтемені ашпа!

Бейтаныс адам жіберген сілтемені
ашпас бұрын үлкен адамнан сұра.
"""

        elif "сурет" in q or "фото" in q:

            answer = """
📷 Жеке суреттеріңді бейтаныс адамға жіберме!

Егер біреу сұраса,
ата-анаңа немесе мұғаліміңе айт.
"""

        elif "мекенжай" in q or "телефон" in q:

            answer = """
🏠 Мекенжайыңды және телефон нөміріңді
интернеттегі бейтаныс адамдарға берме!

Бұл — жеке ақпарат.
"""

        elif "қорқы" in q or "қауіп" in q:

            answer = """
🆘 Егер интернетте бір нәрсе сені қорқытса:

1️⃣ Сайттан шық.
2️⃣ Жауап берме.
3️⃣ Ата-анаңа немесе мұғаліміңе айт.
"""

        else:

            answer = """
🤖 Мен бұл сұрақты толық түсінбедім.

Мына тақырыптардың бірін сұрап көр:

🔑 Құпиясөз
👤 Бейтаныс адам
🔗 Сілтеме
📷 Сурет
🏠 Мекенжай
🆘 Қауіп
"""

        st.markdown(
            f"""
            <div class="card">
                <h3>🤖 Ақылды досының жауабы:</h3>
                <p style="font-size:19px;
                          white-space:pre-line;">
                    {answer}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.info(
        "💡 Ақылды көмекші балаларға интернет қауіпсіздігі "
        "ережелерін түсіндіруге арналған."
    )

# =========================================================
# МЕНІҢ НӘТИЖЕМ
# =========================================================

elif page == "🏆 Менің нәтижем":

    st.markdown("## 🏆 Менің нәтижем")

    if not st.session_state.name:

        st.warning(
            "👈 Нәтижеңді көру үшін "
            "алдымен аты-жөніңді енгіз."
        )

    else:

        name = st.session_state.name

        current_data = students.get(
            name,
            {
                "game": st.session_state.game_score,
                "quiz": st.session_state.quiz_score,
                "total": (
                    st.session_state.game_score +
                    st.session_state.quiz_score
                )
            }
        )

        game = current_data.get("game", 0)
        quiz = current_data.get("quiz", 0)
        total = current_data.get("total", game + quiz)

        st.markdown(
            f"""
            <div class="hero">
                <div class="robot">🌟</div>
                <h2>{name}</h2>
                <p>Сенің нәтижелерің</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🎮 Ойын ұпайы",
                f"{game} / 5"
            )

        with col2:

            st.metric(
                "🧠 Тест ұпайы",
                f"{quiz} / 5"
            )

        st.markdown(
            f"""
            <div class="result">
                <div style="font-size:50px;">⭐</div>
                <h2>Жалпы нәтиже</h2>
                <h1>{total} / 10</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        if total >= 9:

            st.balloons()

            st.success(
                "🏆 Керемет! Сен интернет қауіпсіздігін "
                "өте жақсы білесің!"
            )

        elif total >= 6:

            st.success(
                "👏 Жақсы нәтиже! Білімінді жетілдіре бер!"
            )

        else:

            st.info(
                "💪 Қауіпсіздік ережелерін қайталап көр!"
            )

        if st.button("💾 Нәтижені рейтингке сақтау"):

            students[name] = {
                "game": game,
                "quiz": quiz,
                "total": total
            }

            save_students(students)

            st.success(
                "🏆 Нәтиже сақталды! "
                "«Оқушылар рейтингі» бөлімінен көре аласың."
            )

# =========================================================
# ОҚУШЫЛАР РЕЙТИНГІ
# =========================================================

elif page == "📊 Оқушылар рейтингі":

    st.markdown("## 📊 Оқушылар рейтингі")

    st.markdown(
        """
        <div class="hero">
            <div class="robot">🏆</div>
            <h2>Ақылды достар жарысы</h2>
            <p>Кім қауіпсіз интернетті жақсы біледі?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not students:

        st.info(
            "👧 Әзірге рейтингте оқушылар жоқ. "
            "Алдымен оқушы тест немесе ойын орындауы керек."
        )

    else:

        # Рейтингті ұпай бойынша сұрыптау
        ranking = sorted(
            students.items(),
            key=lambda x: x[1].get("total", 0),
            reverse=True
        )

        st.markdown("### 🏆 Үздік оқушылар")

        for index, (name, data) in enumerate(ranking):

            total = data.get("total", 0)

            if index == 0:

                medal = "🥇"
                css_class = "rank-first"
                place = "1-орын"

            elif index == 1:

                medal = "🥈"
                css_class = "rank-second"
                place = "2-орын"

            elif index == 2:

                medal = "🥉"
                css_class = "rank-third"
                place = "3-орын"

            else:

                medal = "⭐"
                css_class = ""
                place = f"{index + 1}-орын"

            st.markdown(
                f"""
                <div class="rank-card {css_class}">
                    <span style="font-size:28px;">
                        {medal}
                    </span>
                    &nbsp;&nbsp;
                    <b>{place}</b>
                    &nbsp;&nbsp;
                    👧 <span style="color:#0d47a1;">
                        {name}
                    </span>
                    &nbsp;&nbsp;
                    <span style="color:#1976d2;">
                        ⭐ {total} / 10
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =================================================
        # ДИАГРАММА
        # =================================================

        st.markdown("---")

        st.markdown("### 📊 Оқушылардың ұпай диаграммасы")

        chart_data = {}

        for name, data in ranking:

            chart_data[name] = data.get("total", 0)

        st.bar_chart(
            chart_data,
            height=450
        )

        st.caption(
            "📊 Диаграмма оқушылардың жалпы жинаған "
            "ұпайын көрсетеді."
        )

        # =================================================
        # КЕСТЕ
        # =================================================

        st.markdown("---")

        st.markdown("### 📋 Толық нәтиже")

        header1, header2, header3, header4 = st.columns(
            [3, 1, 1, 1]
        )

        with header1:
            st.markdown("**👧 Оқушы**")

        with header2:
            st.markdown("**🎮 Ойын**")

        with header3:
            st.markdown("**🧠 Тест**")

        with header4:
            st.markdown("**⭐ Жалпы**")

        for name, data in ranking:

            col1, col2, col3, col4 = st.columns(
                [3, 1, 1, 1]
            )

            with col1:
                st.write(f"👧 {name}")

            with col2:
                st.write(
                    f"{data.get('game', 0)} / 5"
                )

            with col3:
                st.write(
                    f"{data.get('quiz', 0)} / 5"
                )

            with col4:
                st.write(
                    f"⭐ {data.get('total', 0)} / 10"
                )

        # =================================================
        # ТАЗАЛАУ
        # =================================================

        st.markdown("---")

        st.warning(
            "⚠️ Бұл батырма барлық оқушы нәтижесін өшіреді."
        )

        if st.button(
            "🗑️ Барлық рейтингті тазалау"
        ):

            students = {}

            save_students(students)

            st.success(
                "Рейтинг тазаланды."
            )

            st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🤖 <b>«Ақылды дос»</b>
        <br><br>
        🌈 Қауіпсіз интернет • Білім • Достық
        <br><br>
        ⭐ «Ақылды дос – қауіпсіз интернетке
        бастайтын көмекші!»
    </div>
    """,
    unsafe_allow_html=True
)