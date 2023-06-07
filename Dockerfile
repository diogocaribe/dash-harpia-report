FROM python:3.11.3-bullseye
RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install nano
 
RUN mkdir /workspace
WORKDIR /workspace

COPY requirements.txt /workspace
RUN pip3 install -r $PWD/requirements.txt 

COPY app/ ./

CMD [ "gunicorn", "--workers=8", "--threads=10", "-b 0.0.0.0:80", "-t 3000", "app:server"]
