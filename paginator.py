import discord
import asyncio
from discord.ext import commands

class Paginator:
	''' This is a project i'm working on and which is still in developement.'''
	def __init__(self,context,mapping,per_page=9):
		self.context = context
		self.mapping = mapping
		self.per_page = per_page
		self.reactions = ['◀️','⏹','▶️']
		self.embed = discord.Embed(color = discord.Color.blue())
		self.page = 1
		self.msg_sent = False
		self.max_pages = 0
		
	def get_page(self, page_num):
		pages = {}
		mapping_list= list(self.mapping.items())
		page_index = count=0
		for index, page in enumerate(mapping_list, start =1):
			count +=1
			if count == self.per_page or index == len(mapping_list):
				page_index+=1 
				dict[page_index]= mapping_list[index-y: index]
				count =0
			self.max_pages = len(pages)
		return pages.get(page_num)
	
	async def prepare_page(self):
		if not self.msg_sent:
			self.msg_sent = True
			self.message = await self.context.send(embed = self.embed)
			if self.max_pages >1:
				await self.react()
		else:
			await self.message.edit(embed = self.embed)
			
	async def start(self):
		return await self.prepare_page()
	# Next Page	
	async def next_page(self):
		self.embed.clear_fields()
		if self.page == self.max_pages:
			return await self.prepare_page()
		self.page += 1 
		return await self.prepare_page()
		
	# Previous page
	async def previous_page(self):
		self.embed.clear_fields()
		self.page -=1
		return await self.prepare_page()

	# The reactions
	async def react(self):
		for reaction in self.reactions:
			await asyncio.sleep(1)
			await self.message.add_reaction(reaction)
		while self.msg_sent:
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

class ListPaginator(Paginator):
	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
	def get_page(self, page_num):
		pages= {}
		page_index =counter=0
		for  key,values in self.mapping.items():
			for index,x in enumerate(values, start=1):
				counter +=1
				if counter == self.per_page or index == len(values):
					page_index+=1 
					pages[page_index]= values[index-counter:index]
					counter =0
		self.max_pages = len(pages)
		return pages.get(page_num)