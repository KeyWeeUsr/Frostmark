FROM node:alpine
RUN mkdir /app
WORKDIR /app

# copy commented package.json and strip comments
COPY package.json.tmpl package.json
RUN sed -i -e '/\/\/ /d' package.json && cat package.json

# install all the deps from package.json
RUN yarn install

# ensure node_modules on PATH
ENV PATH /app/:$PATH

# make sure webpack hot reloading works
ENV CHOKIDAR_USEPOLLING true
