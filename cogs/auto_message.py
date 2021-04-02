import discord; from discord.ext import commands;
import os, iniparser2, traceback, sys

class AutoMessage(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def addmsg(self, ctx, message, out):
		if not ctx.message.author.guild_permissions.administrator: await ctx.send('you don\'t have a permission to use this command!'); return
		if len(message) < 3: await ctx.send('message is too short! (min 3 char)'); return
		_msg = iniparser2.INI('servers/message.ini').read()

		_msg[str(ctx.guild.id)].update({message: out}); iniparser2.INI('servers/message.ini').write(_msg)

		await ctx.send('new auto message has been set!')

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