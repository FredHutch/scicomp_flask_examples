# you need to pass -e STORCRAWL_DB_URL=... to the `docker run` command
# to make the container aware of the database url
# full command might look like this:
# docker run -ti --rm -p 5000:5000 -e STORCRAWL_DB_URL=$STORCRAWL_DB_URL dtenenba/storcrawl_hotspot

FROM ubuntu:16.04

RUN apt-get update -y

RUN apt-get install -y python3 python3-dev python3-pip git

COPY . /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD gunicorn -w 4 -b 0.0.0.0:5000 start_app:app
