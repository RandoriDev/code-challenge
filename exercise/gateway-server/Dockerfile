FROM node:15.8.0-alpine3.12

WORKDIR /app/lib
COPY lib ./
RUN npm install

WORKDIR /app/gateway-server
COPY gateway-server ./
RUN npm install

ENTRYPOINT ["npm", "start"]
