# Loggify
## Self hosted open source IP logger

> This tool is only educational purpose only! I am not responsible for any damages that occur while using this tool.

### Backstory

Once, I was dealing with a scammer on Discord. I wanted to use Grabify to pull his IP address, but I thought the link was too obvious. So, I made this Python app that you can self-host and attach to a custom domain.

### How does it work?

It's a Python Flask web app. You can use it as a normal link shortener, but it will send the victim's IP to a Discord webhook. It also displays geolocation and timezone in the Discord message. You need a server to host this, as well as a Discord account. A custom domain is not required.

---

### Deploy Guide (Docker)

1. Install docker

2. Open a terminal/powershell

3. Run ```docker build -t loggify . ```

4. Log in to Discord, create a new server, and generate a webhook for that server

5. Run
``` 
docker run -d -p 80:8080 --name loggify \
  -e URL_SHORTENER_USERNAME='admin' \
  -e URL_SHORTENER_PASSWORD='admin' \
  -e DISCORD_WEBHOOK_URL='WEBHOOK' \
  loggify
```

6. Replace 'WEBHOOK' with your discord webhook

7. Visit http://localhost

Default Username: admin

Default Password: admin

---
### Deploy Guide (Coolify)

1. Create a new project

2. Go to 'production' environment

3. Add a new resource

4. Click 'public repository'

5. Paste in ```https://github.com/eli32-vlc/ip-logger.git```

6. Click on 'Build Pack'

7. Choose 'Dockerfile'

8. Click on 'Continue'

9. Go down to 'Ports Exposes' and change it to 8080

10. Log in to Discord, create a new server, and generate a webhook for that server

11. Go to 'Environment Variables' and add a these variables

    | Name | Value |
    | -------- | ------- |
    | DISCORD_WEBHOOK_URL  | Your webhook    |
    | URL_SHORTENER_USERNAME | Your admin username     |
    | URL_SHORTENER_PASSWORD    | Your admin password    |

12. Click on 'deploy'

13. Click on 'Links'

14. Click the first link in the dropdown
    
---
### Deploy Guide (Manual with python)

1. Make sure python and git is installed

2. Open powershell/terminal

    > Do not use cmd!!

3. Run ```git clone https://github.com/eli32-vlc/ip-logger.git```

4. Run ```cd ip-logger```

5. Run ```pip install -r requirements.txt```

6. Log in to Discord, create a new server, and generate a webhook for that server

7. Run ```export DISCORD_WEBHOOK_URL=Your webhook```

8. Run ```export URL_SHORTENER_USERNAME=Your admin username```

9. Run ```export URL_SHORTENER_PASSWORD=Your admin username```

10.  Run ```python app.py```

111.  Open the url display in the terminal


---
### Deploy Guide (Render.com)

> This deploy method is unreliable! Your url will not work after 5 minutes of inactivity!

1. Create a new web service

2. Click on 'Build and deploy from a Git repository'

3. Click on 'Next'

4. Scroll down till you see 'Public Git repository'

5. Paste in this url ```https://github.com/eli32-vlc/ip-logger.git```

6. Click on 'Continue'

7. Change 'Instance Type' to 'Free'

8. Scroll to 'Environment Variables'

9. Log in to Discord, create a new server, and generate a webhook for that server

10.  Click 'Add from .env'

11. Paste this in:
    ```
    URL_SHORTENER_USERNAME='Admin Username'
    URL_SHORTENER_PASSWORD='Admin Password'
    DISCORD_WEBHOOK_URL='WEBHOOk'
    ```
12. Replace Admin Username with your own username.

13. Replace Admin Password with your own password.

14. Change WEBHOOK to your Discord webhook URL.

15. Click on 'Deploy Web Service'

16. Click the link and login.

---
### LICENSE

Check LICENSE file

---
### Contacts

Email: lyu63651@gmail.com

Discord: zenithrifle





