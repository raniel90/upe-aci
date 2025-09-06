# 🛡️ NR-06 Operational System

Sistema operacional para Equipamentos de Proteção Individual baseado na Norma Regulamentadora 06, desenvolvido com o framework [Agno](https://docs.agno.com/).

## 🏗️ **Estrutura do Projeto**

```
aci/
├── agent/          # Backend - Sistema de agentes com Agno Framework
│   ├── agent.py
│   ├── pyproject.toml
│   ├── docker-compose.yml
│   └── ...
├── ui/             # Frontend - Interface React/Next.js
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
```

## 🎯 **Agentes Especializados**

- **🎯 Seletor de EPIs** - Recomenda EPIs específicos por tipo de risco
- **📋 Auditor NR-06** - Gera checklists de auditoria e classifica não conformidades  
- **🎓 Designer de Treinamentos** - Cria programas de capacitação personalizados
- **🔍 Investigador de Acidentes** - Analisa acidentes relacionados a EPIs
- **⚖️ Consultor Legal** - Esclarece aspectos legais da NR-06
- **📝 Gerador de POPs** - Cria procedimentos operacionais padrão

## 🚀 **Setup e Execução**

### 🔧 **Desenvolvimento Local**

#### 1. Backend (Agent System)
```bash
cd agent/

# Instalar dependências
poetry install

# Configurar ambiente
cp env.example .env
# Edite .env com sua OPENAI_API_KEY

# Executar localmente
poetry run python agent.py
# ou
./deploy.sh local
```

#### 2. Frontend (UI)
```bash
cd ui/

# Instalar dependências
npm install
# ou
pnpm install

# Executar em desenvolvimento
npm run dev
# ou
pnpm dev
```

### 🐳 **Produção com Docker**

#### Opção 1: Docker Compose (Recomendado)
```bash
# 1. Backend
cd agent/
cp production.env .env
# Edite .env com suas chaves reais

# 2. Deploy completo
./deploy.sh production

# 3. Verificar status
docker-compose -f docker-compose.prod.yml ps
```

#### Opção 2: Containers Separados
```bash
# Backend
cd agent/
docker-compose up -d

# Frontend (em outro terminal)
cd ui/
npm run build
npm start
```

### ☁️ **AWS com Agno CLI (Enterprise)**
```bash
cd agent/

# 1. Instalar Agno CLI
pip install agno-cli

# 2. Configurar workspace
ag ws create

# 3. Deploy AWS
./deploy.sh aws
```

## 📊 **Acesso e Monitoramento**

### URLs de Acesso
#### Frontend (UI)
- **Desenvolvimento**: http://localhost:3000
- **Produção**: http://localhost:3000 (ou porta configurada)

#### Backend (Agent API)
- **Desenvolvimento**: http://localhost:7777
- **Produção**: http://localhost:8000
- **AWS**: https://your-domain.com

### Health Checks
- **Backend Local**: http://localhost:7777/health
- **Backend Produção**: http://localhost:8000/health
- **AWS**: https://your-domain.com/health

### Endpoints Principais
- **UI Interface**: `/` - Interface React principal
- **Agent Playground**: `/playground` - Interface de agentes
- **API Docs**: `/docs` - Documentação automática da API
- **API Root**: `/` - Informações do sistema backend

## 🏗️ **Arquitetura do Sistema**

### Desenvolvimento
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │───▶│  Agent Backend  │───▶│   PgVector DB   │
│   (Port 3000)   │    │  (Port 7777)    │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LanceDB       │
                       │   (Vectors)     │
                       └─────────────────┘
```

### Produção
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │───▶│   React UI      │    │  Agent Backend  │
│   (Port 80/443) │    │   (Port 3000)   │───▶│  (Port 8000)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              ▼
                       │   Redis Cache   │    ┌─────────────────┐
                       │   (Port 6379)   │◀───│   PgVector DB   │
                       └─────────────────┘    │   (Port 5432)   │
                                              └─────────────────┘
```

## 🔧 **Configuração**

### Backend (Agent) - Variáveis Obrigatórias
```bash
OPENAI_API_KEY=sk-...           # API Key da OpenAI
ENVIRONMENT=production          # Ambiente de execução
DATABASE_URL=postgresql+psycopg://ai:ai@pgvector:5432/ai
```

### Backend (Agent) - Variáveis Opcionais
```bash
SENTRY_DSN=https://...         # Monitoramento de erros
REDIS_URL=redis://redis:6379/0 # Cache e sessões
SECRET_KEY=your_secret_key     # Segurança da aplicação
```

### Frontend (UI) - Configuração
```bash
# .env.local na pasta ui/
NEXT_PUBLIC_API_URL=http://localhost:7777  # URL do backend em desenvolvimento
# ou
NEXT_PUBLIC_API_URL=http://localhost:8000  # URL do backend em produção
```

## 📦 **Dependências**

### Backend (Agent)
- **Core**: `agno`, `fastapi`, `uvicorn`
- **Database**: `psycopg2-binary`, `sqlalchemy`, `lancedb`
- **AI**: `openai`, `pypdf`
- **Produção**: `gunicorn`, `redis`, `sentry-sdk`

### Frontend (UI)
- **Core**: `next`, `react`, `react-dom`
- **UI**: `tailwindcss`, `lucide-react`
- **State**: `zustand`
- **Styling**: `@tailwindcss/typography`
- **Development**: `typescript`, `eslint`, `prettier`

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

### Backend (Agent)
```bash
# Desenvolvimento
cd agent/
poetry run python agent.py

# Ver logs em tempo real (Docker)
docker-compose -f docker-compose.prod.yml logs -f

# Restart apenas a aplicação
docker-compose -f docker-compose.prod.yml restart nr06-playground

# Backup do database
docker exec pgvector pg_dump -U ai ai > backup.sql
```

### Frontend (UI)
```bash
# Desenvolvimento
cd ui/
npm run dev

# Build para produção
npm run build
npm start

# Lint e format
npm run lint
npm run format
```

### Sistema Completo
```bash
# Monitorar performance
docker stats

# Verificar portas em uso
lsof -i :3000  # Frontend
lsof -i :7777  # Backend dev
lsof -i :8000  # Backend prod
```

## 🆘 **Troubleshooting**

### Backend (Agent)

#### Erro: "Could not connect to docker"
```bash
# Verificar se Docker está rodando
docker info

# No macOS: reiniciar Docker Desktop
# No Linux: sudo systemctl restart docker
```

#### Erro: "ImportError OpenAI"
```bash
# Reinstalar dependências
cd agent/
poetry install --only=main,prod
```

#### Erro: Database connection
```bash
# Verificar se PgVector está rodando
docker ps | grep pgvector

# Testar conexão
docker exec pgvector psql -U ai -d ai -c "SELECT 1;"
```

### Frontend (UI)

#### Erro: "Module not found"
```bash
# Limpar cache e reinstalar
cd ui/
rm -rf node_modules package-lock.json
npm install
```

#### Erro: "Port 3000 already in use"
```bash
# Verificar processo usando a porta
lsof -ti:3000 | xargs kill -9

# Ou usar porta diferente
npm run dev -- -p 3001
```

#### Erro: "API connection failed"
```bash
# Verificar se backend está rodando
curl http://localhost:7777/health

# Verificar variável de ambiente
echo $NEXT_PUBLIC_API_URL
```

## 🔄 **Workflow de Desenvolvimento**

### Setup Inicial
```bash
# 1. Clone o repositório
git clone <repository-url>
cd aci

# 2. Setup Backend
cd agent/
poetry install
cp env.example .env
# Configure OPENAI_API_KEY no .env

# 3. Setup Frontend
cd ../ui/
npm install
# Configure NEXT_PUBLIC_API_URL se necessário
```

### Desenvolvimento Diário
```bash
# Terminal 1: Backend
cd agent/
poetry run python agent.py

# Terminal 2: Frontend
cd ui/
npm run dev
```

### Antes de Commit
```bash
# Backend
cd agent/
poetry run pytest  # Se houver testes

# Frontend
cd ui/
npm run lint
npm run type-check
npm run build  # Verificar se build passa
```

## 📚 **Documentação**

- [Agno Framework](https://docs.agno.com/)
- [Agno Playground](https://docs.agno.com/applications/playground/introduction)
- [Agno Production Deployment](https://docs.agno.com/workspaces/workspace-management/production-app)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)

---

**Desenvolvido com ❤️ usando [Agno Framework](https://docs.agno.com/)**