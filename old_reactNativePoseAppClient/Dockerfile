FROM node:17-alpine

# EXPOSE 19000

WORKDIR /app

COPY package.json .

RUN yarn install --ignore-engines

COPY . .

CMD [ "yarn", "expo", "start"]