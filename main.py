import discord
from discord import File
import sqlite3
import requests
import json
import asyncio
import random
import discord.utils
from datetime import *
from discord.ext import commands
from config import *
from data_text import rules
from Cybernator import Paginator
from non_db_func import *
from Library import Ring

# Создание intents для работы с намерениями
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)
bot.remove_command('help')
# DATA-TEXT
r1, r2, r3, r4, r5 = rules[1], rules[2], rules[3], rules[4], rules[5]

# Data-Base
data_base = sqlite3.connect('bot_test.db', timeout=10)
cursor = data_base.cursor()

print("Loading casino..")
casinoring = Ring("ring", "png", "arrow.png")
casinoring.create_files(1)
print("Casino loaded")


# List of bot events
@bot.event
async def on_ready():
    print('Bot launched successfully :)')
    print(f'My name is {bot.user.name}')
    print(f'My client id is {bot.user.id}')
    for guild in bot.guilds:
        print(f'Connected to server, id is: {guild.id}')
        for member in guild.members:
            cursor.execute(f"SELECT id FROM users where id={member.id}")
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', {db_settings['db_entry_money']})")
            else:
                pass
            data_base.commit()


@bot.event
async def on_message(message):
    if message.content.startswith('!member'):
        for guild in bot.guilds:
            for member in guild.members:
                await message.channel.send(member)
    await bot.process_commands(message)


@bot.event
async def on_command_error(error, *args):
    embed = discord.Embed(title='Оповещение', color=0xFF0000)
    embed.add_field(name='Ошибка',
                    value='Возможно вы допустили ошибку при написании команды. '
                          'Если ошибку не получается исправить, свяжитесь с @MishaSok#6723 или @Pavel.img#8636')
    await error.send(embed=embed)


@bot.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users where id={member.id}")
    if cursor.fetchone() is None:
        cursor.execute(
            f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', {db_settings['db_entry_money']})")
    else:
        pass
    data_base.commit()
    await bot.process_commands(member)


# List of bot commands
# Data-Base commands below
@bot.command()
async def balance(ctx):
    for row in cursor.execute(f"SELECT nickname, money FROM users where id={ctx.author.id}"):
        embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
        embed.set_author(name='Insomnia Community Bot',
                         icon_url=links['insomnia_avatar'])
        embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def give_money(ctx, mention, money):
    try:
        mention = str(mention).replace('!', '')
        for row in cursor.execute(f'SELECT money FROM users where mention=?', (mention,)):
            cursor.execute(f'UPDATE users SET money={int(money) + row[0]} where mention=?', (mention,))
        data_base.commit()
        for row in cursor.execute(f'SELECT nickname FROM users where mention=?', (mention,)):
            embed = discord.Embed(title='Пополнение баланса', color=0x42f566)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Оповещение', value=f'Баланс пользователя {row[0]} пополнен на {money} SH')
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title='Оповещение', color=0xFF0000)
        embed.add_field(name='Ововещение', value='Ошибка при выполнение программы.')
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def set_money(ctx, mention, money):
    try:
        ment = str(mention).replace('!', '')
        cursor.execute(f'UPDATE users SET money={money} where mention=?', (ment,))
        data_base.commit()
        embed = discord.Embed(title='Изменение баланса', color=0x42f566)
        embed.set_author(name='Insomnia Community Bot',
                         icon_url=links['insomnia_avatar'])
        embed.add_field(name='Оповещение', value=f'Баланс пользователя {mention} изменён на {money} SH')
        await ctx.send(embed=embed)
    except Exception as E:
        print(f'set money Error: {E}')
        embed = discord.Embed(title='Оповещение', color=0xFF0000)
        embed.add_field(name='Ововещение', value='Ошибка при выполнение программы.')
        await ctx.send(embed=embed)


@bot.command()
async def pay(ctx, mention, money):
    try:
        mention = str(mention).replace('!', '')
        for row in cursor.execute(f'SELECT money FROM users where id=?', (ctx.author.id,)):
            money_from = row[0]
            for row_1 in cursor.execute(f'SELECT money FROM users where mention=?', (mention,)):
                money_to = row_1[0]
                cursor.execute(f'UPDATE users SET money={money_from - int(money)} where id=?', (ctx.author.id,))
                cursor.execute(f'UPDATE users SET money={money_to + int(money)} where mention=?', (mention,))
                data_base.commit()
                embed = discord.Embed(title='Перевод средств', color=0x42f566)
                embed.set_author(name='Insomnia Community Bot',
                                 icon_url=links['insomnia_avatar'])
                embed.add_field(name='Оповещение',
                                value=f'Пользователь {ctx.author.mention} перевел {money} SH пользователю {mention}')
                await ctx.send(embed=embed)
    except Exception as E:
        print(f'"Pay" command Error: {E}')


