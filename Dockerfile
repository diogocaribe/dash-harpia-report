FROM python:3.11.2-bullseye
RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install nano
 
RUN mkdir /workspace
WORKDIR /workspace

COPY requirements.txt /workspace
RUN pip3 install -r $PWD/requirements.txt 

CMD [ "gunicorn", "--workers=2", "--threads=1", "-b 0.0.0.0:80", "app.app:server"]
