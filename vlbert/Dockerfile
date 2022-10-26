# Environment cuda9.0-cudnn7-ubuntu16.04-pytorch1.1-python3.6
FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

WORKDIR /work
COPY ./docker_build/* ./
COPY . .
RUN nvidia-smi

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		git vim libgl1-mesa-glx libglib2.0-0 wget \
	&& rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN /bin/bash ./Miniconda3-py37_4.12.0-Linux-x86_64.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create -n rec2vqa python=3.6 -y
RUN echo "source activate rec2vqa" > ~/.bashrc
ENV PATH /opt/conda/envs/rec2vqa/bin:$PATH

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install ./torch-1.1.0-cp36-cp36m-linux_x86_64.whl torchvision==0.3.0 Cython
RUN pip install git+https://ghproxy.com/https://github.com/tianzhi0549/FCOS.git
RUN pip install ./tensorflow-2.6.2-cp36-cp36m-manylinux2010_x86_64.whl tensorboard tensorboardx
RUN pip install -r ./requirements_vlbert.txt
RUN pip install -r ./requirements_django.txt
RUN ./scripts/init.sh
RUN mkdir -p /root/.torch/models && \
 		wget -O /root/.torch/models/fcos_syncbn_bs32_c128_MNV2_FPN_1x.pth \
		 https://cloudstor.aarnet.edu.au/plus/s/3GKwaxZhDSOlCZ0/download#fcos_syncbn_bs32_c128_MNV2_FPN_1x.pth