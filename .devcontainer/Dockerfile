ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

ARG USERNAME=vscode
RUN mkdir -p /home/$USERNAME/.vscode-server/extensions \
    && chown -R $USERNAME /home/$USERNAME/.vscode-server

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/home/$USERNAME/.local/share/pypoetry python3 - \
    && mkdir -p /home/$USERNAME/.local/bin \
    && ln -s /home/$USERNAME/.local/share/pypoetry/bin/poetry /home/$USERNAME/.local/bin/poetry \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME/.local
