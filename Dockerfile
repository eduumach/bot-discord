FROM python:3.11.4

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . app/

WORKDIR app/

EXPOSE 80/tcp  # Expose port 80

CMD [ "python", "./main.py" ]