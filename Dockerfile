# Dockerfile for Python 2.7 running Flask on gunicorn

FROM python:2-onbuild

MAINTAINER Robert Wlodarczyk (http://github.com/SimplicityGuy)

EXPOSE 80

ADD ./force /usr/src/app/force
WORKDIR /usr/src/app

CMD [ "gunicorn", "-c", "gunicorn-config.py", "force:app" ]
