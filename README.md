
# SysBot.py
[![License](https://img.shields.io/badge/license-GNU%20Affero%20General%20Public%20License%20Version%203%20or%20Later-blue.svg)]()

A sys-botbase client for remote control automation of Nintendo Switch consoles. Based on SysBot.NET, written in python. 

## Setup:
1. Download the repo
2. Make a discord bot
3. Download sys-botbase on your switch
4. Fill out the config.yaml
5. Install dependencies
6. py sysbot.py

## Should I use this bot?
If you want to use this for SysBot:

	No. It barely works, I did it for fun. Use [SysBot.NET](https://github.com/kwsch/SysBot.NET) instead.
	- There is no legality checks and there is no pkx or pbx conversion. 
	- I did not implement anything with offsets other than b1s1.
	- This was more for fun. Use the other bot for actual SysBot use.
    
If you want to use this for other features:

	I personally use it along side SysBot.NET.
	It has some nice features, especially if the bot is used in multiple servers.

## Something doesn't work correctly:
Not everything is tested and I doubt everything will work as expected.
- If you want to open an issue then I might take a look at it. If you want to fork and fix then I could always pull as well.

## Support:
Ask nicely and I might have an answer
[<img src="https://canary.discordapp.com/api/guilds/771539948687589386/widget.png?style=banner2">](https://discord.gg/TwyCFr5WDY)

## Future goals:
Feel free to fork and do the stuff I couldn't.

### Touchscreen input:
- [ ] More accurate trade code input
### CoreApi
- [ ] Encryption and Decryption
- [ ] Legality Checks
### Screen capture
- [ ] Fix pixelPeek
### Offset Checks
- [ ] Make it more stable

## Credits:
- [olliz0r's sys-botbase](https://github.com/olliz0r/sys-botbase): Switch automation and pokemon injection
- [kwsch](https://github.com/kwsch/SysBot.NET): Offsets needed for b1s1
- [Manu098vm](https://github.com/Manu098vm): Teaching me how to use offsets correctly
- [GriffinG1](https://github.com/GriffinG1/FlagBot): Stole some stuff from Flagbot like the error handler and how he did legality checks
- Santa, Bewears, Bones: Giving me ideas and fixing errors

## License:
[AGPLv3+](https://www.gnu.org/licenses/agpl-3.0.en.html)

This is free software, and you are welcome to redistribute it under certain conditions.

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


For more details on this issue, check the [COPYING](COPYING) file.
