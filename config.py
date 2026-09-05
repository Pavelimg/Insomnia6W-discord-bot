import os

from dotenv import load_dotenv

load_dotenv()

settings = {
    "ID": "535128939170103307",
    "token": os.getenv("DISCORD_BOT_TOKEN", ""),
    "bot_name": "Insomnia",
    "prefix": "!",
}

if not settings["token"]:
    raise RuntimeError("DISCORD_BOT_TOKEN is not configured")

links = {
    "insomnia_gif": "https://cdn.discordapp.com/attachments/514854375663992837/817422476886933554/Insomnia.gif",
    "insomnia_avatar": "https://www.meme-arsenal.com/memes/9b5d4ed428e6d1efa70f394c03420b49.jpg",
    "zones": "https://cdn.discordapp.com/attachments/816413867671945256/826870699041620028/Cube.png",
}

authors = {
    "author": "Pavel.IMG",
    "co-author": "MishaSok",
}

db_settings = {
    "db_entry_money": 0,
}

help_embed_1 = (
    ("!help", "Показывает это сообщение"),
    ("!zones", "Показывает карту проекта (все зоны)"),
    ("!meme", "Присылает случайный мем на английском"),
    ("!balance", "Показывает баланс"),
    ("!pay <кому> <кол-во>", "Переводит средства отмеченному пользователю"),
)

help_embed_2 = (
    ("!give_money <кому> <кол-во>", "Добавляет средства пользователю"),
    ("!set_money <кому> <кол-во>", "Изменяет баланс пользователя"),
    ("!add_shop_role <название> <роль> <цена>", "Добавляет роль в магазин"),
    ("!add_shop_item <название> <цена>", "Добавляет предмет в магазин"),
)

stuff = (
    ("Pavel.img", "Главный администратор"),
    ("MishaSok", "Глава Community центра"),
    ("LazyMike", "Веб-программист проекта"),
)

__all__ = [
    "settings",
    "links",
    "authors",
    "db_settings",
    "help_embed_1",
    "help_embed_2",
    "stuff",
]

