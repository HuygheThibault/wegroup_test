FROM python:3.8-alpine

WORKDIR '/app'

#RUN apk add --no-cache linux-headers g++

#RUN apk add --no-cache tzdata

COPY ./ ./

RUN pip install pipenv

EXPOSE 5000
CMD [ "python", "app/app.py" ]
