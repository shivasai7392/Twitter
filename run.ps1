# Run FastAPI dev server with UTF-8 encoding (fixes emoji crash on Windows)
$env:PYTHONIOENCODING = "utf-8"
uv run fastapi dev main.py
