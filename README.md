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
sudo apt-get install redis-server
sudo apt-get install rabbitmq-server
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
├── vlbert (VLBERT project root dir)
│   ├── cfgs (model train/val/test configs)
│   ├── ckpts (finetuned model dir, include vqa and rec)
│   ├── common (some common modules required by vlbert including resnet101, fastrcnn)
│   ├── data (MS COCO train2014/val2014/test2015 images, vqa/rec annotations and precomputed boxes and features)
│   ├── external (pretrained bert codes developed by huggingface)
│   ├── model (pretrained vlbert model, bert model and resnet101 model parameters)
│   ├── pretrain (some packaged functions)
│   ├── refcoco (vlbert for refcoco codes)
│   ├── vqa (vlbert for vqa codes)
│   ├── vcr (vlbert for vcr codes)
│   ├── viz (vlbert for visulization codes)
│   └── requirements.txt (origin vlbert environment requirements)
```
