# 🛡️ NR-06 Operational System

Sistema operacional para Equipamentos de Proteção Individual baseado na Norma Regulamentadora 06, desenvolvido com o framework [Agno](https://docs.agno.com/).

## 🎯 **Agentes Especializados**

- **🎯 Seletor de EPIs** - Recomenda EPIs específicos por tipo de risco
- **📋 Auditor NR-06** - Gera checklists de auditoria e classifica não conformidades  
- **🎓 Designer de Treinamentos** - Cria programas de capacitação personalizados
- **🔍 Investigador de Acidentes** - Analisa acidentes relacionados a EPIs
- **⚖️ Consultor Legal** - Esclarece aspectos legais da NR-06
- **📝 Gerador de POPs** - Cria procedimentos operacionais padrão

## 🚀 **Deployment em Produção**

### Opção 1: Desenvolvimento Local (Recomendado para testes)
```bash
# 1. Configurar ambiente
export OPENAI_API_KEY=your_api_key

# 2. Deploy local (seguindo padrão Agno)
./deploy.sh local
```

### Opção 2: Produção com Docker Compose
```bash
# 1. Configurar variáveis de ambiente
cp production.env .env
# Edite .env com suas chaves reais

# 2. Deploy produção
./deploy.sh production

# 3. Verificar status
docker-compose -f docker-compose.prod.yml ps
```

### Opção 3: AWS com Agno CLI (Enterprise)
```bash
# 1. Instalar Agno CLI
pip install agno-cli

# 2. Configurar workspace
ag ws create

# 3. Deploy AWS
./deploy.sh aws
```

## 📊 **Monitoramento**

### Health Checks
- **Local**: http://localhost:7777/health
- **Produção**: http://localhost:8000/health
- **AWS**: https://your-domain.com/health

### Endpoints Principais
- **Playground**: `/playground` - Interface principal
- **API Docs**: `/docs` - Documentação automática
- **Root**: `/` - Informações do sistema

## 🏗️ **Arquitetura de Produção**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │───▶│  NR-06 App      │───▶│   PgVector DB   │
│   (Port 80/443) │    │  (Port 8000)    │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis Cache   │
                       │   (Port 6379)   │
                       └─────────────────┘
```

## 🔧 **Configuração**

### Variáveis de Ambiente Obrigatórias
```bash
OPENAI_API_KEY=sk-...           # API Key da OpenAI
ENVIRONMENT=production          # Ambiente de execução
DATABASE_URL=postgresql+psycopg://ai:ai@pgvector:5432/ai
```

### Variáveis Opcionais
```bash
SENTRY_DSN=https://...         # Monitoramento de erros
REDIS_URL=redis://redis:6379/0 # Cache e sessões
SECRET_KEY=your_secret_key     # Segurança da aplicação
```

## 📦 **Dependências de Produção**

- **Core**: `agno`, `fastapi`, `uvicorn`
- **Database**: `psycopg2-binary`, `sqlalchemy`, `lancedb`
- **AI**: `openai`, `pypdf`
- **Produção**: `gunicorn`, `redis`, `sentry-sdk`

## 🔒 **Segurança**

- ✅ Containers não-root
- ✅ Health checks configurados
- ✅ Rate limiting (Nginx)
- ✅ Security headers
- ✅ Environment variables isoladas
- ✅ Logs estruturados

## 📈 **Escalabilidade**

### Horizontal Scaling
```bash
# Escalar aplicação
docker-compose -f docker-compose.prod.yml up --scale nr06-playground=3

# Load balancer automático via Nginx
```

### Vertical Scaling
```yaml
# Ajustar resources no docker-compose.prod.yml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
```

## 🛠️ **Comandos Úteis**

```bash
# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Restart apenas a aplicação
docker-compose -f docker-compose.prod.yml restart nr06-playground

# Backup do database
docker exec pgvector pg_dump -U ai ai > backup.sql

# Monitorar performance
docker stats
```

## 🆘 **Troubleshooting**

### Erro: "Could not connect to docker"
```bash
# Verificar se Docker está rodando
docker info

# No macOS: reiniciar Docker Desktop
# No Linux: sudo systemctl restart docker
```

### Erro: "ImportError OpenAI"
```bash
# Reinstalar dependências
poetry install --only=main,prod
```

### Erro: Database connection
```bash
# Verificar se PgVector está rodando
docker ps | grep pgvector

# Testar conexão
docker exec pgvector psql -U ai -d ai -c "SELECT 1;"
```

## 📚 **Documentação**

- [Agno Framework](https://docs.agno.com/)
- [Agno Playground](https://docs.agno.com/applications/playground/introduction)
- [Agno Production Deployment](https://docs.agno.com/workspaces/workspace-management/production-app)

---

**Desenvolvido com ❤️ usando [Agno Framework](https://docs.agno.com/)**