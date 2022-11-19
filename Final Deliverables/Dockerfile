FROM python:3.10.5
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install ibm_db
RUN pip install requests
RUN pip install urllib3

ENTRYPOINT FLASK_APP=app.py flask run --host=0.0.0.0
EXPOSE 5000