@bot.command()
@commands.has_permissions(administrator=True)
async def add_shop_role(ctx, name, id, cost):
    try:
        cursor.execute(f'SELECT id FROM shop where id=?', (id,))
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO shop VALUES (?, ?, ?, ?)", (name, 'ROLE', cost, id))
            data_base.commit()
            embed = discord.Embed(title='Оповещение', color=0x00ff00)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Добавление роли в базу данных',
                            value=f'Роль {id} была успешно добавлена в базу данных')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Оповещение', color=0xFF0000)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Ошибка',
                            value=f'Роль {id} уже имеется в базе данных')
            await ctx.send(embed=embed)
    except Exception as e:
        print('"add_shop_role" Error', e)


@bot.command()
@commands.has_permissions(administrator=True)
async def add_shop_item(ctx, name, cost):
    try:
        cursor.execute(f'SELECT id FROM shop where name=?', (name,))
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO shop VALUES (?, ?, ?, ?)",
                           (str(' '.join(str(name).split('.'))), 'ITEM', cost, str(datetime.now())))
            data_base.commit()
            embed = discord.Embed(title='Оповещение', color=0x00ff00)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Добавление предмета в базу данных',
                            value=f"Предмет {str(' '.join(str(name).split('.')))} был успешно добавлена в базу данных")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Оповещение', color=0xFF0000)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Ошибка',
                            value=f'Предмет {name} уже имеется в базе данных')
            await ctx.send(embed=embed)
    except Exception as e:
        print("add_shop_item Error:", e)
        embed = discord.Embed(title='Ошибка', color=0xFF0000)
        embed.add_field(name='Error', value=str(e))
        await ctx.send(embed=embed)


@bot.command()
async def shop(ctx):
    try:
        embed = discord.Embed(title='Магазин ролей', color=0x00ff00)
        embed.set_author(name='Insomnia Community Bot',
                         icon_url=links['insomnia_avatar'])
        for row in cursor.execute(f'SELECT id, cost, name FROM shop WHERE type=?', ('ROLE',)):
            embed.add_field(name=f'Роль {row[2]}',
                            value=f'Наименование товара: {row[0]}\n'
                                  f'Цена товара: {row[1]}', inline=False)
        embed2 = discord.Embed(title='Магазин предметов', color=0x00ff00)
        embed2.set_author(name='Insomnia Community Bot',
                          icon_url=links['insomnia_avatar'])
        for row in cursor.execute(f'SELECT id, cost, name FROM shop WHERE type=?', ('ITEM',)):
            embed2.add_field(name=f'{row[2]}',
                             value=f'Наименование товара: {row[2]}\n'
                                   f'Цена товара: {row[1]}', inline=False)
        embeds = [embed, embed2]
        message = await ctx.send(embed=embed)
        page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds)
        await page.start()
    except Exception as E:
        print("shop command Error", E)


@bot.command()
async def buy_role(ctx, *product):
    try:
        if not discord.utils.get(ctx.author.roles, name=' '.join(product)):
            for row in cursor.execute(f'SELECT name, cost, id FROM shop WHERE name=?', (str(' '.join(product)),)):
                for row_2 in cursor.execute(f'SELECT money FROM users WHERE id=?', (ctx.author.id,)):
                    cash = int(row_2[0]) - int(row[1])
                    if cash < 0:
                        embed = discord.Embed(title='Оповещение', color=0xFF0000)
                        embed.set_author(name='Insomnia Community Bot',
                                         icon_url=links['insomnia_avatar'])
                        embed.add_field(name='Не хватает средств',
                                        value=f"Вам не хватает {abs(cash)} для покупки этой роли")
                        await ctx.send(embed=embed)
                    else:
                        cursor.execute(f'UPDATE users SET money={cash} WHERE id=?', (ctx.author.id,))
                        data_base.commit()
                        embed = discord.Embed(title='Оповещение', color=0x00ff00)
                        embed.set_author(name='Insomnia Community Bot',
                                         icon_url=links['insomnia_avatar'])
                        embed.add_field(name='Покупка',
                                        value=f"Пользователь {ctx.author.mention} приобрел роль {row[0]} за {row[1]} SH")
                        await ctx.send(embed=embed)
                        role = discord.utils.get(ctx.message.guild.roles, name=row[0])
                        await ctx.author.add_roles(role)
            if cursor.fetchone():
                embed = discord.Embed(title='Оповещение', color=0xFF0000)
                embed.set_author(name='Insomnia Community Bot',
                                 icon_url=links['insomnia_avatar'])
                embed.add_field(name='Ошибка', value=f"Роль {str(' '.join(product))} не найдена в базе данных Insomnia")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Оповещение', color=0xFF0000)
            embed.set_author(name='Insomnia Community Bot',
                             icon_url=links['insomnia_avatar'])
            embed.add_field(name='Ошибка',
                            value=f"У вас уже есть эта роль")
            await ctx.send(embed=embed)
    except Exception as e:
        print("buy command Error:", e)


