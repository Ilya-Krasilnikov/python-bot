import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
import os

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
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 3 года 10 мес\n"
            "• на базе 11 кл. — 2 года 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: бюджетных — 25, договорных — 110\n"
            "• 11 кл.: бюджетных — 5, договорных — 45\n\n"
            "📖 **Что изучают:**\n"
            "• программирование\n"
            "• инженерная графика\n"
            "• базы данных\n"
            "• web-дизайн\n\n"
            "💼 **Кем работают:**\n"
            "• техник-программист\n"
            "• 1С-программист\n"
            "• web-программист\n"
            "• администратор БД\n"
            "• системный администратор\n"
            "• инженер по информбезопасности\n"
            "• SEO-специалист"
        ),
        "photo_id": "-237266527_457239046"
    },
    2: {
        "title": "Экономика и бухгалтерский учёт",
        "short": "Экономика и бухучёт",
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 2 года 10 мес\n"
            "• на базе 11 кл. — 1 год 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: бюджетных — 15, договорных — 85\n"
            "• 11 кл.: бюджетных — 10, договорных — 40\n\n"
            "📖 **Что изучают:**\n"
            "• бухгалтерский учёт\n"
            "• расчёты с бюджетом\n"
            "• составление отчётности\n"
            "• бизнес-планирование\n"
            "• инвентаризация\n\n"
            "💼 **Кем работают:**\n"
            "• бухгалтер\n"
            "• экономист\n"
            "• финансовый аналитик\n"
            "• налоговый эксперт\n"
            "• аудитор\n"
            "• кадровик"
        ),
        "photo_id": "-237266527_457239047"
    },
    3: {
        "title": "Страховое дело",
        "short": "Страховое дело",
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 2 года 10 мес\n"
            "• на базе 11 кл. — 1 год 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: договорных — 25\n"
            "• 11 кл.: договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• экономика страхования\n"
            "• прямые и посреднические продажи\n"
            "• интернет-продажи страховых полисов\n"
            "• аудит страховых организаций\n"
            "• налогообложение в страховом деле\n\n"
            "💼 **Кем работают:**\n"
            "• страховой агент\n"
            "• менеджер по развитию агентских сетей\n"
            "• ведущий специалист по работе с клиентами\n"
            "• заместитель директора филиала"
        ),
        "photo_id": "-237266527_457239048"
    },
    4: {
        "title": "Банковское дело",
        "short": "Банковское дело",
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 2 года 10 мес\n"
            "• на базе 11 кл. — 1 год 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: бюджетных — 5, договорных — 45\n"
            "• 11 кл.: договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• финансы, денежное обращение и кредит\n"
            "• рынок ценных бумаг\n"
            "• депозитные операции\n"
            "• безналичные расчёты\n"
            "• финансовый анализ\n\n"
            "💼 **Кем работают:**\n"
            "• агент банка\n"
            "• кредитный специалист\n"
            "• операционист\n"
            "• финансовый менеджер\n"
            "• сотрудник бэк-офиса\n"
            "• ипотечный специалист"
        ),
        "photo_id": "-237266527_457239049"
    },
    5: {
        "title": "Торговое дело",
        "short": "Торговое дело",
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 2 года 10 мес\n"
            "• на базе 11 кл. — 1 год 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: бюджетных — 15, договорных — 80\n"
            "• 11 кл.: договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• маркетинг и реклама\n"
            "• управление подразделением\n"
            "• экспертиза качества товаров\n"
            "• документационное обеспечение\n"
            "• техническое оснащение\n\n"
            "💼 **Кем работают:**\n"
            "• товаровед\n"
            "• директор магазина\n"
            "• руководитель бизнеса\n"
            "• менеджер по продажам\n"
            "• мерчандайзер\n"
            "• торговый представитель"
        ),
        "photo_id": "-237266527_457239050"
    },
    6: {
        "title": "Поварское и кондитерское дело",
        "short": "Поварское дело",
        "more_info": (
            "🎓 **Поступление:** конкурс аттестатов (9 или 11 кл.)\n\n"
            "⏳ **Срок обучения:**\n"
            "• на базе 9 кл. — 3 года 10 мес\n"
            "• на базе 11 кл. — 2 года 10 мес\n\n"
            "💰 **Количество мест:**\n"
            "• 9 кл.: договорных — 40\n"
            "• 11 кл.: договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• организация процесса приготовления\n"
            "• метрология и стандартизация\n"
            "• микробиология и санитария\n"
            "• управление подразделением\n"
            "• физиология питания\n"
            "• десерты\n\n"
            "💼 **Кем работают:**\n"
            "• повар\n"
            "• бренд-шеф\n"
            "• технолог пищевого производства\n"
            "• повар-кондитер\n"
            "• менеджер ресторана\n"
            "• ресторатор\n"
            "• бармен\n"
            "• food-дизайнер"
        ),
        "photo_id": "-237266527_457239052"
    }
}

