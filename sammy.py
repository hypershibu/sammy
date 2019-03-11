#!/usr/bin/env python3.7
import discord
import asyncio

TOKEN = ''

client = discord.Client()


# background task definition that gets enabled by client.loo.create_task()
async def autobumper():
	await client.wait_until_ready()
	# write channel ID to send "bump" message every 2 hours (7200 seconds)
	channel = discord.Object(id='')
	while not client.is_closed:
		await client.send_message(channel, 'bump')
		print('bumped')
		await asyncio.sleep(7200)


# react to message content
@client.event
@asyncio.coroutine
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


# Initialization commands
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')


# creates a task in the background
client.loop.create_task(autobumper())

client.run(TOKEN)
