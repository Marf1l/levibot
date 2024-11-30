# levibot
# !!!read in code mode!!!
tgbot for downloading videos from tik tok without watermark

!!!settings for windows!!!

1). First you need to install a virtual environment (venv):
python -m venv venv
venv/scripts/activate
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

1.1). install libraries with the required versions specified in the "requirements.txt" file.
  pip install Flask
  pip install -U yt-dlp
  pip install pyTelegramBotAPI
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

2). Select which host to upload the file to.
"For example, fly":
2.1) Register on the fly.io website:

1. Registration on Fly.io - https://fly.io/
2. Install Fly CLI:
2.1 Go to the Fly.io CLI page on GitHub: https://github.com/superfly/flyctl/releases
2.2 Download the archive with the .zip extension, for example: flyctl-vX.X.X-windows-amd64.zip (where X.X.X is the version number).
2.3 Unzip the downloaded file to a convenient folder. 
For example, you can create a folder C:\flyctl and unzip the file there.
Move the flyctl.exe file to a folder that is already added to the system Path, or add the path to this folder to the Path environment variable. To add it to the system Path
2.4 Checking the Fly CLI installation and authorization:
flyctl version
flyctl auth login
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

3) Then we create a Dockerfile:
we write on which version of Python we wrote the code, for example: 

# Устанавливаем рабочую директорию
FROM python:3.12.2-slim
# Set up the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install all dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Launch your Telegram bot
CMD ["python", "levidw.py"] - instead of "levidw.py" write the name of your py file.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

4). We change the api token to yours which you take from BotFather:
bot = telebot.TeleBot("APITOKEN") - instead of "APITOKEN" change to your own.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

5). In the fly.toml file we change:
app = 'levidw' - instead of 'levidw' we change to our name.
internal_port = 8080 - instead of "8080" we change to our port.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

6). Change webhook:
bot.set_webhook(url="https://levidw.fly.dev/webhook") - instead of "https://levidw.fly.dev/webhook" - write your link that you will receive on the hosting.

7). Deploy:
flyctl deploy

8). Commands:
Viewing Logs: To monitor application logs in real time, use the command:
flyctl logs

Application Management:
flyctl status

Stopping the application: To stop the application:
flyctl apps destroy my-app

Updating the application: If you want to make changes to the code and deploy the updated version, simply run the command:
flyctl deploy
