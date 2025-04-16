# Iris - Discord Pokémon Assistant

<div align="center">

![Pikachu Sprite](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png)

</div>

## About

Iris is a feature-rich Discord bot that brings the world of Pokémon to your server! With commands for looking up Pokémon information, playing games, and more, it's the perfect companion for any Pokémon fan community.

## Features

- 🔍 **Pokémon Lookup** - Get detailed information about any Pokémon by name or ID
- ✨ **Shiny Pokémon** - View the shiny version of any Pokémon
- 🎲 **Random Pokémon** - Discover a random Pokémon from the Pokédex
- ⚔️ **Type Matchups** - Check the strengths and weaknesses of different Pokémon types
- 🎮 **Who's That Pokémon?** - Play the classic guessing game with your friends
- 👥 **Team Generator** - Generate a balanced team of 6 random Pokémon
- 📚 **Move Information** - Look up details about any Pokémon move

## Commands

- `/lookup_pokemon [name/id]` - Look up information about a specific Pokémon
- `/shiny_lookup [name/id]` - View the shiny version of a Pokémon
- `/random_pokemon` - Get information about a randomly selected Pokémon
- `/type_matchup [type]` - Check effectiveness information for a Pokémon type
- `/whos_that_pokemon` - Start a game of "Who's That Pokémon?"
- `/generate_team` - Create a random, balanced team of 6 Pokémon
- `/move_info [move]` - Get detailed information about a Pokémon move

## Setup

1. Clone this repository
2. Install required dependencies: `pip install discord.py requests pillow`
3. Replace `YOUR BOT TOKEN` in the code with your actual Discord bot token
4. Run the bot: `python test.py`

## Creating a Discord Bot

To use this code, you'll need to create a Discord bot application:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" tab and add a bot
4. Enable the necessary Intents (Message Content, Server Members, etc.)
5. Copy your token and add it to the code (replace `YOUR BOT TOKEN`)
6. Use the OAuth2 URL Generator to invite the bot to your server

## Contributing

Feel free to fork this repository and submit pull requests to contribute new features or bug fixes!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Pokémon data provided by [PokéAPI](https://pokeapi.co/)
- Pokémon is © Nintendo, Game Freak, and The Pokémon Company
