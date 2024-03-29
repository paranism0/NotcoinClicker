FROM python:3.11-slim-buster as base
ARG CHROME_VERSION="116.0.5845.179"
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb \
    && apt install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb \
    && apt-get install -y python3-distutils && \
    python3 -m pip install pipenv
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && chmod +x chromedriver && \
    rm LICENSE.chromedriver

RUN pipenv install --system

CMD ["python" , "main.py"]