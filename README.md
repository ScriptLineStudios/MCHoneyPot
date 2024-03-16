<p align="center">
  <img align="center" src="https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Bee_with_nectar_%28angry%29.png/revision/latest/scale-to-width-down/250?cb=20200317174807"></img>
</p>
<h1 align="center"><b>MCHoneyPot</b></h1>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge"></img>
  <img src="https://img.shields.io/github/repo-size/ScriptLineStudios/MCHoneyPot?style=%22for-the-badge%22"></img>
  <img src="https://img.shields.io/github/last-commit/ScriptLineStudios/MCHoneyPot?style=%22for-the-badge%22"></img>
</p>
<p align="center">
  <a target="_blank" style="display: none;" href="https://discord.gg/7QSnA726dx">
    <img src="https://dcbadge.vercel.app/api/server/7QSnA726dx">
  </a>
</p>
<p align="center">
A Minecraft server honeypot built to report mass server scanning. 
</p>

## About

MCHoneyPot works by creating realistic looking Minecraft server, faking details such as players online, server version etc. 
It's job is to log all attempts made to interact with the server including pings, status requests, and attempts to join.
The goal is to index, report, and raise awareness of mass server scanning and how it can affect server owners.

![Screenshot from 2024-03-16 09-18-49](https://github.com/ScriptLineStudios/MCHoneyPot/assets/85095943/c906b738-1a25-4db1-ab87-59cb467c1dcb)

All interactions made with the server are logged:

![Screenshot from 2024-03-16 09-23-43](https://github.com/ScriptLineStudios/MCHoneyPot/assets/85095943/0ec9e6bf-3b07-43d4-95e4-53162bdb896f)

![Screenshot from 2024-03-16 18-50-55](https://github.com/ScriptLineStudios/MCHoneyPot/assets/85095943/54f13d77-7bce-4f5b-aab3-8066b9c4edb4)

Additionally reports are made to https://www.abuseipdb.com/  

## Getting Started

If you would simplily like to interact with the hosted version of the bot, you can do so by joining our <a href="https://discord.gg/7QSnA726dx">Discord Server</a> where you can feel free to interact with the bot as you please.

Alternatively you can invite the bot to your own server using the following <a href="https://discord.com/oauth2/authorize?client_id=1216381150910742558&permissions=826781321280&scope=bot">invite</a>
Once the bot is in your server run /configure in the channel where you would like the bot to output logs!

<p align="center">
<img src="https://github.com/ScriptLineStudios/MCHoneyPot/assets/85095943/a531528a-0d4e-495b-bc76-59c322fdab8a">
</p>

## Running your own instance

In order to run your own instance of MCHoneyPot you will need the following:

* An account and API key on https://www.abuseipdb.com/
* A fresh Discord bot token
* A MongoDB database with the following 4 collections: ```Pings```, ```Joins```, ```Servers```, and ```Reports```

To get started simpily:
```bash
git clone https://github.com/ScriptLineStudios/MCHoneyPot
cd MCHoneyPot
pip install -r requirements.txt
python run.py [LIST OF PORTS]
```

On you first run, you will be promopted to give your API keys/tokens to your newly created config file. Once you have done this you can run the script again and you should be good to go!
