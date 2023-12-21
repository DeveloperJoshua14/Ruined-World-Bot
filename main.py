#Imports
import discord 
import os 
import dotenv
import json
from discord.ext import tasks, commands
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()

# Set up Discord client
Intents = discord.Intents.default()
Intents.message_content = True
client = discord.Client(intents=Intents) 

custom_rooms = []
custom_rooms_file_path = "custom_rooms.json"

maintenance_manager = [
	493874564590338058, #Developer Joshua
]

last_anythin = datetime.now()

try:
	with open(custom_rooms_file_path, 'r') as json_file:
		a = json.load(json_file)
	maintenance = True
	testing_bot = True
except:
	custom_rooms_file_path = "home/haven/Share/Projects/Bots/Ruined World Server Bot/.Live Version/custom_rooms.json"
	maintenance = False
	testing_bot = False

try:
	with open(custom_rooms_file_path, 'r') as json_file:
		custom_rooms = json.load(json_file)
except json.decoder.JSONDecodeError:
	custom_rooms = []

async def create_Channel(message):
	guild = client.get_guild(1175973620170895491)
	new_channel_id = await guild.create_voice_channel(name=str(message.content[6:]), category=guild.get_channel(message.channel.category_id))
	
	try:
		await message.author.move_to(new_channel_id)
		await message.reply(f"Moved you to the new channel: {new_channel_id.name}")
		custom_rooms.append({'name': new_channel_id.name, 'id': new_channel_id.id})  # Store channel info
		try:
			with open(custom_rooms_file_path, 'w') as json_file:
				json.dump(custom_rooms, json_file, default=lambda o: o.__dict__, indent=4)
		except:
			await message.channel.send(f"<@493874564590338058>, ```def create_Channel``` failed to open *{custom_rooms_file_path}*")
	except:
		await message.reply("You Must join a voice to create a new voice.")
		await new_channel_id.delete()

async def statusChange(type):
	#Sleeping
	if type == 0:
		activity = discord.CustomActivity(name="I am awake")
		await client.change_presence(status=discord.Status.online, activity=activity)
	elif type == 1:
		activity = discord.CustomActivity(name="Sleeping... zZz")
		await client.change_presence(status=discord.Status.idle, activity=activity)
	elif type == 2:
		activity = discord.CustomActivity(name="Maintenance Mode")
		await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
	elif type == 3:
		activity = discord.CustomActivity(name="Goofy Testing")
		await client.change_presence(status=discord.Status.online, activity=activity)

#set the bot to sleeping at night
@tasks.loop(seconds=5) 
async def my_periodic_task():
	
	if testing_bot:
		await statusChange(3)
		return

	if maintenance:
		await statusChange(2)
		return

	if datetime.now().hour >= 22 or datetime.now().hour <= 5:
		if (datetime.now() - last_anythin).seconds >= 15:  #15*60
			await statusChange(1)
			return
	
	await statusChange(0)
	
#Let Console know bot is online
@client.event 
async def on_ready(): 
	print("Logged in as:  \"{0.user}\"".format(client))
	
	await statusChange(0)
	my_periodic_task.start()
	
@client.event
async def on_voice_state_update(member, before, after):

	try:
		channel = client.get_channel(before.channel.id) #gets the channel you want to get the list from
	except:
		return
	
	try:
		with open(custom_rooms_file_path, 'r') as json_file:
			loaded_rooms = json.load(json_file)
	except json.decoder.JSONDecodeError:
		loaded_rooms = []

	if channel.id in [room['id'] for room in loaded_rooms]:
		members = channel.members
		ind = 0

		for i in loaded_rooms:
			if channel.id == i['id']:
				ind = loaded_rooms.index(i)
				break

		memids = []
		for member in members:
			memids.append(member.id)

		if not memids:
			await channel.delete()
			custom_rooms.remove(loaded_rooms[ind])
			with open(custom_rooms_file_path, 'w') as json_file:
				json.dump(custom_rooms, json_file, default=lambda o: o.__dict__, indent=4)
			

#Recivce message
@client.event 
async def on_message(message): 
	global maintenance
	global testing_bot

	admin_role = "1175974553047019550"
	is_admin = False

	for role in message.author.roles:
		if str(role.id) == admin_role:
			is_admin = True

	if testing_bot:
		for manager in maintenance_manager:
			if manager == message.author.id:
				pass
			else:
				return
	
	if maintenance and not testing_bot:
		for manager in maintenance_manager:
			if manager == message.author.id:
				if message.content.lower().startswith("!comeback") and is_admin:
					pass
				else:
					return
			else:
				pass
	
	# Remove bot messages
	if message.author == client.user: 
		global last_anythin
		last_anythin = datetime.now()
		await statusChange(0)
		return
	
	
	channel_ID = message.channel.id

	#Public Commands
	if True:
		#Make Command
		Allowed_Channels = [
			#Hypixel
			1180616386729476117, 
			#Ruined World SMP
			1180897376291008624, 
			#Special Stuff
			1180581157188939886
			]
		if channel_ID in Allowed_Channels:
			if message.content.lower().startswith("!make "):
				await message.reply("Making Channel")
				await create_Channel(message)

		#Ping to start SMP
		if (message.content.lower() == "!smp-start" or message.content.lower() == "!start-smp") and channel_ID == 1180897376291008624:
			await message.channel.send("""Are any <@&1180902537444982844> availabe to start the server? \n
							  Starters, here is the ling: (https://aternos.org/server/)""")

	#Admin ONLY commands
	if is_admin:
		#Say Command
		if message.content.lower().startswith("!say "):
			await message.channel.send(message.content[5:])
		elif message.content.lower().startswith("!gounder") and not testing_bot:
			await message.channel.send("This bot is going into maintenance mode!")
			maintenance = True
		elif message.content.lower().startswith("!comeback") and not testing_bot:
			await message.channel.send("This bot is back from maintenance mode!")
			maintenance = False
		elif message.content.lower().startswith("!vstat"):
			try:
				await message.channel.send(f"{message.content[7:]}: {globals()[message.content[7:]]}")
			except Exception as error:
				await message.channel.send(f"Error! \"{message.content[7:]}\" is not a variable!")

if not maintenance:
	# Run the Discord client
	client.run(os.getenv('TOKEN'))
else:
	client.run(os.getenv('TESTING_TOKEN'))