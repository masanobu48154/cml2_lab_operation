FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 vim && a2enmod cgid && service apache2 restart
COPY html/index.html /var/www/html/
ADD html/cml2s.tar.gz /var/www/html/

ENTRYPOINT ["/bin/bash"]
CMD  ["apachectl", "-D", "FOREGROUND"]
