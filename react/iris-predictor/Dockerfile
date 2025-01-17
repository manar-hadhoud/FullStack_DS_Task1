# Step 1: Use an official Node.js image for building the app
FROM node:20.13.0 

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json .

# Install dependencies
RUN npm install

# Copy the entire React app to the working directory
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
