FROM python:3.8-alpine3.12

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache git &&\
    pip install --no-cache-dir \
    git+git://github.com/PyGithub/PyGithub@e272f1172178391f80e4c61b113fb7e1e2002962

COPY action.py /usr/local/bin/

ENTRYPOINT ["action.py"]
