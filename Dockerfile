FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV PORT 8080
ARG postgres_local_password
ARG poke_go_pal_database_name
ARG weather_api_key

ENV POSTGRES_LOCAL_PASSWORD=${postgres_local_password}
ENV POKE_GO_PAL_DATABASE_NAME=${poke_go_pal_database_name}
ENV WEATHER_API_KEY=${weather_api_key}

CMD ["python", "src/server.py"]