from ubuntu:latest

#################################
#                               #
# Vapor configuration and build #
#                               #
#################################

RUN apt clean \
    && apt update \
    && apt install -y git \
    && apt install -y python3 \
    && apt install -y python3-pip \
    && apt install -y gdal-bin \
    && apt install -y libgdal-dev

RUN python3 -m pip install gdal scipy Pillow cartopy numpy OWSLib

RUN git clone https://github.com/sgpearse/geotiff-maker.git

RUN python3 geotiff-maker/wmts.py
