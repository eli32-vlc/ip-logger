# Loggify
## Self hosted open source IP logger

> This tool is only educational purpose only! I am not responsible for any damages that occur while using this tool.

### Backstory

Once, I was dealing with a scammer on Discord. I wanted to use Grabify to pull his IP address, but I thought the link was too obvious. So, I made this Python app that you can self-host and attach to a custom domain.

### How does it work?

It's a Python Flask web app. You can use it as a normal link shortener, but it will send the victim's IP to a Discord webhook. It also displays geolocation and timezone in the Discord message. You need a server to host this, as well as a Discord account. A custom domain is not required.

### Deploy Guide (Docker)

1. Install docker

2. Run ```docker build -t loggify . ```

3. Log in to Discord, create a new server, and generate a webhook for that server

3. Run
``` 
docker run -d -p 80:8080 --name loggify \
  -e URL_SHORTENER_USERNAME='admin' \
  -e URL_SHORTENER_PASSWORD='admin' \
  -e DISCORD_WEBHOOK_URL='WEBHOOK' \
  loggify
```

4. Replace 'WEBHOOK' with your discord webhook

5. Visit http://localhost

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

12. Click 'deploy'

13. Click on 'Links'

14. Click the first link in the dropdown
    
---
### Deploy Guide (Manual with python)

1. Make sure python and git is installed

2. Open powershell/terminal

    > Do not use cmd!!

3. Run ```git clonehttps://github.com/eli32-vlc/ip-logger.git```

4. Run ```cd ip-logger```

5. Run ```pip install -r requirements.txt```

6. Run ```export DISCORD_WEBHOOK_URL=Your webhook```

7. Run ```export URL_SHORTENER_USERNAME=Your admin username```

8. Run ```export URL_SHORTENER_PASSWORD=Your admin username```

9.  Run ```python app.py```

10.  Open the url display in the terminal


---
### Deploy Guide (Render.com)

> This deploy method is unreliable! Your url will not work after 5 minutes of inactivity!

1. Create a new web service

2. Click 'Build and deploy from a Git repository'

3. Click 'Next'
