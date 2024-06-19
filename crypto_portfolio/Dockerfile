FROM homeassistant/amd64-base-python:3.9

RUN apk add --no-cache python3 py3-pip
RUN python3 -m pip install --upgrade pip
RUN pip install requests

COPY rootfs/etc/services.d/crypto_portfolio/run /etc/services.d/crypto_portfolio/run
COPY rootfs/usr/bin/crypto_portfolio.py /usr/bin/
COPY rootfs/usr/bin/db.py /usr/bin/

RUN chmod a+x /etc/services.d/crypto_portfolio/run

CMD [ "/etc/services.d/crypto_portfolio/run" ]
