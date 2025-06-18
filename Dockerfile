# Use a lightweight Node.js image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose app port
EXPOSE 3000

# Start the server
CMD ["node", "server.js"]
