# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.4

FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1261170300666646528/mhJM6vLfKt6k0w3EX361vdMHygdobbhQY2u_jMZH7bq1_GxqK23FBfVgcpkgbk6Glm5k

ENV URL_SHORTENER_USERNAME=eli32

ENV URL_SHORTENER_PASSWORD=eason2830

EXPOSE 8080

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
