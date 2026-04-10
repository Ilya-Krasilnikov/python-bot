import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
import os
from flask import Flask

# ========== ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ==========
GROUP_ID = os.environ.get('GROUP_ID')
TOKEN = os.environ.get('TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')

if not all([GROUP_ID, TOKEN, ADMIN_ID]):
    raise ValueError("Ошибка: не заданы переменные окружения GROUP_ID, TOKEN, ADMIN_ID")

GROUP_ID = int(GROUP_ID)
ADMIN_ID = int(ADMIN_ID)

# ========== ВЕБ-СЕРВЕР ДЛЯ ПОДДЕРЖАНИЯ АКТИВНОСТИ ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот для приёмной комиссии работает!", 200

# ========== КОНСТАНТЫ (ФОТО) ==========
PHOTO_OPEN_DAYS = "-237266527_457239044"
PHOTO_ADMISSION_HOURS = "-237266527_457239045"

# ========== СПЕЦИАЛЬНОСТИ ==========
specialties = {
    1: {
        "title": "Информационные системы и программирование",
        "short": "Программирование",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 3 года 10 мес (на базе 9 кл.) / 2 года 10 мес (на базе 11 кл.).\n"
                      "Бюджетных мест: 25 (9 кл.), 5 (11 кл.). Договор: 110 (9 кл.), 45 (11 кл.).\n"
                      "Изучают: программирование, инженерная графика, базы данных, web-дизайн.\n"
                      "Кем работают: техник-программист, 1С-программист, web-программист, администратор БД, системный администратор, инженер по информбезопасности, SEO-специалист."),
        "photo_id": "-237266527_457239046"
    },
    2: {
        "title": "Экономика и бухгалтерский учёт",
        "short": "Экономика и бухучёт",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 2 года 10 мес (9 кл.) / 1 год 10 мес (11 кл.).\n"
                      "Бюджетных мест: 15 (9 кл.), 10 (11 кл.). Договор: 85 (9 кл.), 40 (11 кл.).\n"
                      "Изучают: бухучет, расчеты с бюджетом, составление отчетности, бизнес-планирование, инвентаризацию.\n"
                      "Кем работают: бухгалтер, экономист, финансовый аналитик, налоговый эксперт, аудитор, кадровик."),
        "photo_id": "-237266527_457239047"
    },
    3: {
        "title": "Страховое дело",
        "short": "Страховое дело",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 2 года 10 мес (9 кл.) / 1 год 10 мес (11 кл.).\n"
                      "Всего мест: 25 на договоре (9 кл.), 25 на договоре (11 кл.).\n"
                      "Изучают: экономика страхования, прямые и посреднические продажи, интернет-продажи, аудит страховых организаций, налогообложение.\n"
                      "Кем работают: страховой агент, менеджер по развитию агентских сетей, ведущий специалист по работе с клиентами, заместитель директора филиала."),
        "photo_id": "-237266527_457239048"
    },
    4: {
        "title": "Банковское дело",
        "short": "Банковское дело",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 2 года 10 мес (9 кл.) / 1 год 10 мес (11 кл.).\n"
                      "Бюджетных мест: 5 (9 кл.), 0 (11 кл.). Договор: 45 (9 кл.), 25 (11 кл.).\n"
                      "Изучают: финансы, денежное обращение и кредит, рынок ценных бумаг, депозитные операции, безналичные расчеты, финансовый анализ.\n"
                      "Кем работают: агент банка, кредитный специалист, операционист, финансовый менеджер, сотрудник бэк-офиса, ипотечный специалист."),
        "photo_id": "-237266527_457239049"
    },
    5: {
        "title": "Торговое дело",
        "short": "Торговое дело",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 2 года 10 мес (9 кл.) / 1 год 10 мес (11 кл.).\n"
                      "Бюджетных мест: 15 (9 кл.), 0 (11 кл.). Договор: 80 (9 кл.), 25 (11 кл.).\n"
                      "Изучают: маркетинг и реклама, управление подразделением, экспертиза качества товаров, документационное обеспечение, техническое оснащение.\n"
                      "Кем работают: товаровед, директор магазина, руководитель бизнеса, менеджер по продажам, мерчандайзер, торговый представитель."),
        "photo_id": "-237266527_457239050"
    },
    6: {
        "title": "Поварское и кондитерское дело",
        "short": "Поварское дело",
        "more_info": ("Поступление по конкурсу аттестатов (9 или 11 классов).\n"
                      "Срок обучения: 3 года 10 мес (9 кл.) / 2 года 10 мес (11 кл.).\n"
                      "Договорных мест: 40 (9 кл.), 25 (11 кл.).\n"
                      "Изучают: организация процесса приготовления, метрология и стандартизация, микробиология и санитария, управление подразделением, физиология питания, десерты.\n"
                      "Кем работают: повар, бренд-шеф, технолог пищевого производства, повар-кондитер, менеджер ресторана, ресторатор, бармен, food-дизайнер."),
        "photo_id": "-237266527_457239052"
    }
}

