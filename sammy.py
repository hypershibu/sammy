#!/usr/bin/env python3.5
import discord
import asyncio
import datetime
import logging

TOKEN = ''

# list of memos as a global variable
memo_list = []

client = discord.Client()

# basic logging set-up
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# background task definition that gets enabled by client.loo.create_task()
async def autobumper():
	await client.wait_until_ready()
	# write channel ID to send "bump" message every t_seconds seconds (20 in example)
	channel = discord.Object(id='')
	t_seconds = 20
	while not client.is_closed:
		await client.send_message(channel, 'bump')
		print('bumped')
		await asyncio.sleep(t_seconds)


# background task for handling memos 
async def memo_handler():
	await client.wait_until_login()
	print(datetime.datetime.now())
	while not client.is_closed:
		for memo in memo_list:
			now = datetime.datetime.now().timestamp()
			if memo[2] < now:
				msg = memo[0] + ' (memo) ' + memo[3]
				await client.send_message(memo[1], msg)
				memo_list.remove(memo)
		await asyncio.sleep(10)


# react to message content
@client.event
async def on_message(message):
	# so the bot doesn't react on itself
	if message.author == client.user:
		return

	# Test command/template for all the commands
	# that end up with automatic text reply
	if message.content.startswith("!top_kek"):
		msg = 'Toppest of keks'
		await client.send_message(message.channel, msg)

	# Template for responding to all messages that include given string(s)
	pankek = message.content.lower()
	if 'naleśni' in pankek or 'nalesni' in pankek:
		print(message.content)
		msg = '(smacznego)'
		await client.send_message(message.channel, msg)

	# command that sends memo to memo_list, that gets handled by memo_handler()
	if message.content.startswith('!memo '):
		try:
			msg_input = message.content.split(maxsplit=3)
			msg_input.remove('!memo')
			msg_datetime = msg_input[0] + ' ' + msg_input[1]
			memo_epoch = datetime.datetime.strptime(msg_datetime, '%Y-%m-%d %H:%M').timestamp()
			msg_memo = msg_input[2]
			msg = message.author.mention + ' (memo) ' + msg_memo
			memo = [message.author.mention, message.channel, memo_epoch, msg_memo]
			memo_list.append(memo)
		except Exception as e:
			msg = message.author.mention + ' error! Expected format is:\n!memo YYYY-MM-DD HH:MM memo_content\nWhere "memo_content" is your memo'
			await client.send_message(message.channel, msg)
			raise e


	# write all your pending memos and remove them from queue
	if message.content.startswith('!memo_get'):
		for memo in memo_list:
			if memo[0] == message.author.mention:
				msg = msg = memo[0] + ' (memo) ' + memo[3]
				memo_list.remove(memo)
				await client.send_message(message.channel, msg)


# Initialization commands
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')


# creates a task in the background
# client.loop.create_task(autobumper())

# creates a memo_handler() task in the background
client.loop.create_task(memo_handler())

client.run(TOKEN)
