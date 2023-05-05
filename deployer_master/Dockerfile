FROM python:3.8
RUN apt-get update && apt-get install -y gcc
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "master.py"]