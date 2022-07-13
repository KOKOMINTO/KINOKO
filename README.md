# Kinoko
A lightweight reaction role Discord bot using slash commands, meant to be a multi-purpose bot in the future. You can also use it as a base for your own!

Hosted by the awesome [@Annwan](https://github.com/Annwan)

**Current available commands:**
- /setreactionrole (message)(channel)(reaction)(role)

**Compilation:**
- Rename template.env as just .env and replace the token inside by a valid one
- Create the database (```sqlite3 Kinoko.db``` ,which can be used )
- Run the sql script (```.read directory/of/source_code/init.sql```)
- Run ```python3 main.py```

**Dependencies:**
- python3
- discord.py 
- discord-ext-slash
- python-dotenv
- sqlite

**Roadmap:**
- [x] Add ability to set reaction roles with both default and custom emojis  
- [x] Replace the use of discord-py-slash with discord-ext-slash 
- [x] Replace the current .json save system with a SQL database
- [ ] Add ability to set one-time reminders
- [ ] Add ability to set repeated reminders
- [ ] Add ability to set automatic welcoming and leaving messages for your server
