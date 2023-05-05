# Use the official Node.js 18 base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Set the production environment variable
ENV NODE_ENV=production

# Expose the port for the app to run on
EXPOSE 9090

# Start the app
CMD ["npm", "run", "start"]
