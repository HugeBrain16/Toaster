import discord; from discord.ext import commands
import iniparser2, os

_cfg = iniparser2.INI('config.ini').read() # load config
client = commands.Bot(command_prefix=_cfg['bot']['prefix'])

# load cogs
for cog in os.listdir('./cogs/'):
	if cog.endswith('.py'): client.load_extension('cogs.{}'.format(cog.strip('.py')))

@client.event
async def on_ready():
	print('the bot is ready!')
	print('User: {}'.format(client.user))

@client.event
async def on_guild_join(guild):

	# setup new auto message
	auto_msg_dat = iniparser2.INI('./server/message.ini').read()
	if not str(guild.id) in auto_msg_dat:
		auto_msg_dat.update({str(guild.id): {}})
		iniparser2.INI('./server/messages.ini').write(auto_msg_dat)

@client.event
async def on_guild_remove(guild):

	# delete auto message
	auto_msg_dat = iniparser2.INI('./server/message.ini').read()
	if str(guild.id) in auto_msg_dat:
		del auto_msg_dat[str(guild.id)]
		iniparser2.INI('./server/messages.ini').write(auto_msg_dat)

@client.event
async def on_message(message):

	_msg_trg = iniparser2.INI('./servers/message.ini').read() # get auto messages

	# send auto message
	if str(message.guild.id) in _msg_trg:
		for msg in _msg_trg[str(message.guild.id)]:
			if msg in message.content and not message.author.bot:
				await message.channel.send(_msg_trg[str(message.guild.id)][msg])

	await client.process_commands(message)

# general commands

@client.command()
async def ping(ctx):
	await ctx.send('No')

@client.command()
async def info(ctx):
	_inf = iniparser2.INI('about.ini').read()

	emb = discord.Embed(title='Toaster',description=_inf['program']['description'],color=0xFF0000)
	emb.add_field(name='Program',value=f'Name: **{_inf["program"]["name"]}**\nVersion: `{_inf["program"]["version"]}`\nSource Code: https://github.com/HugeBrain16/Toaster',inline=False)
	emb.add_field(name='Developer',value=f'Name: **{_inf["developer"]["name"]}**\nDiscord: **{_inf["developer"]["discord"]}**\nGithub: {_inf["developer"]["github"]}',inline=False)

	await ctx.send(embed=emb)

@client.command()
async def invite(ctx):
	await ctx.send('https://discord.com/api/oauth2/authorize?client_id=825518085820907520&permissions=8&scope=bot')

client.run(_cfg['bot']['token'])