# ========== ТЕСТ (КОРОТКИЕ КНОПКИ) ==========
test_questions = [
    {"text": "Что для вас важнее в будущей работе?", "options": ["💰 Доход", "📈 Рост", "👨‍👩‍👧‍👦 Помощь", "🎨 Творчество"]},
    {"text": "Какие школьные предметы вам нравятся больше всего?", "options": ["📐 Математика", "💻 Информатика", "📖 Обществознание", "🍳 Технология"]},
    {"text": "Как вы относитесь к работе с большим объемом цифр и данных?", "options": ["😍 Обожаю", "😐 Нейтрально", "😫 С трудом", "😱 Боюсь"]},
    {"text": "Вам больше нравится?", "options": ["🧑‍💻 ПК", "🤝 Общение", "👩‍🍳 Руками", "📊 Анализ"]},
    {"text": "Какой рабочий коллектив вам ближе?", "options": ["🏢 Компания", "👨‍💼 Отдел", "🙋‍♂️ Один", "🚀 Стартап"]}
]

user_states = {}

# ========== ФУНКЦИИ ==========
def send_message(user_id, text, keyboard=None):
    vk.messages.send(user_id=user_id, message=text, random_id=random.randint(1, 2**63-1), keyboard=keyboard.get_keyboard() if keyboard else None)

def send_photo_with_text(user_id, photo_id, text, keyboard=None):
    if photo_id:
        vk.messages.send(user_id=user_id, message=text, attachment=f"photo{photo_id}", random_id=random.randint(1, 2**63-1), keyboard=keyboard.get_keyboard() if keyboard else None)
    else:
        send_message(user_id, text, keyboard)

