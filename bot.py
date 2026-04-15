import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import os
import threading
from flask import Flask

GROUP_ID = int(os.environ.get('GROUP_ID', 237266527))
TOKEN = os.environ.get('TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 267710669))

PHOTO_OPEN_DAYS = "-237266527_457239044"
PHOTO_ADMISSION_HOURS = "-237266527_457239045"
PHOTO_WELCOME = "-237266527_457239053"

# Данные специальностей (сокращённо, полные версии есть в предыдущих кодах)
specialties_spo = {
    1: {"title": "Информационные системы и программирование", "short": "Программирование", "photo_id": "-237266527_457239046"},
    2: {"title": "Экономика и бухгалтерский учёт", "short": "Экономика и бухучёт", "photo_id": "-237266527_457239047"},
    3: {"title": "Страховое дело", "short": "Страховое дело", "photo_id": "-237266527_457239048"},
    4: {"title": "Банковское дело", "short": "Банковское дело", "photo_id": "-237266527_457239049"},
    5: {"title": "Торговое дело", "short": "Торговое дело", "photo_id": "-237266527_457239050"},
    6: {"title": "Поварское и кондитерское дело", "short": "Поварское дело", "photo_id": "-237266527_457239052"},
}
specialties_bachelor = {
    1: {"title": "Экономика", "short": "Экономика", "photo_id": "-237266527_457239062"},
    2: {"title": "Менеджмент", "short": "Менеджмент", "photo_id": "-237266527_457239061"},
    3: {"title": "Торговое дело", "short": "Торговое дело", "photo_id": "-237266527_457239060"},
    4: {"title": "Прикладная информатика", "short": "Прикладная информатика", "photo_id": "-237266527_457239059"},
    5: {"title": "Товароведение", "short": "Товароведение", "photo_id": "-237266527_457239058"},
    6: {"title": "Технология питания", "short": "Технология питания", "photo_id": "-237266527_457239057"},
}

# Описания (полные версии, вставьте свои)
for k in specialties_spo:
    specialties_spo[k]["more_info"] = "Подробное описание специальности СПО..."
for k in specialties_bachelor:
    specialties_bachelor[k]["more_info"] = "Подробное описание направления бакалавриата..."

# Тесты (4 варианта, короткие, с эмодзи)
test_spo = [
    ("💻 Какая сфера вам ближе?", ["💻 Программирование и IT", "💰 Экономика и финансы", "🍳 Ресторанный бизнес", "🛒 Торговля и продажи"]),
    ("🧑‍💻 Что вас привлекает в работе?", ["🧑‍💻 Создавать программы", "📊 Анализировать данные", "🍝 Готовить блюда", "🤝 Общаться с людьми"]),
    ("🔧 Какую задачу вы решите лучше?", ["🖥️ Написать код", "📈 Составить бизнес-план", "🍽️ Организовать кухню", "💬 Провести переговоры"]),
    ("🏢 Ваше идеальное место работы?", ["🏢 IT-компания", "🏦 Банк", "🍽️ Ресторан", "🛍️ Магазин"]),
    ("🚀 Какой бизнес вы бы открыли?", ["🚀 Разработка приложений", "💸 Финансовые услуги", "🍕 Кафе", "📦 Интернет-магазин"]),
]
test_bachelor = [
    ("💼 Какое направление перспективно?", ["💻 Информационные технологии", "👔 Управление", "💰 Финансы", "🛒 Маркетинг"]),
    ("👥 В какой роли вы видите себя?", ["⚙️ Технический эксперт", "👥 Руководитель", "📊 Аналитик", "🤝 Переговорщик"]),
    ("🔧 Какая задача интереснее?", ["🔧 Техническая", "🗣️ Стратегическая", "📉 Финансовая", "💡 Креативная"]),
    ("🏢 Какая культура вам ближе?", ["🧑‍💻 IT-команда", "👔 Иерархия", "📊 Работа с данными", "🎯 Клиентоориентированность"]),
    ("🎯 Что важнее в работе?", ["🚀 Интересные задачи", "💼 Высокий доход", "🏦 Стабильность", "🎨 Творчество"]),
]

user_states = {}  # user_id: {"menu": str, "level": str, "test": dict}

# Flask для healthcheck
app = Flask(__name__)
@app.route('/')
def healthcheck():
    return "OK", 200
def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
threading.Thread(target=run_web, daemon=True).start()

# VK API
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

def send(user_id, text, keyboard=None):
    vk.messages.send(user_id=user_id, message=text, random_id=random.randint(1, 2**63-1), keyboard=keyboard.get_keyboard() if keyboard else None)

def send_photo(user_id, photo_id, text, keyboard=None):
    vk.messages.send(user_id=user_id, message=text, attachment=f"photo{photo_id}", random_id=random.randint(1, 2**63-1), keyboard=keyboard.get_keyboard() if keyboard else None)

def make_keyboard(buttons, one_time=True):
    kb = VkKeyboard(one_time=one_time)
    for i, btn in enumerate(buttons):
        kb.add_button(btn, color=VkKeyboardColor.SECONDARY)
        if i != len(buttons)-1:
            kb.add_line()
    return kb

# Главное меню
main_buttons = ['📅 Дни открытых дверей', '🕒 Работа приёмной комиссии', '🎓 Специальности', '❓ Помощь']
main_kb = make_keyboard(main_buttons, one_time=False)

# Меню выбора уровня
level_buttons = ['📚 СПО (9-11)', '🎓 Бакалавриат', '📖 Магистратура (скоро)', '🔙 Назад']
level_kb = make_keyboard(level_buttons)

def send_main_menu(user_id, text=None):
    if not text:
        text = "Добро пожаловать! Я бот приёмной комиссии Пермского института РЭУ. Выберите действие:"
    send_photo(user_id, PHOTO_WELCOME, text, main_kb)

# Обработка
print("Бот запущен...")
for event in longpoll.listen():
    if event.type != VkBotEventType.MESSAGE_NEW or not event.message.text:
        continue
    user_id = event.message.peer_id
    msg = event.message.text.strip()

    # Состояние теста
    if user_id in user_states and "test" in user_states[user_id]:
        state = user_states[user_id]["test"]
        q_num = state["step"]
        if q_num < len(state["questions"]):
            # Ищем ответ
            options = state["questions"][q_num][1]
            if msg in options:
                state["answers"].append(options.index(msg))
                state["step"] += 1
                if state["step"] < len(state["questions"]):
                    q_text, opts = state["questions"][state["step"]]
                    kb = make_keyboard(opts)
                    send(user_id, q_text, kb)
                else:
                    # Подсчёт результатов
                    spo_scores = [0,0,0,0]  # IT, Эконом, Еда, Торговля
                    bachelor_scores = [0,0,0,0]
                    for ans in state["answers"]:
                        if state["level"] == "spo":
                            spo_scores[ans] += 1
                        else:
                            bachelor_scores[ans] += 1
                    if state["level"] == "spo":
                        max_idx = spo_scores.index(max(spo_scores))
                        if max_idx == 0: rec = "Информационные системы и программирование (СПО)"
                        elif max_idx == 1: rec = "Экономика и бухучёт, Банковское дело или Страховое дело (СПО)"
                        elif max_idx == 2: rec = "Поварское и кондитерское дело (СПО)"
                        else: rec = "Торговое дело (СПО)"
                    else:
                        max_idx = bachelor_scores.index(max(bachelor_scores))
                        if max_idx == 0: rec = "Прикладная информатика (бакалавриат)"
                        elif max_idx == 1: rec = "Менеджмент (бакалавриат)"
                        elif max_idx == 2: rec = "Экономика (бакалавриат)"
                        else: rec = "Торговое дело или Товароведение (бакалавриат)"
                    send(user_id, f"🎉 Тест завершён!\n\n✨ Рекомендуем: {rec}", main_kb)
                    del user_states[user_id]["test"]
            else:
                # Неверный ответ — повторяем вопрос
                q_text, opts = state["questions"][state["step"]]
                kb = make_keyboard(opts)
                send(user_id, q_text, kb)
        continue

    # Ожидание вопроса администратору
    if user_states.get(user_id) == "waiting_question":
        vk.messages.send(user_id=ADMIN_ID, message=f"Вопрос от [id{user_id}|]:\n{msg}", random_id=random.randint(1, 2**63-1))
        send(user_id, "Вопрос передан администратору. Ответ придёт в ближайшее время.", main_kb)
        del user_states[user_id]
        continue

    # Основные команды
    if msg == "📅 Дни открытых дверей":
        text = ("🗓️ Дни открытых дверей в Пермском институте РЭУ\n📍 Адрес: 614070, г. Пермь, б-р Гагарина, д. 57\n📅 23 апреля 2026 г., 18:00\n❗ Регистрация: https://forms.yandex.ru/u/696612da95add521ace1d211/\n📞 Телефон: +7 (342) 263-26-75")
        send_photo(user_id, PHOTO_OPEN_DAYS, text, main_kb)

    elif msg == "🕒 Работа приёмной комиссии":
        text = ("🕒 Контакты приёмной комиссии\n📞 +7 (342) 263-26-75\n📍 г. Пермь, б-р Гагарина, 57\n✉️ perm.pk@rea.ru\n🌐 rea.perm.ru\n🕒 Пн-пт 09:00–18:00, Сб 10:00–14:00\n📱 VK: https://vk.com/rea_perm\n📱 Telegram: https://t.me/PlekhanovUniversity")
        send_photo(user_id, PHOTO_ADMISSION_HOURS, text, main_kb)

    elif msg == "🎓 Специальности":
        user_states[user_id] = {"menu": "level"}
        send(user_id, "Выберите уровень образования:", level_kb)

    elif msg == "❓ Помощь":
        send(user_id, "Напишите ваш вопрос, я передам администратору.")
        user_states[user_id] = "waiting_question"

    elif msg == "🔙 Назад":
        # Возврат в главное меню
        if user_id in user_states:
            del user_states[user_id]
        send_main_menu(user_id)

    # Обработка выбора уровня
    elif msg == "📚 СПО (9-11)":
        buttons = [spec["short"] for spec in specialties_spo.values()] + ["🔙 Назад"]
        kb = make_keyboard(buttons)
        send(user_id, "Выберите специальность СПО:", kb)
        user_states[user_id] = {"menu": "spo_list"}

    elif msg == "🎓 Бакалавриат":
        buttons = [spec["short"] for spec in specialties_bachelor.values()] + ["🔙 Назад"]
        kb = make_keyboard(buttons)
        send(user_id, "Выберите направление бакалавриата:", kb)
        user_states[user_id] = {"menu": "bachelor_list"}

    elif msg == "📖 Магистратура (скоро)":
        send(user_id, "🔜 Информация о магистратуре появится позже.", main_kb)
        if user_id in user_states:
            del user_states[user_id]

    # Обработка выбора специальности СПО
    elif user_states.get(user_id, {}).get("menu") == "spo_list" and msg != "🔙 Назад":
        for spec in specialties_spo.values():
            if spec["short"] == msg:
                text = f"📌 {spec['title']}\n\n{spec['more_info']}"
                actions = ["📝 Пройти профтест", "🔙 Назад"]
                kb = make_keyboard(actions)
                send_photo(user_id, spec["photo_id"], text, kb)
                user_states[user_id] = {"selected_spec": spec, "level": "spo", "menu": "spec_action"}
                break

    # Обработка выбора специальности бакалавриата
    elif user_states.get(user_id, {}).get("menu") == "bachelor_list" and msg != "🔙 Назад":
        for spec in specialties_bachelor.values():
            if spec["short"] == msg:
                text = f"📌 {spec['title']}\n\n{spec['more_info']}"
                actions = ["📝 Пройти профтест", "🔙 Назад"]
                kb = make_keyboard(actions)
                send_photo(user_id, spec["photo_id"], text, kb)
                user_states[user_id] = {"selected_spec": spec, "level": "bachelor", "menu": "spec_action"}
                break

    # Действия после выбора специальности
    elif user_states.get(user_id, {}).get("menu") == "spec_action":
        if msg == "📝 Пройти профтест":
            level = user_states[user_id]["level"]
            questions = test_spo if level == "spo" else test_bachelor
            user_states[user_id]["test"] = {
                "step": 0,
                "answers": [],
                "questions": questions,
                "level": level
            }
            q_text, opts = questions[0]
            kb = make_keyboard(opts)
            send(user_id, q_text, kb)
        elif msg == "🔙 Назад":
            # Вернуться к списку специальностей
            if user_states[user_id]["level"] == "spo":
                buttons = [spec["short"] for spec in specialties_spo.values()] + ["🔙 Назад"]
                kb = make_keyboard(buttons)
                send(user_id, "Выберите специальность СПО:", kb)
                user_states[user_id] = {"menu": "spo_list"}
            else:
                buttons = [spec["short"] for spec in specialties_bachelor.values()] + ["🔙 Назад"]
                kb = make_keyboard(buttons)
                send(user_id, "Выберите направление бакалавриата:", kb)
                user_states[user_id] = {"menu": "bachelor_list"}

    # Если сообщение не распознано
    else:
        send_main_menu(user_id)
