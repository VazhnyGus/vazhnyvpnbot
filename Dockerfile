FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

RUN --mount=type=secret,id=bot_token,env=BOT_TOKEN
RUN --mount=type=secret,id=database_url,env=DATABASE_URL
RUN --mount=type=secret,id=outline_api_url,env=OUTLINE_API_URL
RUN --mount=type=secret,id=outline_api_cer,env=OUTLINE_API_CERT
RUN --mount=type=secret,id=admin_password,env=ADMIN_PASSWORD

ENV DATABASE_URL=secrets.database_url

COPY . .

ENTRYPOINT ["python3", "run.py"]