FROM python:3.11.4

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . app/

WORKDIR app/

CMD [ "python", "./main.py" ]
