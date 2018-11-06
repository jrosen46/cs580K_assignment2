FROM iwaseyusuke/mininet

WORKDIR /app

COPY ./app /app

# RUN apt-get update && apt-get -y install git
# RUN env GIT_SSL_NO_VERIFY=true git clone https://github.com/noxrepo/pox
