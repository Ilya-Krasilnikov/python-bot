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

specialties_spo = {
    1: {
        "title": "Информационные системы и программирование",
        "short": "Программирование",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 3 года 10 мес\n• 11 кл. — 2 года 10 мес\n\n💰 Места:\n• 9 кл.: бюджет 25, договор 110\n• 11 кл.: бюджет 5, договор 45\n\n📖 Изучают: программирование, БД, web-дизайн\n\n💼 Кем работают: программист, 1С, web, админ БД, сисадмин, инженер ИБ, SEO",
        "photo_id": "-237266527_457239046"
    },
    2: {
        "title": "Экономика и бухгалтерский учёт",
        "short": "Экономика и бухучёт",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 2 года 10 мес\n• 11 кл. — 1 год 10 мес\n\n💰 Места:\n• 9 кл.: бюджет 15, договор 85\n• 11 кл.: бюджет 10, договор 40\n\n📖 Изучают: бухучёт, расчёты с бюджетом, отчётность, бизнес-планирование, инвентаризация\n\n💼 Кем работают: бухгалтер, экономист, финаналитик, налоговый эксперт, аудитор, кадровик",
        "photo_id": "-237266527_457239047"
    },
    3: {
        "title": "Страховое дело",
        "short": "Страховое дело",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 2 года 10 мес\n• 11 кл. — 1 год 10 мес\n\n💰 Места:\n• 9 кл.: договор 25\n• 11 кл.: договор 25\n\n📖 Изучают: экономика страхования, продажи, аудит, налогообложение\n\n💼 Кем работают: страховой агент, менеджер по развитию, ведущий специалист, зам. директора филиала",
        "photo_id": "-237266527_457239048"
    },
    4: {
        "title": "Банковское дело",
        "short": "Банковское дело",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 2 года 10 мес\n• 11 кл. — 1 год 10 мес\n\n💰 Места:\n• 9 кл.: бюджет 5, договор 45\n• 11 кл.: договор 25\n\n📖 Изучают: финансы, кредит, ценные бумаги, депозиты, безналичные расчёты, финанализ\n\n💼 Кем работают: агент банка, кредитный специалист, операционист, финаменеджер, сотрудник бэк-офиса, ипотечный специалист",
        "photo_id": "-237266527_457239049"
    },
    5: {
        "title": "Торговое дело",
        "short": "Торговое дело",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 2 года 10 мес\n• 11 кл. — 1 год 10 мес\n\n💰 Места:\n• 9 кл.: бюджет 15, договор 80\n• 11 кл.: договор 25\n\n📖 Изучают: маркетинг, реклама, управление подразделением, экспертиза товаров, документооборот\n\n💼 Кем работают: товаровед, директор магазина, руководитель бизнеса, менеджер по продажам, мерчандайзер, торговый представитель",
        "photo_id": "-237266527_457239050"
    },
    6: {
        "title": "Поварское и кондитерское дело",
        "short": "Поварское дело",
        "more_info": "🎓 Поступление: конкурс аттестатов (9 или 11 кл.)\n\n⏳ Срок обучения:\n• 9 кл. — 3 года 10 мес\n• 11 кл. — 2 года 10 мес\n\n💰 Места:\n• 9 кл.: договор 40\n• 11 кл.: договор 25\n\n📖 Изучают: организация приготовления, метрология, микробиология, управление, физиология питания, десерты\n\n💼 Кем работают: повар, бренд-шеф, технолог, повар-кондитер, менеджер ресторана, ресторатор, бармен, food-дизайнер",
        "photo_id": "-237266527_457239052"
    }
}

