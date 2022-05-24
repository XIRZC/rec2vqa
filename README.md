# Referring Expression Based Visual Question Answering

This repository is the official implementation of project "Referring Expression Based Visual Question Answering".

## Prerequisites

### Environments

#### Backend

Please refer to ![VL-BERT repository](https://github.com/jackroos/VL-BERT.git) for prepare backend environments.

#### Frontend

The version of Python, django and its dependencies should be as newer as possible.

### Installation

### Backend

Just clone the repository backend subdir into your GPU server and deploy by `python manage.py runserver 127.0.0.1:6009` after backend environments prepared.

### Frontend

You should use below commands to create basic frontend environments:

```
apt-get install nodejs
npm set registry https://registry.npmmirror.com/
npm install -g @vue/cli
npm install axios --save
npm install element-plus --save
```

## Technology Stack

- frontend: vue3 + elementplus + typescript (port: 8000, deployed at ALiYun)

- backend: django + restframework + corsheader (port: 6006, deployed at AutoDL 1080Ti GPU server)


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
