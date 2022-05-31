# Referring Expression Based Visual Question Answering

This repository is the official implementation of project "Referring Expression Based Visual Question Answering".

## Prerequisites

### Environments

#### Backend

Please refer to ![VL-BERT repository](https://github.com/jackroos/VL-BERT.git) for prepare backend environments.

#### Frontend

The essential frontend environments are node.js and npm, you must note that your ubuntu server version should later than 20.04 and node.js should later than 12.0, so that you can install npm dependencies correctly.

### Installation

### System

You need `redis-server` and `rabbitmq-server` to ensure using channel_layer in Django Channels and deploy VLBERT vqa and rec worker, respectively.

```sh
sudo apt-get install redis
sudo apt-get install rabbitmq
```

### Backend

Just clone the repository into your GPU server and deploy by `cd rec2vqa/backend && python manage.py runserver 6006` after backend environments prepared.

### Frontend

You should use below commands to create basic frontend environments:

```
cd rec2vqa
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install nodejs
npm set registry https://registry.npmmirror.com/
cd frontend/app
npm install
```

## Technology Stack

- frontend: vue3 + elementplus + typescript (port: 80, deployed at Nginx using TencentYun)

- backend: django + restframework + corsheader (port: 6006, deployed at AutoDL Tesla P40 GPU server)


## Project Structure

```
.
├── backend (django project root dir)
│   ├── api (api app root dir)
│   ├── backend (project setting dir)
│   ├── manage.py
│   └── dp.splite3 (sqlite3 database file)
├── frontend
│   └── app
│       ├── node_modules (installed node_modules)
│       ├── public (static files)
│       ├── src (vue app root dir)
│       ├── package.json
│       ├── babel.config.js
│       ├── tsconfig.json
│       └── vue.config.js
└── rest-framework-tutorial
```