def get_main_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button('📅 Дни открытых дверей', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🕒 Работа приёмной комиссии', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('📚 Наши специальности (СПО)', color=VkKeyboardColor.POSITIVE)
    kb.add_button('❓ Помощь', color=VkKeyboardColor.SECONDARY)
    return kb

def get_specialties_keyboard():
    kb = VkKeyboard(one_time=True)
    for spec in specialties.values():
        kb.add_button(spec['short'], color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.NEGATIVE)
    return kb

def get_spec_actions_keyboard(spec_id):
    kb = VkKeyboard(one_time=True)
    kb.add_button('📝 Пройти тест', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 Назад к специальностям', color=VkKeyboardColor.SECONDARY)
    return kb

def start_test(user_id):
    user_states[user_id] = {"step": 0, "answers": []}
    send_next_question(user_id)

def send_next_question(user_id):
    state = user_states.get(user_id)
    if not state or "step" not in state:
        return
    step = state["step"]
    if step < len(test_questions):
        q = test_questions[step]
        kb = VkKeyboard(one_time=True)
        for opt in q["options"]:
            kb.add_button(opt, color=VkKeyboardColor.SECONDARY)
        send_message(user_id, q["text"], kb)
        state["step"] += 1
    else:
        answers = state["answers"]
        if any("💻 Информатика" in a for a in answers):
            result = "Рекомендуем: Информационные системы и программирование."
        elif any("🍳 Технология" in a for a in answers):
            result = "Рекомендуем: Поварское и кондитерское дело."
        elif any("📐 Математика" in a or "📊 Анализ" in a for a in answers):
            result = "Обратите внимание на Экономику, Банковское дело или Страховое дело."
        else:
            result = "Все наши специальности могут вас заинтересовать. Приходите на День открытых дверей!"
        send_message(user_id, f"🎉 Тест завершён!\n\n{result}", get_main_keyboard())
        del user_states[user_id]

# ========== ПОДКЛЮЧЕНИЕ К VK ==========
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# ========== ЗАПУСК ВЕБ-СЕРВЕРА В ОТДЕЛЬНОМ ПОТОКЕ ==========
import threading
def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

web_thread = threading.Thread(target=run_web)
web_thread.start()

print("Бот запущен и работает 24/7...")

# ========== ОСНОВНОЙ ЦИКЛ ==========
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
        user_id = event.message.peer_id
        msg = event.message.text.strip()

        if user_id in user_states and "step" in user_states[user_id]:
            state = user_states[user_id]
            state["answers"].append(msg)
            send_next_question(user_id)
            continue

        if user_states.get(user_id) == "waiting_question":
            vk.messages.send(user_id=ADMIN_ID, message=f"Вопрос от [id{user_id}|]:\n{msg}", random_id=random.randint(1, 2**63-1))
            send_message(user_id, "Вопрос передан администратору.", get_main_keyboard())
            del user_states[user_id]
            continue

        if msg == "📅 Дни открытых дверей":
            text = ("🗓️ Дни открытых дверей в Пермском институте РЭУ им. Г.В. Плеханова\n\n"
                    "📍 Адрес: 614070, г. Пермь, бульвар Гагарина, д. 57\n"
                    "📅 Ближайшая дата: 27 апреля 2025 г., начало в 11:00\n\n"
                    "Программа:\n"
                    "• Встреча с директором института\n"
                    "• Презентация специальностей СПО\n"
                    "• Экскурсия по учебным корпусам и лабораториям\n"
                    "• Ответы на вопросы приёмной комиссии\n\n"
                    "❗ Регистрация: https://forms.yandex.ru/u/67d141a7e010db67db64bc4b/\n\n"
                    "📞 Телефон единой справочной службы: 8-800-200-08-36")
            send_photo_with_text(user_id, PHOTO_OPEN_DAYS, text, get_main_keyboard())

        elif msg == "🕒 Работа приёмной комиссии":
            text = ("🕒 График работы приёмной комиссии Пермского филиала\n\n"
                    "📅 с 20 июня по 25 августа 2025 г.:\n"
                    "• Пн-пт: 09:00 – 18:00\n"
                    "• Сб: 10:00 – 14:00\n"
                    "• Вс: выходной\n\n"
                    "📞 Телефон единой справочной службы: 8-800-200-08-36\n"
                    "📞 Телефон приёмной директора: +7 (342) 282-57-45\n"
                    "✉️ E-mail: perm@rea.ru\n"
                    "🌐 Сайт: https://www.rea.perm.ru")
            send_photo_with_text(user_id, PHOTO_ADMISSION_HOURS, text, get_main_keyboard())

        elif msg == "📚 Наши специальности (СПО)":
            send_message(user_id, "Выберите специальность:", get_specialties_keyboard())

        elif msg == "❓ Помощь":
            send_message(user_id, "Напишите ваш вопрос, я передам администратору.")
            user_states[user_id] = "waiting_question"

        elif msg == "🔙 Назад":
            send_message(user_id, "Главное меню:", get_main_keyboard())

        elif msg == "🔙 Назад к специальностям":
            send_message(user_id, "Выберите специальность:", get_specialties_keyboard())

        elif any(msg == spec['short'] for spec in specialties.values()):
            spec = next(spec for spec in specialties.values() if spec['short'] == msg)
            spec_id = next(i for i, s in specialties.items() if s['short'] == msg)
            user_states[user_id] = {"selected_spec": spec_id}
            text = f"📌 {spec['title']}\n\n{spec['more_info']}"
            send_photo_with_text(user_id, spec['photo_id'], text, get_spec_actions_keyboard(spec_id))

        elif msg == "📝 Пройти тест":
            start_test(user_id)

        else:
            send_message(user_id, "Добро пожаловать! Я бот приёмной комиссии Пермского института РЭУ. Выберите действие:", get_main_keyboard())