specialties_bachelor = {
    1: {
        "title": "Экономика",
        "short": "Экономика",
        "more_info": (
            "🎓 **Направление:** 38.03.01 Экономика\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 25\n"
            "• договорных — 30\n\n"
            "📖 **Что изучают:**\n"
            "• макро- и микроэкономика\n"
            "• эконометрика\n"
            "• финансы и кредит\n"
            "• бухгалтерский учёт и анализ\n"
            "• налоги и налогообложение\n\n"
            "💼 **Кем работают:**\n"
            "• экономист\n"
            "• финансовый аналитик\n"
            "• специалист банка\n"
            "• аудитор\n"
            "• налоговый консультант"
        ),
        "photo_id": "-237266527_457239062"
    },
    2: {
        "title": "Менеджмент",
        "short": "Менеджмент",
        "more_info": (
            "🎓 **Направление:** 38.03.02 Менеджмент\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 20\n"
            "• договорных — 35\n\n"
            "📖 **Что изучают:**\n"
            "• стратегический менеджмент\n"
            "• маркетинг\n"
            "• управление персоналом\n"
            "• логистика\n"
            "• бизнес-планирование\n\n"
            "💼 **Кем работают:**\n"
            "• менеджер проектов\n"
            "• HR-специалист\n"
            "• руководитель отдела\n"
            "• маркетолог\n"
            "• аналитик"
        ),
        "photo_id": "-237266527_457239061"
    },
    3: {
        "title": "Торговое дело",
        "short": "Торговое дело",
        "more_info": (
            "🎓 **Направление:** 38.03.06 Торговое дело\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 15\n"
            "• договорных — 40\n\n"
            "📖 **Что изучают:**\n"
            "• коммерческая деятельность\n"
            "• мерчандайзинг\n"
            "• логистика\n"
            "• товароведение\n"
            "• электронная торговля\n\n"
            "💼 **Кем работают:**\n"
            "• товаровед\n"
            "• менеджер по закупкам\n"
            "• коммерческий директор\n"
            "• категорийный менеджер\n"
            "• торговый представитель"
        ),
        "photo_id": "-237266527_457239060"
    },
    4: {
        "title": "Прикладная информатика",
        "short": "Прикладная информатика",
        "more_info": (
            "🎓 **Направление:** 09.03.03 Прикладная информатика\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 30\n"
            "• договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• программирование\n"
            "• базы данных\n"
            "• веб-технологии\n"
            "• информационная безопасность\n"
            "• бизнес-аналитика\n\n"
            "💼 **Кем работают:**\n"
            "• IT-специалист\n"
            "• разработчик\n"
            "• бизнес-аналитик\n"
            "• администратор БД\n"
            "• системный аналитик"
        ),
        "photo_id": "-237266527_457239059"
    },
    5: {
        "title": "Товароведение",
        "short": "Товароведение",
        "more_info": (
            "🎓 **Направление:** 38.03.07 Товароведение\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 10\n"
            "• договорных — 30\n\n"
            "📖 **Что изучают:**\n"
            "• товароведение продовольственных и непродовольственных товаров\n"
            "• экспертиза качества\n"
            "• стандартизация и сертификация\n"
            "• управление качеством\n\n"
            "💼 **Кем работают:**\n"
            "• товаровед-эксперт\n"
            "• специалист по качеству\n"
            "• менеджер по закупкам\n"
            "• эксперт в лаборатории\n"
            "• сотрудник Роспотребнадзора"
        ),
        "photo_id": "-237266527_457239058"
    },
    6: {
        "title": "Технология продукции и организация общественного питания",
        "short": "Технология питания",
        "more_info": (
            "🎓 **Направление:** 19.03.04 Технология продукции и организация общественного питания\n\n"
            "⏳ **Срок обучения:** 4 года (очная форма)\n\n"
            "💰 **Количество мест:**\n"
            "• бюджетных — 20\n"
            "• договорных — 25\n\n"
            "📖 **Что изучают:**\n"
            "• технология продукции общественного питания\n"
            "• контроль качества\n"
            "• микробиология\n"
            "• организация ресторанного бизнеса\n"
            "• разработка новых блюд\n\n"
            "💼 **Кем работают:**\n"
            "• технолог общественного питания\n"
            "• шеф-повар\n"
            "• менеджер ресторана\n"
            "• разработчик рецептур\n"
            "• руководитель производства"
        ),
        "photo_id": "--237266527_457239057"
    }
}

