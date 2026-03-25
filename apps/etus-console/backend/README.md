# ETUS Console Backend

Backend local read-only para o console do ETUS.

## Rodando

```bash
cd apps/etus-console/backend
python3 -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

## Testes

```bash
cd apps/etus-console/backend
source .venv/bin/activate
python -m unittest discover -s tests
```
