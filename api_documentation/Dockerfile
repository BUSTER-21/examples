FROM ubuntu:22.04 as baseimg

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /product-docs
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install python3-tk
RUN apt -y install curl && apt -y install unzip
COPY . ./
WORKDIR /product-docs/docs
RUN ./img_capture/setup.sh
RUN pip3 install -r ./requirements.txt

RUN make html

FROM nginx 
WORKDIR /product-docs
COPY --from=baseimg /product-docs/  ./
COPY --from=baseimg /product-docs/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"]