FROM node:19.0-alpine3.16

WORKDIR /work
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve"]