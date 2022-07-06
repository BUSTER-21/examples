FROM ubuntu:22.04 as baseimg

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /api_documentation
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install python3-tk
RUN apt -y install curl && apt -y install unzip
COPY . ./
WORKDIR /api_documentation/docs
RUN ./img_capture/setup.sh
RUN pip3 install -r ./requirements.txt

RUN make html

FROM nginx 
WORKDIR /api_documentation
COPY --from=baseimg /api_documentation/  ./
COPY --from=baseimg /api_documentation/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"]
