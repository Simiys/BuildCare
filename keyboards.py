from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


phone_request_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Для работы с ботом необходимо поделиться номером телефона", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def start_cleaning_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать уборку")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def building_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пятницкая, 7A")],
            [KeyboardButton(text="Свободы, 95к2")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def skip_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пропустить➡️")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def order_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Туалетная бумага")],
            [KeyboardButton(text="Швабра")],
            [KeyboardButton(text="Мыло")],
            [KeyboardButton(text="Средство для сантехники")],
            [KeyboardButton(text="Мусорные мешки")],
            [KeyboardButton(text="Тряпки")],
            [KeyboardButton(text="Губки")],
            [KeyboardButton(text="Универсальное чистящее средство")],
            [KeyboardButton(text="Перчатки")],
            [KeyboardButton(text="Далее➡️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def fixes_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Лампочки")],
            [KeyboardButton(text="Стены")],
            [KeyboardButton(text="Ручки")],
            [KeyboardButton(text="Потолок")],
            [KeyboardButton(text="Плитка")],
            [KeyboardButton(text="Перила")],
            [KeyboardButton(text="Двери")],
            [KeyboardButton(text="Сан. узел")],
            [KeyboardButton(text="Далее➡️")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def consumables_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Туалетная бумага")],
            [KeyboardButton(text="Диффузор")],
            [KeyboardButton(text="Мыло")],
            [KeyboardButton(text="Мусорный пакет")],
            [KeyboardButton(text="Далее➡️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
def final_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Закончить уборку")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )