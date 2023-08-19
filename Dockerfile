FROM python:3.11.4

ADD . /

RUN pip install -r requirements.txt

EXPOSE 80/tcp  # Expose port 80

CMD [ "python", "./main.py" ]