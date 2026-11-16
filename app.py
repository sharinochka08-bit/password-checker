import streamlit as st
import math
from zxcvbn import zxcvbn
import secrets
import string

def calculate_entropy(password):
    pool = 0

    if any(c.islower() for c in password):
        pool += 26

    if any(c.isupper() for c in password):
        pool += 26

    if any(c.isdigit() for c in password):
        pool += 10

    if any(not c.isalnum() for c in password):
        pool += 33

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase

    if use_lower:
        characters += string.ascii_lowercase

    if use_digits:
        characters += string.digits

    if use_symbols:
        characters += "!@#$%^&*()-_=+"

    if not characters:
        return ""

    required = []

    if use_upper:
        required.append(secrets.choice(string.ascii_uppercase))

    if use_lower:
        required.append(secrets.choice(string.ascii_lowercase))

    if use_digits:
        required.append(secrets.choice(string.digits))

    if use_symbols:
        required.append(secrets.choice("!@#$%^&*()-_=+"))

    remaining = [
        secrets.choice(characters)
        for _ in range(length - len(required))
    ]

    password_chars = required + remaining
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)



st.set_page_config(
    page_title="Password Checker",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #102744);
    color: #ffffff;
}

h1, h2, h3, p, label {
    color: #ffffff !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #42e8d5;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #b5c8dc;
    font-size: 17px;
    margin-bottom: 30px;
}

.info-card {
    background: #142d49;
    border: 1px solid #285273;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}

.result-title {
    text-align: center;
    font-size: 27px;
    font-weight: bold;
}

.small-text {
    color: #b5c8dc;
    font-size: 14px;
}

div.stButton > button {
    background: #16b9ad;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown(
    '<div class="main-title">🔐 PASSWORD CHECKER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Умная проверка надёжности паролей</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
    <h3>🛡️ Защитите свои аккаунты</h3>
    <p class="small-text">
    Проверьте сложность пароля и получите рекомендации
    по повышению безопасности.
    </p>
</div>
""", unsafe_allow_html=True)

# Поле ввода
password = st.text_input(
    "🔑 Введите тестовый пароль",
    type="password",
    placeholder="Введите пароль здесь..."
)

if password:
    result = zxcvbn(password)
    score = result["score"]

    levels = {
        0: "Очень слабый",
        1: "Слабый",
        2: "Средний",
        3: "Сильный",
        4: "Очень сильный"
    }

    colors = {
        0: "#ef4444",
        1: "#f97316",
        2: "#eab308",
        3: "#22c55e",
        4: "#14b8a6"
    }

    color = colors[score]

    st.markdown("---")
    st.markdown(
        '<div class="result-title">📊 Результат проверки</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="info-card" style="text-align:center;">'
        f'<div class="small-text">Уровень надёжности</div>'
        f'<div style="font-size:30px;font-weight:bold;color:{color};">'
        f'{levels[score]}</div>'
        f'<div class="small-text">Оценка: {score} из 4</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Индикатор надёжности
    st.progress(score / 4)

    st.markdown("### 📋 Характеристики пароля")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Длина", f"{len(password)} символов")
        st.metric(
            "Заглавные буквы",
            "Есть" if any(c.isupper() for c in password) else "Нет"
        )
        st.metric(
            "Строчные буквы",
            "Есть" if any(c.islower() for c in password) else "Нет"
        )

    with col2:
        st.metric(
            "Цифры",
            "Есть" if any(c.isdigit() for c in password) else "Нет"
        )
        st.metric(
            "Спецсимволы",
            "Есть" if any(not c.isalnum() for c in password) else "Нет"
        )
        st.metric("Оценка", f"{score}/4")

    # Предупреждения
    warning = result["feedback"]["warning"]

    if warning:
        st.warning(warning)

    suggestions = result["feedback"]["suggestions"]

    st.markdown("### 💡 Рекомендации")

    if suggestions:
        for suggestion in suggestions:
            st.info("• " + suggestion)
    else:
        st.success("Специальных рекомендаций нет. Продолжайте использовать уникальные пароли!")

    if len(password) < 12:
        st.info("Попробуйте использовать более длинный пароль.")

    st.caption(
        "Оценка приблизительная. Не вводите настоящие пароли."
    )

else:
    st.markdown("""
    <div class="info-card">
        <h3>✨ Возможности приложения</h3>
        <p>✔ Анализ сложности пароля</p>
        <p>✔ Проверка длины и состава</p>
        <p>✔ Поиск распространённых шаблонов</p>
        <p>✔ Рекомендации по безопасности</p>
    </div>
    """, unsafe_allow_html=True)

# Подвал
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#9bb5ca;">'
    'PASSWORD CHECKER | Учебный проект по кибербезопасности'
    '</p>',
    unsafe_allow_html=True
)
# Генератор надёжных паролей
st.markdown("---")
st.header("🔑 Генератор надёжных паролей")

st.write("Создайте случайный пароль с выбранными параметрами.")

length = st.slider(
    "Длина пароля:",
    min_value=8,
    max_value=32,
    value=16
)

st.write("Выберите символы для генерации:")

use_upper = st.checkbox("Заглавные буквы (A-Z)", value=True)
use_lower = st.checkbox("Строчные буквы (a-z)", value=True)
use_digits = st.checkbox("Цифры (0-9)", value=True)
use_symbols = st.checkbox("Специальные символы (!@#$)", value=True)

if st.button("🎲 Сгенерировать пароль"):
    if not any([use_upper, use_lower, use_digits, use_symbols]):
        st.error("Выберите хотя бы одну группу символов.")

    elif length < sum([use_upper, use_lower, use_digits, use_symbols]):
        st.error("Увеличьте длину пароля для выбранных групп.")

    else:
        generated = generate_password(
            length,
            use_upper,
            use_lower,
            use_digits,
            use_symbols
        )

        st.session_state.generated_password = generated

if "generated_password" in st.session_state:
    generated_password = st.session_state.generated_password

    st.success("Ваш новый пароль:")
    st.code(generated_password)

    # Автоматическая проверка надёжности
    result = zxcvbn(generated_password)

    st.subheader("📊 Результат проверки")

    score = result["score"]

    st.progress((score + 1) / 5)

    if score <= 1:
        st.error("Низкая надёжность")
    elif score == 2:
        st.warning("Средняя надёжность")
    elif score == 3:
        st.info("Хорошая надёжность")
    else:
        st.success("Отличная надёжность! 🔒")

    st.write(f"Оценка: {score} из 4")
    st.write(f"Энтропия: {calculate_entropy(generated_password):.2f} бит")