@bot.command()
async def casino(ctx, *args):
    try:
        global casinoring
        bet = int(args[0])
        for row in cursor.execute('SELECT money FROM users where id=?', (ctx.author.id,)):
            if bet >= int(row[0]):
                embed = discord.Embed(title='Оповещение', color=0x00ff00)
                embed.set_author(name='Insomnia Community Bot',
                                 icon_url=links['insomnia_avatar'])
                embed.add_field(name='Ошибка',
                                value='На вашем счету недостаточно средств для ставки в нашем еврейском казино')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Оповещение', color=0x00ff00)
                embed.set_author(name='Insomnia Community Bot',
                                 icon_url=links['insomnia_avatar'])
                embed.add_field(name='Разкручивем рулетку.....',
                                value=f'вы поставили {bet} SH')
                await ctx.send(embed=embed)
                print("было " + str(int(row[0])))
                print("после списания " + str(int(row[0]) - bet))
                WinRate = casinoring.create_pro_video(random.randint(0, 360), 30,
                                                      [[25, 5], [25, 4], [25, 3], [25, 2], [25, 1], [10, 0]])
                print(WinRate)
                print("После игры" + str(int(row[0]) + bet * WinRate))
                data_base.commit()
                if WinRate > 1:
                    cursor.execute(f'UPDATE users SET money={int(row[0]) + bet * (WinRate - 1)} where id=?',
                                   (ctx.author.id,))
                    embed = discord.Embed(title='Оповещение', color=0x00ff00)
                    embed.set_author(name='Insomnia Community Bot',
                                     icon_url=links['insomnia_avatar'])
                    embed.add_field(name='Победа',
                                    value=f'Ваш баланс был пополнен на {bet * (WinRate - 1)} SH')
                else:
                    embed = discord.Embed(title='Оповещение', color=0x00ff00)
                    embed.set_author(name='Insomnia Community Bot',
                                     icon_url=links['insomnia_avatar'])
                    if WinRate == 0:
                        cursor.execute(f'UPDATE users SET money={int(row[0]) - bet} where id=?', (ctx.author.id,))
                        embed.add_field(name='Проигрыш',
                                        value=f'Сегодня удача не на вашей стороне. С вашего счета было списано '
                                              f'{bet} SH')
                    else:
                        cursor.execute(f'UPDATE users SET money={int(row[0]) - bet * 0.5} where id=?', (ctx.author.id,))
                        embed.add_field(name='Проигрыш',
                                        value=f'Сегодня удача не на вашей стороне. С вашего счета было списано '
                                              f'{bet} SH')
                await ctx.send(embed=embed, file=File('result.gif'))
                data_base.commit()
    except Exception as E:
        print('Casino command error:', E)


# Similar commands below
@bot.command()
async def help(ctx):
    message = await ctx.send(embed=help_embed_func(ctx)[0])
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=help_embed_func(ctx))
    await page.start()


@bot.command()
async def zones(ctx):
    await zones_embed_func(ctx)


@bot.command()
@commands.has_permissions(administrator=True)
async def rules_for_channel(ctx):
    await ctx.message.delete()
    await rules_for_channel_embed_func(ctx)


@bot.command()
async def meme(ctx):
    try:
        await ctx.message.delete()
        res = requests.get('https://meme-api.herokuapp.com/gimme').json()
        embed = discord.Embed(color=0xff9900, title=res['title'])
        embed.set_author(name=f"Автор: {res['author']}   Очки: {res['ups']}")
        embed.set_image(url=f"{res['url']}")
        embed.set_footer(text='P.S мемы на английском потому что с Reddit\'a ')
        await ctx.send(embed=embed)
    except Exception as E:
        print(f'Meme command Error: {E}')
        embed = discord.Embed(color=0xff0000, title='Мемчики не отвечают (')


@bot.command()
async def stuff(ctx):
    await stuff_embed_func(ctx)


@bot.command()
async def rules(ctx):
    message = await ctx.send(embed=rules_embed_func(ctx)[0])
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=rules_embed_func(ctx))
    await page.start()


bot.run(settings['token'])
