FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y \
    bluez bluetooth 

RUN pip install -r requirements.txt

EXPOSE 5000

COPY ./docker_entrypoint.sh /
RUN chmod +x docker_entrypoint.sh
ENTRYPOINT sh docker_entrypoint.sh