specialties_bachelor = {
    1: {
        "title": "Экономика",
        "short": "Экономика",
        "more_info": "🎓 Направление: 38.03.01 Экономика\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 25, договор 30\n\n📖 Изучают: макро- и микроэкономика, эконометрика, финансы, бухучёт, налоги\n\n💼 Кем работают: экономист, финаналитик, специалист банка, аудитор, налоговый консультант",
        "photo_id": "-237266527_457239062"
    },
    2: {
        "title": "Менеджмент",
        "short": "Менеджмент",
        "more_info": "🎓 Направление: 38.03.02 Менеджмент\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 20, договор 35\n\n📖 Изучают: стратегический менеджмент, маркетинг, управление персоналом, логистика, бизнес-планирование\n\n💼 Кем работают: менеджер проектов, HR, руководитель отдела, маркетолог, аналитик",
        "photo_id": "-237266527_457239061"
    },
    3: {
        "title": "Торговое дело",
        "short": "Торговое дело",
        "more_info": "🎓 Направление: 38.03.06 Торговое дело\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 15, договор 40\n\n📖 Изучают: коммерция, мерчандайзинг, логистика, товароведение, электронная торговля\n\n💼 Кем работают: товаровед, менеджер по закупкам, коммерческий директор, категорийный менеджер, торговый представитель",
        "photo_id": "-237266527_457239060"
    },
    4: {
        "title": "Прикладная информатика",
        "short": "Прикладная информатика",
        "more_info": "🎓 Направление: 09.03.03 Прикладная информатика\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 30, договор 25\n\n📖 Изучают: программирование, БД, веб-технологии, информационная безопасность, бизнес-аналитика\n\n💼 Кем работают: IT-специалист, разработчик, бизнес-аналитик, администратор БД, системный аналитик",
        "photo_id": "-237266527_457239059"
    },
    5: {
        "title": "Товароведение",
        "short": "Товароведение",
        "more_info": "🎓 Направление: 38.03.07 Товароведение\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 10, договор 30\n\n📖 Изучают: товароведение прод. и непрод. товаров, экспертиза, стандартизация, управление качеством\n\n💼 Кем работают: товаровед-эксперт, специалист по качеству, менеджер по закупкам, эксперт лаборатории, сотрудник Роспотребнадзора",
        "photo_id": "-237266527_457239058"
    },
    6: {
        "title": "Технология продукции и организация общественного питания",
        "short": "Технология питания",
        "more_info": "🎓 Направление: 19.03.04 Технология продукции и организация общественного питания\n\n⏳ Срок обучения: 4 года (очная)\n\n💰 Места: бюджет 20, договор 25\n\n📖 Изучают: технология продукции общепита, контроль качества, микробиология, организация ресторанного бизнеса, разработка блюд\n\n💼 Кем работают: технолог общепита, шеф-повар, менеджер ресторана, разработчик рецептур, руководитель производства",
        "photo_id": "-237266527_457239057"
    }
}

# Вопросы для теста СПО (4 варианта, короткие)
test_spo = [
    ("💻 Какая сфера вам ближе?", ["💻 Программирование и IT", "💰 Экономика и финансы", "🍳 Ресторанный бизнес", "🛒 Торговля и продажи"]),
    ("🧑‍💻 Что вас привлекает в работе?", ["🧑‍💻 Создавать программы", "📊 Анализировать данные", "🍝 Готовить блюда", "🤝 Общаться с людьми"]),
    ("🔧 Какую задачу вы решите лучше?", ["🖥️ Написать код", "📈 Составить бизнес-план", "🍽️ Организовать кухню", "💬 Провести переговоры"]),
    ("🏢 Ваше идеальное место работы?", ["🏢 IT-компания", "🏦 Банк", "🍽️ Ресторан", "🛍️ Магазин"]),
    ("🚀 Какой бизнес вы бы открыли?", ["🚀 Разработка приложений", "💸 Финансовые услуги", "🍕 Кафе", "📦 Интернет-магазин"]),
]

# Вопросы для теста бакалавриата
test_bachelor = [
    ("💼 Какое направление перспективно?", ["💻 Информационные технологии", "👔 Управление", "💰 Финансы", "🛒 Маркетинг"]),
    ("👥 В какой роли вы видите себя?", ["⚙️ Технический эксперт", "👥 Руководитель", "📊 Аналитик", "🤝 Переговорщик"]),
    ("🔧 Какая задача интереснее?", ["🔧 Техническая", "🗣️ Стратегическая", "📉 Финансовая", "💡 Креативная"]),
    ("🏢 Какая культура вам ближе?", ["🧑‍💻 IT-команда", "👔 Иерархия", "📊 Работа с данными", "🎯 Клиентоориентированность"]),
    ("🎯 Что важнее в работе?", ["🚀 Интересные задачи", "💼 Высокий доход", "🏦 Стабильность", "🎨 Творчество"]),
]

user_states = {}

# Flask для healthcheck (чтобы Render не выключал)
app = Flask(__name__)
@app.route('/')
def healthcheck():
    return "OK", 200
def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
threading.Thread(target=run_web, daemon=True).start()

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

main_buttons = ['📅 Дни открытых дверей', '🕒 Работа приёмной комиссии', '🎓 Специальности', '❓ Помощь']
main_kb = make_keyboard(main_buttons, one_time=False)

level_buttons = ['📚 СПО (9-11)', '🎓 Бакалавриат', '📖 Магистратура (скоро)', '🔙 Назад']
level_kb = make_keyboard(level_buttons)

def send_main_menu(user_id, text=None):
    if not text:
        text = "Добро пожаловать! Я бот приёмной комиссии Пермского института РЭУ. Выберите действие:"
    send_photo(user_id, PHOTO_WELCOME, text, main_kb)

