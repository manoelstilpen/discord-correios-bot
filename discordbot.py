import discord
import asyncio
from discord.ext import commands
from correios_status import CorreiosStatus


# handler = DiscordHandler()
bot = commands.Bot(command_prefix='!', description='Edmilson, the mailman')
tasks_list = []


def find_dict(user, dict):

    for d in dict:
        if d['info']['user'] == user:
            return d

    return None


async def check_status(info):
    await bot.wait_until_ready()

    status = info['status']

    msg = '{0} fique tranquilo, estou monitorando sua entrega. Avisarei qualquer alteração!'.format(info['user'].mention)
    await bot.send_message(info['channel'], msg)

    while not bot.is_closed:
        if status.had_change():
            await bot.send_message(info['channel'], "Olá " + info['user'].mention + ", houve uma alteração no status da sua entrega:"
                                   + "\n\n`" + status.atual_status() + "`"
                                   + "\n<" + status.link() + ">")

        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print('------')


@bot.command(pass_context=True)
async def status(ctx: discord.ext.commands.Context):
    stats = find_dict(ctx.message.author, tasks_list)

    if stats is None:
        await bot.say(ctx.message.author.mention + " não existe uma encomenda cadastrada com seu nome")
        return

    info = stats['info']
    status = info['status'].atual_status()
    date = info['status'].atual_date()
    await bot.send_message(info['channel'], info['user'].mention + " a ultima atualização da sua encomenda foi feita em: " + date
                                            + " e o estado atual é:"
                                            + "\n\n`" + status + "`")


@bot.command(pass_context=True)
async def rastreio(ctx: discord.ext.commands.Context):
    # print(ctx.message.author.name, ctx.message.author.id)

    message: str = ctx.message.content.replace('!rastreio ', '')
    info = {'code': message,
            'channel': ctx.message.channel,
            'user': ctx.message.author,
            'status': CorreiosStatus(message)}

    if ' ' in message:
        await bot.say(info['user'].mention + ' coloque na mensagem apenas o código de rastreio')

    else:
        task = bot.loop.create_task(check_status(info))
        tasks_list.append({'info': info, 'task': task})


@bot.command(pass_context=True)
async def repete(ctx: discord.ext.commands.Context):
    await bot.say(ctx.message.content.replace('!repete', ''))


if __name__ == '__main__':
    # bot.loop.create_task(check_status({'code': 'LS816758501CH', 'user': '<@415006523933065236>', 'status': None}))
    # bot.loop.create_task(check_status())
    bot.run('token')
