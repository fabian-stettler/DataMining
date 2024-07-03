# Use the official Node.js image from the Docker Hub
FROM node:22-alpine3.19

# Create and set the working directory inside the container
WORKDIR /usr/src/dataminingFiles/

# Install necessary libraries for Puppeteer and bash
RUN apk update && apk add --no-cache \
    chromium \
    nss \
    ttf-freefont \
    font-noto \
    libx11 \
    libxcomposite \
    libxrandr \
    alsa-lib \
    pango \
    gtk+3.0 \
    mesa-gl \
    wget \
    vim \
    bash \
    && rm -rf /var/cache/apk/*

# Set the environment variable to point to the installed Chromium binary
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser


# Copy package.json and package-lock.json (if available) to the working directory
COPY package*.json /usr/src/dataminingFiles/

# Install the dependencies specified in package.json
RUN npm install


# Copy the rest of your application code to the working directory
COPY . /usr/src/dataminingFiles/

# Expose the port the application will run on
EXPOSE 3000

# Execution of control.js
CMD ["node", "control.js"]