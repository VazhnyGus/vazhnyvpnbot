FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENV BOT_TOKEN=$bot_token
ENV DATABASE_URL=$database_url
ENV OUTLINE_API_URL=$outline_api_url
ENV OUTLINE_API_CERT=$outline_api_cert
ENV ADMIN_PASSWORD=$admin_password

COPY . .

ENTRYPOINT ["python3", "run.py"]