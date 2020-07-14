FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/


RUN apt update && apt install -y netcat
# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


COPY ./ /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "shostner.main:app", "--host", "0.0.0.0", "--port", "80"]