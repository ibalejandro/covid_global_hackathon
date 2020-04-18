FROM denismakogon/opencv3-slim:edge
COPY . /app
WORKDIR /app
RUN apt-get -y update && apt-get install -y libgtk2.0-dev && pip install -r requirements.txt
CMD ["python", "runner.py"]
