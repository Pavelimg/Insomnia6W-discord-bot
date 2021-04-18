import discord
from discord.ext import commands
from config import *
from Cybernator import Paginator
from data_text import rules

r1, r2, r3, r4, r5 = rules[1], rules[2], rules[3], rules[4], rules[5]


def stuff_embed_func(ctx):
    embed = discord.Embed(color=0x08FF00, title='Создатели проекта Insomnia')
    embed.set_author(name='Insomnia Community Bot',
                     icon_url=links['insomnia_avatar'])
    embed.set_image(url=links['insomnia_gif'])
    for x in stuff:
        embed.add_field(name=x[0], value=x[1], inline=False)
    res = ctx.send(embed=embed)
    return res


def rules_embed_func(ctx):
    embed1 = discord.Embed(title='Общее положение', color=0xFF0000)
    embed1.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed1.add_field(name='Страница 1/5', value=r1)
    embed1.set_image(url=links['insomnia_gif'])

    embed2 = discord.Embed(title='Положение об аккаунте', color=0xFF0000)
    embed2.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed2.add_field(name='Страница 2/5', value=r2)
    embed2.set_image(url=links['insomnia_gif'])

    embed3 = discord.Embed(title='Положение Игровых Чатов', color=0xFF0000)
    embed3.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed3.add_field(name='Страница 3/5', value=r3)
    embed3.set_image(url=links['insomnia_gif'])

    embed4 = discord.Embed(title='Положение игрового процесса', color=0xFF0000)
    embed4.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed4.add_field(name='Страница 4/5', value=r4)
    embed4.set_image(url=links['insomnia_gif'])

    embed5 = discord.Embed(title='Привила для сервера Discord', color=0xFF0000)
    embed5.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed5.add_field(name='Страница 5/5', value=r5)
    embed5.set_image(url=links['insomnia_gif'])

    embeds = [embed1, embed2, embed3, embed4, embed5]
    return embeds


def zones_embed_func(ctx):
    embed = discord.Embed(color=0xff9900, title='Схема проекта Insomnia <3')
    embed.set_author(name='Insomnia Community Bot',
                     icon_url=links['insomnia_avatar'])
    embed.set_image(
        url=links['zones'])
    res = ctx.send(embed=embed)
    return res


def help_embed_func(ctx):
    embed = discord.Embed(color=0x08FF00, title='Список команд бота Insomnia',
                          description='P.S Здесь могут быть не все команды')
    embed.set_author(name='Insomnia Community Bot',
                     icon_url=links['insomnia_avatar'])
    embed.set_image(url=links['insomnia_gif'])
    for i in help_embed_1:
        embed.add_field(name=i[0], value=i[1], inline=False)
    embed2 = discord.Embed(color=0x08FF00, title='Список команд для Администрации',
                           description='P.S Здесь могут быть не все команды')
    embed2.set_author(name='Insomnia Community Bot',
                      icon_url=links['insomnia_avatar'])
    embed2.set_image(url=links['insomnia_gif'])
    for x in help_embed_2:
        embed2.add_field(name=x[0], value=x[1], inline=False)
    res = [embed, embed2]
    return res


def rules_for_channel_embed_func(ctx):
    try:
        embed = discord.Embed(color=0xff9900, title='Общие правила сервера',
                              description='***Правила для Discord сервера начинаются с 5.1***')
        embed.set_thumbnail(url=links['insomnia_gif'])
        embed.set_author(name='**Insomnia Community Bot**',
                         icon_url=links['insomnia_avatar'],
                         url='https://discord.gg/TQwzABez')
        embed.set_footer(text='Пока что это все правила проекта Insomnia <3')
        embed.add_field(name='Общее положение', value=r1, inline=False)
        embed.add_field(name='Положение об аккаунте', value=r2, inline=False)
        embed.add_field(name='Положение Игровых Чатов', value=r3, inline=False)
        embed.add_field(name='Положение игрового процесса', value=r4, inline=False)
        embed.add_field(name='Правила для сервера Discord', value=r5, inline=False)
        res = ctx.send(embed=embed)
        return res
    except Exception as E:
        print(f'rules for channel command error: {E}')