test_questions_spo = [
    {"text": "Что для вас важнее в будущей работе?", "options": ["💰 Высокий доход", "📈 Карьерный рост", "👨‍👩‍👧‍👦 Помощь людям", "🎨 Творческое самовыражение"]},
    {"text": "Какие школьные предметы вам нравятся больше всего?", "options": ["📐 Математика и физика", "💻 Информатика и ИКТ", "📖 Обществознание и право", "🍳 Технология (кулинария, труд)"]},
    {"text": "Как вы относитесь к работе с большим объёмом цифр и данных?", "options": ["😍 Обожаю анализировать", "😐 Нейтрально", "😫 С трудом", "😱 Боюсь и не люблю"]},
    {"text": "Вам больше нравится?", "options": ["🧑‍💻 Работа за компьютером", "🤝 Живое общение с людьми", "👩‍🍳 Создавать что-то руками", "📊 Планировать и анализировать"]},
    {"text": "Какой рабочий коллектив вам ближе?", "options": ["🏢 Крупная стабильная компания", "👨‍💼 Небольшой дружный отдел", "🙋‍♂️ Работать самостоятельно", "🚀 Свой стартап"]}
]

test_questions_bachelor = [
    {"text": "Какая сфера деятельности вас привлекает больше всего?", "options": ["💰 Финансы и аналитика", "🧑‍💼 Управление и менеджмент", "🛒 Торговля и логистика", "💻 Информационные технологии"]},
    {"text": "Что для вас важнее при выборе профессии?", "options": ["🏦 Стабильность и высокая зарплата", "🚀 Возможность карьерного роста", "🤝 Работа в команде", "🎨 Креатив и нестандартные задачи"]},
    {"text": "Какие задачи вам кажутся наиболее интересными?", "options": ["📈 Анализ данных и прогнозирование", "👥 Управление проектами и людьми", "🤝 Ведение переговоров и продажи", "🖥️ Разработка и внедрение систем"]},
    {"text": "Какой стиль работы вам ближе?", "options": ["📊 Кабинетный, с документами", "🗣️ Активный, много общения", "🔬 Исследовательский, поиск решений", "👨‍💻 Работа с компьютером и кодом"]},
    {"text": "Выберите ключевое качество успешного специалиста", "options": ["🧮 Аналитический склад ума", "🎯 Лидерские качества", "💬 Коммуникабельность", "⚙️ Техническое мышление"]}
]

