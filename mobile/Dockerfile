# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN npm install

# Expose the port the app runs on
EXPOSE 19006

# Run the app
CMD ["npm", "start"]