print("Бот запущен...")

for event in longpoll.listen():
    if event.type != VkBotEventType.MESSAGE_NEW or not event.message.text:
        continue
    user_id = event.message.peer_id
    msg = event.message.text.strip()

    # ---- Обработка теста ----
    if user_id in user_states and "test" in user_states[user_id]:
        state = user_states[user_id]["test"]
        step = state["step"]
        questions = state["questions"]
        if step < len(questions):
            q_text, opts = questions[step]
            if msg in opts:
                state["answers"].append(opts.index(msg))
                state["step"] += 1
                if state["step"] < len(questions):
                    q_text2, opts2 = questions[state["step"]]
                    send(user_id, q_text2, make_keyboard(opts2))
                else:
                    # Подсчёт результатов
                    spo_scores = [0,0,0,0]
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
                send(user_id, q_text, make_keyboard(opts))
        continue

    # ---- Ожидание вопроса администратору ----
    if user_states.get(user_id) == "waiting_question":
        vk.messages.send(user_id=ADMIN_ID, message=f"Вопрос от [id{user_id}|]:\n{msg}", random_id=random.randint(1, 2**63-1))
        send(user_id, "Вопрос передан администратору. Ответ придёт в ближайшее время.", main_kb)
        del user_states[user_id]
        continue

    # ---- Главное меню ----
    if msg == "📅 Дни открытых дверей":
        text = ("🗓️ Дни открытых дверей в Пермском институте (филиале) РЭУ им. Г. В. Плеханова\n\n📍 Адрес: 614070, г. Пермь, б-р Гагарина, д. 57\n\n📅 23 апреля 2026 г., 18:00\n\n❗ Регистрация: https://forms.yandex.ru/u/696612da95add521ace1d211/\n\n📞 Телефон: +7 (342) 263-26-75")
        send_photo(user_id, PHOTO_OPEN_DAYS, text, main_kb)

    elif msg == "🕒 Работа приёмной комиссии":
        text = ("🕒 Контакты приёмной комиссии Пермского филиала\n\n"
                "📞 Телефон: +7 (342) 263-26-75\n"
                "📍 Адрес: г. Пермь, б-р Гагарина, д. 57\n"
                "✉️ E-mail: perm.pk@rea.ru\n"
                "🌐 Сайт: https://rea.perm.ru\n\n"
                "🕒 Часы работы:\n"
                "• Пн-пт: 09:00 – 18:00\n"
                "• Сб: 10:00 – 14:00\n"
                "• Вс: выходной\n\n"
                "📱 Мы в соцсетях:\n"
                "• VK: https://vk.com/rea_perm\n"
                "• Telegram: https://t.me/PlekhanovUniversity")
        send_photo(user_id, PHOTO_ADMISSION_HOURS, text, main_kb)

    elif msg == "🎓 Специальности":
        user_states[user_id] = {"menu": "level"}
        send(user_id, "Выберите уровень образования:", level_kb)

    elif msg == "❓ Помощь":
        send(user_id, "Напишите ваш вопрос, я передам администратору.")
        user_states[user_id] = "waiting_question"

    elif msg == "🔙 Назад":
        if user_id in user_states:
            del user_states[user_id]
        send_main_menu(user_id)

    # ---- Выбор уровня ----
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

    # ---- Выбор специальности СПО ----
    elif user_states.get(user_id, {}).get("menu") == "spo_list" and msg != "🔙 Назад":
        for spec in specialties_spo.values():
            if spec["short"] == msg:
                text = f"📌 {spec['title']}\n\n{spec['more_info']}"
                actions = ["📝 Пройти профтест", "🔙 Назад"]
                kb = make_keyboard(actions)
                send_photo(user_id, spec["photo_id"], text, kb)
                user_states[user_id] = {"selected_spec": spec, "level": "spo", "menu": "spec_action"}
                break

    # ---- Выбор специальности бакалавриата ----
    elif user_states.get(user_id, {}).get("menu") == "bachelor_list" and msg != "🔙 Назад":
        for spec in specialties_bachelor.values():
            if spec["short"] == msg:
                text = f"📌 {spec['title']}\n\n{spec['more_info']}"
                actions = ["📝 Пройти профтест", "🔙 Назад"]
                kb = make_keyboard(actions)
                send_photo(user_id, spec["photo_id"], text, kb)
                user_states[user_id] = {"selected_spec": spec, "level": "bachelor", "menu": "spec_action"}
                break

    # ---- Действия после выбора специальности ----
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
            send(user_id, q_text, make_keyboard(opts))
        elif msg == "🔙 Назад":
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

    # ---- Неизвестная команда ----
    else:
        send_main_menu(user_id)
