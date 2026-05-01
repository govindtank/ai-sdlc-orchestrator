FROM node:18-alpine

WORKDIR /app

# Install app dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend code
COPY frontend/ .

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]