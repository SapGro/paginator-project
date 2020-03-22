import discord
from discord.ext import commands
import asyncio
class Paginator:
	''' This is a project i'm working on and which is still in developement, it's now specefic for help command formatting. I did it this way so that i can test it. The per_page function is not implemented yet.'''
	def __init__(self, context,mapping ,per_page=9):
		self.context = context
		self.mapping = mapping
		self.per_page = per_page
		self.reactions = ['◀️','⏹','▶️']
		self.embed = discord.Embed(color = discord.Color.blue())
		self.page = 1
		self.msg_sent = False
		self.max_pages = 0
		
	# Courotine to prepare the page
	async def prepare_page(self, page):
		# The dict which is going to hold all the commands and 
		# sort them by their cogs using indexes
		dict = {}
		# The mapping here is the mapping of the cogs of the bot
		for index,(cog, command) in enumerate(self.mapping.items(), start=1):
			# Skip cogs which are None 
			if not cog or cog.qualified_name == 'Erreur':
				continue
			# Store the commands by their cogs in an array
			# The key is the index of each page
			dict[index] = [cog, cog.walk_commands()]
		self.max_pages = len(dict)
		# Get the page which we are looking for
		value = dict.get(self.page)
		self.embed.title = value[0].qualified_name
		self.embed.description = f"Page {self.page}/{self.max_pages}"
		self.embed.set_footer(text = "Fais help <commande> pour en savoir plus sur une commande.", icon_url = self.context.bot.user.avatar_url )
		# Format the embed
		for x in value[1]:
			command_sig = get_command_signature(x)
			self.embed.add_field(name = command_sig, value = x.description if x.description else x.help, inline = False)
		# If the message is not sent yet
		# Then we need to send it
		if not self.msg_sent:
			self.msg_sent = True
			self.message = await self.context.send(embed = self.embed)
			# Start the reactions
			await self.react()
		# If the message is sent, we just need to edit its embed
		else:
			await self.message.edit(embed = self.embed)
	# start the paginator
	async def start(self):
		return await self.prepare_page(1)
	# Next Page	
	async def next_page(self):
		self.embed.clear_fields()
		self.page += 1 
		return await self.prepare_page(self.page)
		
	# Previous page
	async def previous_page(self):
		self.embed.clear_fields()
		self.page -=1
		return await self.prepare_page(self.page)

	# The reactions
	async def react(self):
		for reaction in self.reactions:
			await asyncio.sleep(1)
			await self.message.add_reaction(reaction)
		while True:
			def check(reaction, user):
				if user == self.context.author and reaction.emoji in self.reactions:
					return True
				if user.bot == True:
					return False
			try:
				reaction, user = await self.context.bot.wait_for('reaction_add', timeout = 30.0,check= check)
				if reaction.emoji == self.reactions[0]:
					await self.message.remove_reaction(reaction.emoji, self.context.author)
					await self.previous_page()
				elif reaction.emoji == self.reactions[1]:
					await self.message.clear_reactions()
					break
				elif  reaction.emoji== self.reactions[2]:
					await self.message.remove_reaction(reaction.emoji, self.context.author)
					await self.next_page()
			except asyncio.TimeoutError:
				await self.message.clear_reactions()
				break

