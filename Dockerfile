

ARG BASE_IMAGE=python:3.7-slim-buster
FROM $BASE_IMAGE

# install project requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
    useradd -d /home/kedro -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro

# copy the whole project except what is in .dockerignore
WORKDIR /home/kedro
COPY . .
RUN chown -R kedro:${KEDRO_GID} /home/kedro
USER kedro
RUN chmod -R a+w /home/kedro

ENTRYPOINT [ "kedro" ]


# FROM python:3.7-slim-buster

# COPY requirements.txt /app/requirements.txt
# COPY .telemetry /app/.telemetry
# COPY pyproject.toml /app/pyproject.toml
# COPY setup.cfg /app/setup.cfg
# COPY conf /app/conf
# COPY logs /app/logs
# COPY data /app/data
# COPY src /app/src

# WORKDIR /app

# RUN pip install -r requirements.txt
# ENV GIT_PYTHON_REFRESH=quiet
# RUN kedro package
# RUN pip install src/dist/$(ls src/dist | grep ".whl")

# ENTRYPOINT [ "kedro" ]
