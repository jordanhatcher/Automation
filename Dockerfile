FROM alpine:3.7

COPY requirements.txt .

RUN apk --no-cache add python3 py-pip && \
    pip3 install -r requirements.txt

COPY src /src
WORKDIR /src

ENTRYPOINT ./entrypoint.sh
