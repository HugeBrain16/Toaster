import discord; from discord.ext import commands;
import os, iniparser2, traceback, sys

class AutoMessage(commands.Cog):
	def __init__(self, client):
		self.client = client

	# https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
		    return
		cog = ctx.cog
		if cog:
		    if cog._get_overridden_method(cog.cog_command_error) is not None:
		        return
		ignored = (commands.CommandNotFound, )
		error = getattr(error, 'original', error)
		if isinstance(error, ignored):
		    return
		if isinstance(error, commands.DisabledCommand):
		    await ctx.send(f'{ctx.command} has been disabled.')
		elif isinstance(error, commands.NoPrivateMessage):
		    try:
		        await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
		    except discord.HTTPException:
		        pass
		elif isinstance(error, commands.BadArgument):
		    if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
		        await ctx.send('I could not find that member. Please try again.')
		else:
		    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	
	@commands.command()
	async def addmsg(self, ctx, message, out):
		if not ctx.message.author.guild_permissions.administrator: await ctx.send('you don\'t have a permission to use this command!'); return
		if len(message) < 3: await ctx.send('message is too short! (min 3 char)'); return
		_msg = iniparser2.INI('servers/message.ini').read()

		if message not in _msg[str(ctx.guild.id)]:
			_msg[str(ctx.guild.id)].update({message: out})
		else:
			_msg[str(ctx.guild.id)][message] = out

		iniparser2.INI('servers/message.ini').write(_msg); await ctx.send('new auto message has been set!')

	@commands.command()
	async def delmsg(self,ctx,message):
		if not ctx.message.author.guild_permissions.administrator: await ctx.send('you don\'t have a permission to use this command!'); return
		_msg = iniparser2.INI('servers/message.ini').read()

		if message not in _msg[str(ctx.guild.id)]: await ctx.send('message not found!'); return
		else:
			del _msg[str(ctx.guild.id)][message]

		iniparser2.INI('servers/message.ini').write(_msg); await ctx.send('message deleted!')

	@addmsg.error
	async def addmsg_error(self,ctx,error):
		if isinstance(error, commands.MissingRequiredArgument):
			if error.param.name == 'message': await ctx.send('you need to provide the message!')
			elif error.param.name == 'out': await ctx.send('you need to provide the message output!')

	@delmsg.error
	async def delmsg_error(self,ctx,error):
		if isinstance(error, commands.MissingRequiredArgument):
			if error.param.name == 'message': await ctx.send('you need to provide the message!')

def setup(client):
	client.add_cog(AutoMessage(client))