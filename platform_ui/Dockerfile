FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local app directory to the container at /app
COPY app /app

RUN pip install -r ./requirements.txt

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN npm install dayjs

RUN npm install

EXPOSE 5173

# Set the user to root
USER root

CMD ["npm", "run", "dev"]
