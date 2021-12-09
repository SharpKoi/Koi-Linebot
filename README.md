# Koi Line Messaging Bot
A linebot project with integration Gunicorn + Flask + Sqlalchemy + PostgresQL.  

This project works fine. If you are starting a line bot project with flask app
and may have some trouble on development, the project will be a nice reference for you.  
In this project you will learn how to integrate sqlalchemy properly with gunicorn app, 
and how to deal with gunicorn multi workers.

Before starting, it's recommended to have some basic knowledge about Flask, WSGI, Gunicorn,
sqlalchemy and PostgresQL. I have already put them in the [reference](#Reference).

The project showcase: https://lin.ee/64nNuMK  
The common problems and solutions: https://hackmd.io/@KoiSharp/B1-vVZWOK

## Features
- [x] Notification
- [ ] Youtube audio downloading
- [ ] Website

## Usage
You can clone this repo to run locally.  
Note that gunicorn does not support Windows os. It's suggested to run in Linux or UNIX os.  

Here is a simple way to run this project locally:
1. Install ngrok. Please refer to its download page https://ngrok.com/download.
2. Run this command below to clone this repo to your local machine.
   ```shell
   git clone https://github.com/SharpKoi/Koi-Linebot.git
   ```
3. Go to the `Koi-Linebot/`
   ```shell
   cd Koi-Linebot
   ```
4. Install the requirements of this project.
   ```shell
   pip install -r requirements.txt
   ```
5. Execute `main.py` with your token, secret and database url:
   ```shell
   python main.py --token="your channel access token" --secret="your channel secret" --db="your database url"
   ```
6. Start ngrok server.
   ```shell
   ngrok http 8000
   ```
7. Copy the ngrok https address and paste it to the webhook url of your line bot. With `/callback`
   at its end. Like this: `https://a371-140-113-136-218.ngrok.io/callback`
8. Press the "Verify" button to check if it works. If works, you will see a message "received ping"
   on your terminal.


## Reference
- [Flask Document](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask App Factories](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/)
- [Flask Sqlalchemy Document](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Intro to WSGI](https://wsgi.tutorial.codepoint.net/)
- [Gunicorn Document](https://docs.gunicorn.org/en/latest/index.html)
- [PostgresQL Document](https://www.postgresql.org/docs/current/index.html)
- [PostgresQL 中文說明文件](https://docs.postgresql.tw/)
- [Flask with WSGI 中文教學](https://minglunwu.github.io/notes/2021/flask_plus_wsgi.html)


*Last Edited on: 2021.12.09*