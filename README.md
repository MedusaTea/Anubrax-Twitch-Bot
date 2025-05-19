## Summary
This starts a python server listening to chat messages from a channel
and sends the input to a server listening for input commands 
Currently the path is hardcoded to the docker host system on port 8048

However, there is no need for a separate input server if you just want to handle that here within the same codebase

# Requirements 
- Python or Docker
- A Twitch Application and an OAUTH token
- Code interfacing to OS Input 

# Setting up a Twitch Application and Getting a Token
- https://twitchio.dev/en/latest/getting-started/quickstart.html

# .env Setup
- Copy `.env.example` to a new file called `.env`
- Enter your env information into that file

# Windows Input Server Reference
https://github.com/MedusaTea/windows-input-server

# Running with Docker
```bash
$ docker-compose build
$ docker-compose up
```

# Running with Python  
## Install Dependencies 
```bash
$ pip install -r requirements.txt
```

```bash
$ python ./bot.py
```
