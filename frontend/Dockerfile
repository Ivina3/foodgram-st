FROM node:21.7.1-alpine
WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install --legacy-peer-deps
RUN npm install --global http-server --legacy-peer-deps


COPY . .
RUN npm run build

CMD ["npx", "-y", "http-server", "-p", "8000", "/app/build"]
