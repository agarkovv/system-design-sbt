FROM alpine:3.11

RUN apk add --no-cache \
    openssh-client \
    ansible \
    git \
    sshpass \
    docker-cli

WORKDIR /ansible

CMD ["/bin/sh"]