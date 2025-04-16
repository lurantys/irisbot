import discord
from discord.ext import commands
from discord.ui import View, Button  # Add imports for UI components
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an instance of a bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Create a tree for slash commands
tree = bot.tree

# Event: When the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Luck Games"))
    print(f'We have logged in as {bot.user}')
    try:
        await tree.sync()  # Sync slash commands with Discord
        print("Slash commands synced successfully.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Slash Command: Lookup a Pokémon by name or ID
@tree.command(name="lookup_pokemon", description="Lookup a Pokémon by name or ID")
@discord.app_commands.describe(pokemon="Name or ID of the Pokémon")
async def lookup_pokemon(interaction: discord.Interaction, pokemon: str):
    import requests
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        id = data['id']
        height = data['height'] / 10  # Convert decimeters to meters
        weight = data['weight'] / 10  # Convert hectograms to kilograms
        base_experience = data['base_experience']
        abilities = [a['ability']['name'].capitalize() for a in data['abilities']]
        abilities_str = ", ".join(abilities)
        types = [t['type']['name'].capitalize() for t in data['types']]
        types_str = ", ".join(types)
        sprite_url = data['sprites']['front_default']
        
        embed = discord.Embed(
            title=f"Pokémon: {name}",
            description=(
                f"ID: {id}\n"
                f"Types: {types_str}\n"
                f"Height: {height} m\n"
                f"Weight: {weight} kg\n"
                f"Base Experience: {base_experience}\n"
                f"Abilities: {abilities_str}"
            ),
            color=discord.Color.blue()
        )
        
        if sprite_url:
            embed.set_thumbnail(url=sprite_url)
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Pokémon not found. Please check the name or ID.")
@tree.command(name="shiny_lookup", description="Lookup a shiny Pokémon by name or ID")
@discord.app_commands.describe(pokemon="Name or ID of the Pokémon")
async def shiny_lookup(interaction: discord.Interaction, pokemon: str):
    import requests
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        id = data['id']
        shiny_sprite_url = data['sprites']['front_shiny']
        
        if shiny_sprite_url:
            embed = discord.Embed(
                title=f"{name} (Shiny)",
                color=discord.Color.gold()
            )
            embed.set_image(url=shiny_sprite_url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Shiny sprite not available for this Pokémon.")
    else:
        await interaction.response.send_message("Pokémon not found. Please check the name or ID.")

# Slash Command: Get a random Pokémon
@tree.command(name="random_pokemon", description="Get information about a random Pokémon")
async def random_pokemon(interaction: discord.Interaction):
    import requests
    import random
    
    # There are currently over 1000 Pokémon, but let's limit to the first 1000 to be safe
    random_id = random.randint(1, 1000)
    
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        id = data['id']
        height = data['height'] / 10  # Convert decimeters to meters
        weight = data['weight'] / 10  # Convert hectograms to kilograms
        base_experience = data['base_experience']
        abilities = [a['ability']['name'].capitalize() for a in data['abilities']]
        abilities_str = ", ".join(abilities)
        types = [t['type']['name'].capitalize() for t in data['types']]
        types_str = ", ".join(types)
        sprite_url = data['sprites']['front_default']
        
        embed = discord.Embed(
            title=f"Random Pokémon: {name}",
            description=(
                f"ID: {id}\n"
                f"Types: {types_str}\n"
                f"Height: {height} m\n"
                f"Weight: {weight} kg\n"
                f"Base Experience: {base_experience}\n"
                f"Abilities: {abilities_str}"
            ),
            color=discord.Color.green()
        )
        
        if sprite_url:
            embed.set_thumbnail(url=sprite_url)
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Failed to fetch a random Pokémon. Please try again.")

# Slash Command: Calculate type effectiveness
@tree.command(name="type_matchup", description="Get Pokémon type effectiveness information")
@discord.app_commands.describe(pokemon_type="The Pokémon type to check effectiveness for")
async def type_matchup(interaction: discord.Interaction, pokemon_type: str):
    import requests
    
    # Normalize the type name
    pokemon_type = pokemon_type.lower()
    
    # Valid Pokémon types
    valid_types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", 
                  "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
    
    if pokemon_type not in valid_types:
        await interaction.response.send_message(f"Invalid type. Please choose from: {', '.join(valid_types).title()}")
        return
    
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Get damage relations
        damage_relations = data['damage_relations']
        
        # Extract effectiveness data
        no_damage_to = [t['name'].capitalize() for t in damage_relations['no_damage_to']]
        half_damage_to = [t['name'].capitalize() for t in damage_relations['half_damage_to']]
        double_damage_to = [t['name'].capitalize() for t in damage_relations['double_damage_to']]
        
        no_damage_from = [t['name'].capitalize() for t in damage_relations['no_damage_from']]
        half_damage_from = [t['name'].capitalize() for t in damage_relations['half_damage_from']]
        double_damage_from = [t['name'].capitalize() for t in damage_relations['double_damage_from']]
        
        # Create embed
        embed = discord.Embed(
            title=f"Type Matchup: {pokemon_type.capitalize()}",
            color=discord.Color.purple()
        )
        
        # Attacking effectiveness
        embed.add_field(
            name="When Attacking",
            value=(
                f"**Super Effective Against**: {', '.join(double_damage_to) if double_damage_to else 'None'}\n"
                f"**Not Very Effective Against**: {', '.join(half_damage_to) if half_damage_to else 'None'}\n"
                f"**No Effect Against**: {', '.join(no_damage_to) if no_damage_to else 'None'}"
            ),
            inline=False
        )
        
        # Defending effectiveness
        embed.add_field(
            name="When Defending",
            value=(
                f"**Weak To**: {', '.join(double_damage_from) if double_damage_from else 'None'}\n"
                f"**Resistant To**: {', '.join(half_damage_from) if half_damage_from else 'None'}\n"
                f"**Immune To**: {', '.join(no_damage_from) if no_damage_from else 'None'}"
            ),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Failed to get type information. Please try again.")

# Slash Command: Who's that Pokémon? game
@tree.command(name="whos_that_pokemon", description="Play a game of Who's That Pokémon?")
async def whos_that_pokemon(interaction: discord.Interaction):
    import requests
    import random
    import io
    from PIL import Image, ImageFilter, ImageEnhance
    
    # Prevent multiple games in the same channel
    channel_id = interaction.channel_id
    if channel_id in pokemon_games:
        await interaction.response.send_message("There's already an active Who's That Pokémon game in this channel!", ephemeral=True)
        return
    
    # Defer the response to prevent interaction timeout
    await interaction.response.defer()
    
    # Get a random Pokémon (from the first 905 for better recognition)
    random_id = random.randint(1, 905)
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        name = data['name'].capitalize()
        sprite_url = data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default']
        
        if not sprite_url:
            await interaction.followup.send("Failed to get Pokémon image. Please try again.")
            return
        
        # Get the image
        img_response = requests.get(sprite_url)
        img = Image.open(io.BytesIO(img_response.content))
        
        # Create silhouette
        silhouette = img.convert("RGBA")
        width, height = silhouette.size
        
        # Make all non-transparent pixels black
        for x in range(width):
            for y in range(height):
                pixel = silhouette.getpixel((x, y))
                if pixel[3] != 0:  # If not transparent
                    silhouette.putpixel((x, y), (0, 0, 0, 255))  # Black
        
        # Save to buffer
        buffer = io.BytesIO()
        silhouette.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Create the embed
        embed = discord.Embed(
            title="Who's that Pokémon?",
            description="Click the button below to guess the Pokémon based on its silhouette!",
            color=discord.Color.orange()
        )
        
        file = discord.File(buffer, filename="silhouette.png")
        embed.set_image(url="attachment://silhouette.png")
        
        # Create the view with the guess button
        view = PokemonGuessView(name, sprite_url, file)
        
        # Send the message with the button
        message = await interaction.followup.send(embed=embed, file=file, view=view)
        
        # Store the game in our active games dictionary
        pokemon_games[channel_id] = {"name": name, "message_id": message.id}
        
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# Slash Command: Generate a random Pokemon team
@tree.command(name="generate_team", description="Generate a random balanced Pokemon team")
async def generate_team(interaction: discord.Interaction):
    import requests
    import random
    
    await interaction.response.defer()
    
    # List of Pokemon types for balancing
    types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
            "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
    
    # To ensure type diversity, we'll track types we've already included
    used_types = set()
    team = []
    team_sprites = []
    
    try:
        # Get all Pokemon count (adjusted based on what's reliably available in the API)
        # We'll use the first 898 Pokemon (up to Gen 8) for better reliability
        max_pokemon_id = 898
        
        # Generate 6 Pokemon for the team
        for _ in range(6):
            attempts = 0
            pokemon_data = None
            
            # Try to find a Pokemon with new types (but don't try too hard to avoid infinite loops)
            while attempts < 10:
                random_id = random.randint(1, max_pokemon_id)
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    pokemon_types = [t['type']['name'] for t in data['types']]
                    
                    # If we have less than 4 Pokemon, prioritize new types
                    if len(team) < 4:
                        if all(t in used_types for t in pokemon_types):
                            attempts += 1
                            continue
                    
                    # Add this Pokemon's types to our used types
                    for t in pokemon_types:
                        used_types.add(t)
                    
                    pokemon_data = data
                    break
                
                attempts += 1
            
            if pokemon_data:
                # Extract needed information
                name = pokemon_data['name'].capitalize()
                pokemon_types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
                sprite_url = pokemon_data['sprites']['front_default']
                
                # Add to our team
                team.append({
                    'name': name,
                    'types': pokemon_types,
                    'sprite_url': sprite_url
                })
                
                if sprite_url:
                    team_sprites.append(sprite_url)
        
        # Create the embed
        embed = discord.Embed(
            title="Your Random Pokémon Team",
            description="Here's a balanced team of 6 Pokémon for your adventure!",
            color=discord.Color.red()
        )
        
        # Add each Pokemon to the embed
        for i, pokemon in enumerate(team, 1):
            type_str = ", ".join(pokemon['types'])
            embed.add_field(
                name=f"{i}. {pokemon['name']}",
                value=f"Types: {type_str}",
                inline=True
            )
        
        # Add a note about type coverage
        covered_types = len(used_types)
        type_coverage = round((covered_types / len(types)) * 100)
        embed.set_footer(text=f"Type Coverage: {covered_types}/{len(types)} ({type_coverage}%)")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"Failed to generate a team: {str(e)}")

# Slash Command: Lookup a Pokemon move
@tree.command(name="move_info", description="Get details about a Pokemon move")
@discord.app_commands.describe(move="Name of the Pokemon move to look up")
async def move_info(interaction: discord.Interaction, move: str):
    import requests
    
    # Format the move name correctly for the API
    move_formatted = move.lower().replace(" ", "-")
    
    url = f"https://pokeapi.co/api/v2/move/{move_formatted}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract move details
        name = data['name'].replace("-", " ").title()
        move_type = data['type']['name'].capitalize()
        power = data['power'] if data['power'] is not None else "N/A"
        accuracy = f"{data['accuracy']}%" if data['accuracy'] is not None else "N/A"
        pp = data['pp']
        damage_class = data['damage_class']['name'].capitalize() if 'damage_class' in data and data['damage_class'] else "N/A"
        
        # Get effect text
        effect_text = "No effect description available."
        if 'effect_entries' in data and data['effect_entries']:
            for entry in data['effect_entries']:
                if entry['language']['name'] == 'en':
                    effect_text = entry['effect']
                    break
        
        # Create embed
        embed = discord.Embed(
            title=f"Move: {name}",
            description=effect_text,
            color=discord.Color.teal()
        )
        
        # Add move stats
        embed.add_field(name="Type", value=move_type, inline=True)
        embed.add_field(name="Category", value=damage_class, inline=True)
        embed.add_field(name="PP", value=pp, inline=True)
        embed.add_field(name="Power", value=power, inline=True)
        embed.add_field(name="Accuracy", value=accuracy, inline=True)
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"Move '{move}' not found. Please check the spelling.")

# Event: Check guesses for Who's That Pokémon
@bot.event
async def on_message(message):
    # Don't respond to bot messages
    if message.author.bot:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Check if we have an active Who's That Pokémon game
    global current_pokemon_answer
    if current_pokemon_answer:  # Just check if the variable is set
        guess = message.content.lower()
        
        # Compare the guess to the answer
        if guess == current_pokemon_answer:
            # Correct guess
            embed = discord.Embed(
                title="Correct!",
                description=f"Congratulations {message.author.mention}! The Pokémon was **{current_pokemon_answer.capitalize()}**!",
                color=discord.Color.green()
            )
            try:
                await message.channel.send(embed=embed)
            except discord.errors.Forbidden:
                print(f"Missing permissions to send messages in channel {message.channel.name} (ID: {message.channel.id})")
                # Log this issue but continue execution
                pass
            except Exception as e:
                print(f"Error responding to correct guess: {str(e)}")
            finally:
                # Reset the game regardless of whether the message was sent
                current_pokemon_answer = None
        
        # Note: We don't respond to incorrect guesses to reduce spam

# Initialize the current_pokemon_answer global variable
current_pokemon_answer = None

# Additional global variables to track active games
pokemon_games = {}  # Dictionary to track active games by channel ID

# Custom View class for the Who's That Pokemon game
class PokemonGuessView(View):
    def __init__(self, pokemon_name, sprite_url, silhouette_file):
        super().__init__(timeout=120)  # The view will timeout after 2 minutes
        self.pokemon_name = pokemon_name
        self.sprite_url = sprite_url
        self.silhouette_file = silhouette_file
        self.guessed = False
        self.guesser = None
        
    @discord.ui.button(label="Guess!", style=discord.ButtonStyle.primary)
    async def guess_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Create a modal for the user to enter their guess
        modal = PokemonGuessModal(self.pokemon_name, self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Skip the current Pokémon
        await self.skip_pokemon(interaction)
    
    async def reveal_pokemon(self, interaction, user):
        self.guessed = True
        self.guesser = user
        
        # Create a new embed with the reveal
        embed = discord.Embed(
            title="Correct!",
            description=f"{user.mention} guessed it! The Pokémon was **{self.pokemon_name}**!",
            color=discord.Color.green()
        )
        
        # Use the original sprite URL for the reveal
        embed.set_image(url=self.sprite_url)
        
        # Disable all buttons after a correct guess
        for item in self.children:
            item.disabled = True
        
        # Update the message with the new embed
        await interaction.response.edit_message(embed=embed, view=self)
        
        # Remove this game from the active games
        if interaction.channel_id in pokemon_games:
            del pokemon_games[interaction.channel_id]
            
    async def skip_pokemon(self, interaction):
        # Create a new embed showing what Pokémon was skipped
        embed = discord.Embed(
            title="Pokémon Skipped",
            description=f"The Pokémon was **{self.pokemon_name}**!",
            color=discord.Color.yellow()  # Yellow color to differentiate from correct guesses
        )
        
        # Use the original sprite URL for the reveal
        embed.set_image(url=self.sprite_url)
        
        # Disable all buttons after skipping
        for item in self.children:
            item.disabled = True
        
        # Update the message
        await interaction.response.edit_message(embed=embed, view=self)
        
        # Remove this game from the active games
        if interaction.channel_id in pokemon_games:
            del pokemon_games[interaction.channel_id]

class PokemonGuessModal(discord.ui.Modal, title="Who's That Pokémon?"):
    def __init__(self, pokemon_name, view):
        super().__init__()
        self.pokemon_name = pokemon_name.lower()
        self.view = view
        
    # Add a text input field for the guess
    guess = discord.ui.TextInput(
        label="Enter your guess:",
        placeholder="Pokemon name...",
        required=True,
        max_length=50
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        user_guess = self.guess.value.lower().strip()
        
        if user_guess == self.pokemon_name.lower():
            # Correct guess - reveal the pokemon
            await self.view.reveal_pokemon(interaction, interaction.user)
        else:
            # Wrong guess - inform the user privately
            await interaction.response.send_message(
                f"Sorry, '{self.guess.value}' is not correct. Try again!", 
                ephemeral=True  # Only the guesser can see this message
            )

# Store the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("The bot token is not set. Please set the DISCORD_TOKEN environment variable.")

# Run the bot
bot.run(TOKEN)
