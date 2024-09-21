FROM python:3.12-slim

WORKDIR /app

# O docker trabalha com layered caching, então se não tiver alteração nas dependencias,
# ele ira pular essa etapa e apenas rodara com as alterações no código
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
