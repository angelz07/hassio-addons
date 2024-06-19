FROM homeassistant/amd64-base-python:3.9

RUN python -m pip install --upgrade pip
RUN pip install requests sqlite3

COPY run.sh /
COPY crypto_portfolio.py /usr/bin/
COPY db.py /usr/bin/

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
