FROM python:3.8
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
EXPOSE 8081
CMD ["python", "deploy.py"]