user_states = {}

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
    kb.add_button('📚 СПО (9-11 классы)', color=VkKeyboardColor.POSITIVE)
    kb.add_button('🎓 Бакалавриат', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('📖 Магистратура (скоро)', color=VkKeyboardColor.SECONDARY)
    kb.add_button('❓ Помощь', color=VkKeyboardColor.SECONDARY)
    return kb

def get_spo_keyboard():
    kb = VkKeyboard(one_time=True)
    for spec in specialties_spo.values():
        kb.add_button(spec['short'], color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.NEGATIVE)
    return kb

def get_bachelor_keyboard():
    kb = VkKeyboard(one_time=True)
    for spec in specialties_bachelor.values():
        kb.add_button(spec['short'], color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.NEGATIVE)
    return kb

def get_spec_actions_keyboard(spec_id, level):
    kb = VkKeyboard(one_time=True)
    kb.add_button('📝 Пройти профтест', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 Назад к списку', color=VkKeyboardColor.SECONDARY)
    return kb

def start_test(user_id, level):
    user_states[user_id] = {"step": 0, "answers": [], "level": level}
    send_next_question(user_id)

def send_next_question(user_id):
    state = user_states.get(user_id)
    if not state or "step" not in state:
        return
    step = state["step"]
    level = state["level"]
    questions = test_questions_spo if level == "spo" else test_questions_bachelor
    if step < len(questions):
        q = questions[step]
        kb = VkKeyboard(one_time=True)
        for opt in q["options"]:
            kb.add_button(opt, color=VkKeyboardColor.SECONDARY)
            kb.add_line()
        send_message(user_id, q["text"], kb)
        state["step"] += 1
    else:
        answers = state["answers"]
        if level == "spo":
            if any("💻 Информатика" in a for a in answers):
                result = "Рекомендуем специальности СПО: Информационные системы и программирование."
            elif any("🍳 Технология" in a for a in answers):
                result = "Рекомендуем специальности СПО: Поварское и кондитерское дело."
            elif any("📐 Математика" in a or "📊 Анализировать" in a for a in answers):
                result = "Рекомендуем специальности СПО: Экономика, Банковское дело или Страховое дело."
            else:
                result = "Все специальности СПО могут вам подойти. Приходите на День открытых дверей!"
        else:
            if any("💰 Финансы" in a for a in answers) or any("📈 Анализ" in a for a in answers):
                result = "Рекомендуем направления бакалавриата: Экономика или Прикладная информатика."
            elif any("🧑‍💼 Управление" in a for a in answers) or any("👥 Управление проектами" in a for a in answers):
                result = "Рекомендуем направление: Менеджмент."
            elif any("🛒 Торговля" in a for a in answers) or any("🤝 Ведение переговоров" in a for a in answers):
                result = "Рекомендуем направления: Торговое дело или Товароведение."
            elif any("👩‍🍳 Создавать" in a for a in answers) or any("🍳 Технология" in a for a in answers):
                result = "Рекомендуем направление: Технология продукции и организация общественного питания."
            else:
                result = "Все направления бакалавриата могут вас заинтересовать. Приходите на День открытых дверей!"
        send_message(user_id, f"🎉 Тест завершён!\n\n{result}", get_main_keyboard())
        del user_states[user_id]

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
print("Бот запущен и работает 24/7...")

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
                    "📅 Ближайшая дата: 23 апреля 2026 г., начало в 18:00\n\n"
                    "Программа:\n"
                    "• Встреча с директором института\n"
                    "• Презентация специальностей СПО и бакалавриата\n"
                    "• Экскурсия по учебным корпусам и лабораториям\n"
                    "• Ответы на вопросы приёмной комиссии\n\n"
                    "❗ Регистрация: https://forms.yandex.ru/u/696612da95add521ace1d211/\n\n"
                    "📞 Телефон: +7 (342) 263-26-75")
            send_photo_with_text(user_id, PHOTO_OPEN_DAYS, text, get_main_keyboard())

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
                    "• Telegram: https://t.me/rea_perm")
            send_photo_with_text(user_id, PHOTO_ADMISSION_HOURS, text, get_main_keyboard())

        elif msg == "📚 СПО (9-11 классы)":
            send_message(user_id, "Выберите специальность СПО:", get_spo_keyboard())

        elif msg == "🎓 Бакалавриат":
            send_message(user_id, "Выберите направление бакалавриата:", get_bachelor_keyboard())

        elif msg == "📖 Магистратура (скоро)":
            send_message(user_id, "🔜 Информация о программах магистратуры появится позже. Следите за обновлениями!", get_main_keyboard())

        elif msg == "❓ Помощь":
            send_message(user_id, "Напишите ваш вопрос, и я передам его администратору. Ответ придёт в ближайшее время.")
            user_states[user_id] = "waiting_question"

        elif msg == "🔙 Назад":
            send_photo_with_text(user_id, PHOTO_WELCOME, "Добро пожаловать! Я бот приёмной комиссии Пермского института (филиала) РЭУ имени Г. В. Плеханова. С чем вам помочь сегодня?", get_main_keyboard())

        elif msg == "🔙 Назад к списку":
            send_message(user_id, "Выберите уровень образования:", get_main_keyboard())

        elif any(msg == spec['short'] for spec in specialties_spo.values()):
            spec = next(spec for spec in specialties_spo.values() if spec['short'] == msg)
            spec_id = next(i for i, s in specialties_spo.items() if s['short'] == msg)
            user_states[user_id] = {"selected_spec": spec_id, "level": "spo"}
            text = f"📌 {spec['title']}\n\n{spec['more_info']}"
            send_photo_with_text(user_id, spec['photo_id'], text, get_spec_actions_keyboard(spec_id, "spo"))

        elif any(msg == spec['short'] for spec in specialties_bachelor.values()):
            spec = next(spec for spec in specialties_bachelor.values() if spec['short'] == msg)
            spec_id = next(i for i, s in specialties_bachelor.items() if s['short'] == msg)
            user_states[user_id] = {"selected_spec": spec_id, "level": "bachelor"}
            text = f"📌 {spec['title']}\n\n{spec['more_info']}"
            send_photo_with_text(user_id, spec['photo_id'], text, get_spec_actions_keyboard(spec_id, "bachelor"))

        elif msg == "📝 Пройти профтест":
            level = user_states.get(user_id, {}).get("level")
            if level in ("spo", "bachelor"):
                start_test(user_id, level)
            else:
                send_message(user_id, "Сначала выберите специальность или направление.", get_main_keyboard())

        else:
            send_photo_with_text(user_id, PHOTO_WELCOME, "Добро пожаловать! Я бот приёмной комиссии Пермского института (филиала) РЭУ имени Г. В. Плеханова. С чем вам помочь сегодня?", get_main_keyboard())
