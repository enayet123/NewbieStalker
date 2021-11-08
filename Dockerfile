# for raspberry pi
FROM balenalib/raspberry-pi-debian-python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./

CMD [ "python3", "-u", "./greedstalker.py" ]
