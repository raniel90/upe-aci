# Dockerfile otimizado para Agno Playground - seguindo boas práticas oficiais
FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Configurar Poetry para produção
RUN poetry config virtualenvs.create false

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instalar dependências (incluindo prod group)
RUN poetry install --only=main,prod --no-dev

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários conforme padrão Agno
RUN mkdir -p tmp data/pdfs

# Configurar usuário não-root para segurança
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check conforme recomendações Agno
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expor porta padrão FastAPI
EXPOSE 8000

# Comando de inicialização com configurações otimizadas para Agno
CMD ["uvicorn", "playground:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]