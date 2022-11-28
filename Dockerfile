FROM python:latest

WORKDIR /CryptoNotifier

COPY poetry.lock .
COPY pyproject.toml .
COPY . .


RUN rm -r tests/

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install

CMD ["poetry", "run", "python", "bot_bob.py"]