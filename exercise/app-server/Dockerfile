FROM node:15.8.0-alpine3.12

WORKDIR /app/app-server
COPY app-server ./
RUN npm install

ENTRYPOINT ["npm", "start"]
