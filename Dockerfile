FROM python:3.6-slim
RUN apt-get -y update && apt-get install -y libgtk2.0-dev
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "runner.py"]
