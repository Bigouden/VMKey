FROM alpine:3.12
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
COPY requirements.txt /
RUN apk add --update --no-cache \
      curl \
      python3 \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && apk del curl \
    && python3 get-pip.py \
    && pip --no-cache-dir install -r requirements.txt \
    && rm -rf \
         /tmp/* \
         /root/.cache/* \
         get-pip.py
COPY vm_key.py /usr/bin/
ENTRYPOINT ["sh"]
