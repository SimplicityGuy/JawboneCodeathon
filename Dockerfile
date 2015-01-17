# Dockerfile for Python 2.7 running Flask on gunicorn

FROM python:2-onbuild

MAINTAINER Robert Wlodarczyk (http://github.com/SimplicityGuy)

EXPOSE 80

CMD [ "gunicorn", "-c", "gunicorn-config.py", "flask-example:app" ]
