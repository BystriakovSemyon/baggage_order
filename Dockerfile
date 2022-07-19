FROM python:3.9

WORKDIR /opt/app/

ENV TZ 'UTC'
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
    #&& rm -rf /opt/venv/src/*/.git \
    #&& rm -rf ~/.gitconfig

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/opt/app/baggage_order"

ENTRYPOINT  []
CMD ["/opt/venv/bin/python", "-m", "baggage_order"]
