import discord
from discord import app_commands
from discord.ui import Select, View, Button
import random
import time
from colors import Colors



class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Python"))

        print(f"{self.user} has been logged in.")

client = Client()
tree = app_commands.CommandTree(client)


@tree.command(name="hello", description="say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user}!")
    await interaction.followup.send("I'm elon!")


@tree.command(name="bye", description="say goodbye")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Goodbye {interaction.user}!")



@tree.command(name="help", description="show bot info")
async def help(interaction: discord.Interaction):
    info = discord.Embed(title="Elon can:", description="Say hello/goodbye\nPlay Rock Paper Scissors\nBe your calculator\nChange Status", colour=discord.Colour.red())
    info.set_image(url="https://i.pinimg.com/originals/5f/91/f4/5f91f46852965b1e366b526ab8089a06.gif")
    await interaction.response.send_message(content=None, embed=info)


@tree.command(name="average", description="calculate average of numbers")
async def average(interaction: discord.Interaction, values:str):
    values = [float(value) for value in values.split(" ")]
    avg = sum(values) / len(values)
    await interaction.response.send_message(avg)



@tree.command(name="calculate", description="Perform simple math calculations")
async def calculate(interaction: discord.Interaction, num1:int, operation:str, num2:int):

    match(operation):
        case "+": await interaction.response.send_message(num1 + num2)
        case "-": await interaction.response.send_message(num1 - num2)
        case "*": await interaction.response.send_message(num1 * num2)
        case "/": await interaction.response.send_message(num1 / num2)
        case "**": await interaction.response.send_message(num1 ** num2)
        case _: await interaction.response.send_message("Invalid operation")
  


@tree.command(name="random", description="Generates a random number from range")
async def random(interaction: discord.Interaction, num1:int, num2:int):
    await interaction.response.send_message(random.randint(num1, num2))
    


class MyButton(Button):
    def __init__(self, author, id, emoji): # override 
        super().__init__(emoji=emoji) # init parent class
        self.id = id
        self.author = author

    async def callback(self, interaction):

        if(self.author != interaction.user):
            await interaction.response.send_message("Not your game")
            return

        plays = ['rock','paper','scissors']
        user_play = self.id
        bot_play = random.choice(plays)
        plays = [user_play, bot_play]
        winning_plays = [["rock", "scissors"], ["scissors", "paper"], ["paper", "scissors"]]

        if(user_play == bot_play):
            # draw
            await interaction.response.send_message(f"elon played **{bot_play}**... draw!")
        elif(plays in winning_plays):
            #win
            await interaction.response.send_message(f"elon played **{bot_play}**... {interaction.user} wins!")
        else:
            #lose
            await interaction.response.send_message(f"elon played **{bot_play}**... elon wins!")

   




@tree.command(name="rps", description="Rock paper scissors game")
async def rps(interaction: discord.Interaction):

    view = View()
    buttons = [
        MyButton(interaction.user, "rock", emoji="🪨"),
        MyButton(interaction.user, "paper", emoji="📄"),
        MyButton(interaction.user, "scissors", emoji="✂️")
    ]

    for button in buttons:
        view.add_item(button)


    await interaction.response.send_message("Let's play!", view=view, delete_after=60)



   


@tree.command(name="status", description="change bot status")
async def changed_status(interaction: discord.Interaction, status: str):
    status = status.title()

    activities = {
        "Playing": discord.ActivityType.playing,
        "Watching": discord.ActivityType.watching,
        "Listening": discord.ActivityType.listening,
        "Streaming": discord.ActivityType.streaming
    }

    select = Select(
        placeholder = "Select an Activity!",
        min_values = 1,
        max_values = 1,
        options = [discord.SelectOption(label=activity, description=f"Display '{activity} {status}'") for activity in activities.keys()]
    )

    async def changed_status_callback(interaction):
        await client.change_presence(activity=discord.Activity(type=activities[select.values[0]], name=status))

        
    select.callback = changed_status_callback
    view = View()
    view.add_item(select)

    await interaction.response.send_message("Choose an Activity to Display!", view=view, ephemeral=True,delete_after=10)
    


TOKEN = ""
client.run(TOKEN)
