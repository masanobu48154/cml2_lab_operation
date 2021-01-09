FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip apache2 vim && pip3 install requests selenium && a2enmod cgid && service apache2 restart
COPY cgi-bin/apple.py /usr/lib/cgi-bin/
COPY cgi-bin/cml2_rest_api.py /usr/lib/cgi-bin/
COPY cgi-bin/breakout.py /usr/lib/cgi-bin/
COPY cgi-bin/env.py /usr/lib/cgi-bin/
ADD cgi-bin/virl_data.tar.gz /usr/lib/cgi-bin/
RUN chmod 755 -R /usr/lib/cgi-bin/

ENTRYPOINT ["/bin/bash"]
CMD  ["apachectl", "-D", "FOREGROUND"]
