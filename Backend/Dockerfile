FROM python:3.12

WORKDIR /MLECH.Backend

COPY pyprojectDocker.toml uv.lock ./

RUN mv pyprojectDocker.toml pyproject.toml

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
