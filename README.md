# Kinoko
A lightweight multi-purpose Discord bot, feel free to use this code for your own bot!

Hosted by the awesome [@Annwan](https://github.com/Annwan)

**Current available commands:**
- /setreactionrole (message)(channel)(reaction)(role) 
- /setreminder (channel)(content)(time)(repeat)
- /welcomeset (channel)(message)
- /goodbyeset (channel)(message)
- /goodbyeunset
- /welcomeunset
- /ping 

**Compilation:**
- Rename template.env as just .env and replace the token inside by a valid one
- Create the database (```sqlite3 Kinoko.db```)
- Run the sql script (```.read directory/of/source_code/init.sql``` while in a sqlite3 prompt)
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
- [x] Add ability to set one-time reminders 
- [X] Add ability to set repeated reminders
- [X] Add ability to set automatic welcoming and leaving messages for your server
- [ ] Make reminders compatible with all timezones
- [ ] Add ability to cancel reminders
- [X] Add ability to unset welcoming and leaving messages
