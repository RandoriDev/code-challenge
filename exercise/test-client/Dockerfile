FROM node:15.8.0-alpine3.12

WORKDIR /app/test-client
COPY test-client ./
RUN npm install

ENTRYPOINT ["npm", "start"]
