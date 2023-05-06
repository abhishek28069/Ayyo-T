# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory to /app
WORKDIR /app

# Copy the rest of the app source code to the container
COPY app .

# Install dependencies
RUN npm install


# Expose port 3000 for the app to listen on
EXPOSE 3000
USER root

# Start the app
CMD ["npm", "start"]
