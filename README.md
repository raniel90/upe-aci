<div align="center">

<img src="ui/src/app/favicon.ico" alt="SafeBot Logo" width="128" height="128">

# 🛡️ SafeBot

*Sistema Inteligente de Segurança do Trabalho*

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

Solução que utiliza inteligência artificial para interpretar, auditar e garantir conformidade através de agentes especializados. Oferece múltiplos canais de acesso: **Telegram Bot 24/7** e **Interface Web** com agentes especializados.

## 🏗️ **Arquitetura**

```
aci/
├── agent/                   # Backend - API SafeBot
│   ├── 🧠 core/
│   │   ├── agent.py         # Factory de agentes reutilizável
│   │   └── __init__.py
│   ├── 📱 telegram_bot/
│   │   ├── bot.py           # Bot Telegram
│   │   └── __init__.py
│   ├── 🌐 web/
│   │   ├── app.py           # Interface web com 6 agentes especializados
│   │   └── __init__.py
│   ├── 🚀 safebot.py        # Launcher unificado
│   ├── 📱 telegram_bot.py   # Acesso rápido ao Telegram
│   ├── 📄 agent.py          # Agent da aplicação web
│   ├── pyproject.toml
│   └── ...
├── ui/                      # Frontend - Interface React/Next.js
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
```

## 🎯 **Canais de Acesso SafeBot**

### 📱 **Telegram Bot**
- **🤖 Bot Real 24/7** - Funciona continuamente no Telegram
- **👥 Multi-usuário** - Cada usuário tem seu próprio agente e memória
- **💬 Conversacional** - Respostas formatadas para mobile
- **⚡ Instantâneo** - Comandos: `/start`, `/help`, `/status`

### 🌐 **Interface Web (Agentes Especializados)**
- **🎯 Seletor de EPIs** - Recomenda EPIs por tipo de risco
- **📋 Auditor NR-06** - Gera checklists de auditoria de conformidade
- **🎓 Designer de Treinamentos** - Cria programas de capacitação personalizados
- **🔍 Investigador de Acidentes** - Analisa acidentes relacionados a EPIs
- **⚖️ Consultor Legal NR-06** - Esclarece aspectos legais da norma
- **📝 Gerador de POPs** - Cria procedimentos operacionais para EPIs

## 🚀 **Setup e Execução**

### 📋 **Configuração Inicial**
```bash
cd agent/

# 1. Instalar dependências
poetry install

# 2. Configurar variáveis de ambiente
cp env.example .env
# Edite .env com suas chaves:
# OPENAI_API_KEY=sua-chave-aqui
# TELEGRAM_TOKEN=seu-token-aqui (opcional, para Telegram)
```

### 🔧 **Opções de Execução**

#### 📱 **Telegram Bot**
```bash
# Opção 1: Via launcher unificado
python safebot.py telegram

# Opção 2: Acesso direto
python telegram_bot.py

# Funcionalidades:
# • Bot real 24/7 no Telegram
# • Múltiplos usuários simultâneos
# • Memória individual por usuário
# • Formatação HTML otimizada
```

#### 🌐 **Interface Web**
```bash
# Opção 1: Via launcher unificado
python safebot.py web

# Opção 2: Aplicação principal (MANTIDA)
python agent.py

# Acesso: http://localhost:7777
# • Interface Agno Playground
# • 6 agentes especializados
# • Ideal para trabalho técnico
```

#### 🔧 **Utilitários**
```bash
# Carregar base de conhecimento NR-06
python safebot.py load-kb

# Informações do sistema
python safebot.py info

# Ajuda completa
python safebot.py help
```

### 🎨 **Frontend (UI)**
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

# Acesso: http://localhost:3000
# • Interface React/Next.js moderna
# • Conecta com backend SafeBot
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

### ☁️ **Deploy em Nuvem**
```bash
cd agent/

# 1. Configurar credenciais AWS
aws configure

# 2. Criar infraestrutura (usando Terraform/CDK)
# terraform init && terraform apply

# 3. Deploy da aplicação
./deploy.sh aws
```

## 📊 **Acesso e Monitoramento**

### URLs de Acesso

#### 📱 **Telegram Bot**
- **Desenvolvimento**: Bot local ativo
- **Produção**: Bot 24/7 no Telegram
- **Comandos**: `/start`, `/help`, `/status`

#### 🌐 **Interface Web (SafeBot)**
- **Desenvolvimento**: http://localhost:7777 (`python agent.py` ou `python safebot.py web`)
- **Produção**: http://localhost:8000
- **Nuvem**: https://your-domain.com

#### 🎨 **Frontend (UI) - Opcional**
- **Desenvolvimento**: http://localhost:3000
- **Produção**: http://localhost:3000 (ou porta configurada)

### Health Checks
- **SafeBot Local**: http://localhost:7777/health
- **SafeBot Produção**: http://localhost:8000/health
- **SafeBot Nuvem**: https://your-domain.com/health

### Endpoints Principais

#### 🌐 **Interface Web SafeBot**
- **Dashboard**: `/` - Visão geral do sistema SafeBot NR-06
- **Playground**: `/playground` - Interação com 6 agentes especializados
- **Documentação**: `/docs` - API interativa e especificações técnicas
- **Health Check**: `/health` - Monitoramento e métricas de performance
- **Agentes**: `/agents` - Lista de agentes disponíveis

#### 📱 **Telegram Bot**
- **Início**: Envie `/start` para o bot
- **Ajuda**: Envie `/help` para comandos
- **Status**: Envie `/status` para informações da sessão

## 🏗️ **Arquitetura do Sistema**

### Desenvolvimento
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ SafeBot Web UI  │───▶│ SafeBot Agents  │───▶│ Base Normas SST │
│   (Port 3000)   │    │  (Port 7777)    │    │ NRs + PgVector  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (GPT-4/3.5)   │
                       └─────────────────┘
```

### Produção
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Load Balancer  │───▶│ SafeBot Web UI  │    │ SafeBot Agents  │
│   (Port 80/443) │    │   (Port 3000)   │───▶│  (Port 8000)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              ▼
                       │   Redis Cache   │    ┌─────────────────┐
                       │ Sessões/Estado  │◀───│ Base Normas SST │
                       └─────────────────┘    │ NRs + PgVector  │
                                              └─────────────────┘
```

## 🔧 **Configuração**

### Sistema Backend - Variáveis Essenciais
```bash
# Obrigatórias
OPENAI_API_KEY=sk-...           # Chave da OpenAI para agentes IA

# Para Telegram (opcional)
TELEGRAM_TOKEN=123456:ABC...    # Token do bot do Telegram

# Para produção
ENVIRONMENT=production          # Ambiente: development/production
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/safebot
```

### Sistema Backend - Configurações Avançadas
```bash
SENTRY_DSN=https://...         # Monitoramento de erros e performance
REDIS_URL=redis://redis:6379/0 # Cache de sessões e dados
SECRET_KEY=your_secret_key     # Chave de segurança da aplicação
LOG_LEVEL=INFO                 # Nível de logging: DEBUG/INFO/WARNING/ERROR
```

### Interface Web - Configuração
```bash
# .env.local na pasta ui/
NEXT_PUBLIC_API_URL=http://localhost:7777  # Backend em desenvolvimento
# ou
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend em produção
NEXT_PUBLIC_APP_NAME="SafeBot"            # Nome da aplicação
```

## 📦 **Stack Tecnológico**

### Backend (Sistema de Agentes)
- **API Framework**: `fastapi`, `uvicorn` - API REST de alta performance
- **Database**: `postgresql`, `sqlalchemy`, `lancedb` - Dados relacionais e vetoriais
- **IA & ML**: `openai`, `langchain`, `pypdf` - Processamento de linguagem natural
- **Infraestrutura**: `docker`, `redis`, `nginx` - Containerização e cache

### Frontend (Interface Web)
- **Framework**: `next.js`, `react` - Interface moderna e responsiva
- **Styling**: `tailwindcss`, `shadcn/ui` - Design system consistente
- **Estado**: `zustand` - Gerenciamento de estado simples
- **Desenvolvimento**: `typescript`, `eslint`, `prettier` - Qualidade de código

### Ferramentas de Desenvolvimento
- **Containerização**: Docker & Docker Compose
- **Monitoramento**: Sentry, Prometheus (opcional)
- **Deploy**: Scripts automatizados, CI/CD ready

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

### Sistema SafeBot
```bash
# Iniciar Telegram Bot
cd agent/
python safebot.py telegram
# ou
python telegram_bot.py

# Iniciar Interface Web
python safebot.py web
# ou
python agent.py

# Carregar base de conhecimento
python safebot.py load-kb

# Informações do sistema
python safebot.py info

# Monitorar logs (Docker)
docker-compose -f docker-compose.prod.yml logs -f

# Backup da base SafeBot
docker exec pgvector pg_dump -U ai ai > safebot_backup_$(date +%Y%m%d).sql
```

### Interface Web
```bash
# Iniciar interface de desenvolvimento
cd ui/
npm run dev

# Construir versão otimizada
npm run build && npm start

# Verificar qualidade do código
npm run lint && npm run type-check
```

### Monitoramento do Sistema
```bash
# Performance dos containers
docker stats

# Status das portas
lsof -i :3000  # Interface Web
lsof -i :7777  # Sistema Backend (dev)
lsof -i :8000  # Sistema Backend (prod)

# Health check completo
curl http://localhost:7777/health && curl http://localhost:3000
```

## 🆘 **Troubleshooting**

### Sistema Backend

#### Erro: "Docker não conecta"
```bash
# Verificar status do Docker
docker info

# Reiniciar Docker (macOS/Linux)
# macOS: Docker Desktop > Restart
# Linux: sudo systemctl restart docker
```

#### Erro: "Dependências Python"
```bash
# Reinstalar ambiente Python
cd agent/
poetry env remove python
poetry install
```

#### Erro: "Base de dados indisponível"
```bash
# Verificar containers
docker ps | grep pgvector

# Testar conexão direta
docker exec pgvector psql -U ai -d ai -c "SELECT version();"
```

### Interface Web

#### Erro: "Módulos não encontrados"
```bash
# Limpar e reinstalar dependências
cd ui/
rm -rf node_modules package-lock.json .next
npm install
```

#### Erro: "Porta 3000 em uso"
```bash
# Liberar porta
lsof -ti:3000 | xargs kill -9

# Usar porta alternativa
npm run dev -- -p 3001
```

#### Erro: "Falha na conexão com API"
```bash
# Verificar backend
curl http://localhost:7777/health

# Verificar configuração
echo $NEXT_PUBLIC_API_URL

# Verificar logs do sistema
docker-compose logs nr06-playground
```

## 🔄 **Workflow de Desenvolvimento**

### Setup Inicial do Projeto
```bash
# 1. Clonar e configurar
git clone <repository-url>
cd aci

# 2. Configurar Sistema Backend
cd agent/
poetry install
cp env.example .env
# Adicionar sua OPENAI_API_KEY no arquivo .env

# 3. Configurar Interface Web
cd ../ui/
npm install
# Configurar NEXT_PUBLIC_API_URL se necessário
```

### Rotina de Desenvolvimento
```bash
# Opção 1: Telegram Bot (Recomendado)
cd agent/
python safebot.py telegram
# Bot ativo no Telegram 24/7

# Opção 2: Interface Web + Frontend
# Terminal 1: SafeBot Backend
cd agent/
python agent.py
# ou
python safebot.py web

# Terminal 2: SafeBot Frontend (Opcional)
cd ui/
npm run dev

# Acesso: http://localhost:7777 (SafeBot Web) + http://localhost:3000 (UI)
```

### Checklist Pré-Deploy
```bash
# Verificar sistema backend
cd agent/
poetry run python -c "import agent; print('✅ Backend OK')"

# Verificar interface web
cd ui/
npm run lint && npm run type-check && npm run build
echo "✅ Frontend OK"

# Teste de integração
curl http://localhost:7777/health
```

## 📚 **Recursos e Documentação**

### Tecnologias Utilizadas
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Framework backend
- [Next.js Documentation](https://nextjs.org/docs) - Framework frontend
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - Integração IA
- [PostgreSQL + pgvector](https://github.com/pgvector/pgvector) - Base vetorial
- [Docker Documentation](https://docs.docker.com/) - Containerização

### Normas Regulamentadoras e SST
- [Normas Regulamentadoras - Ministério do Trabalho](https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/seguranca-e-saude-no-trabalho/ctpp-nrs)
- [ISO 45001 - Sistemas de Gestão de SST](https://www.iso.org/iso-45001-occupational-health-and-safety.html)
- [OHSAS 18001 - Sistemas de Gestão de Segurança](https://www.bsigroup.com/en-US/ohsas-18001-occupational-health-and-safety/)
- [CLT - Consolidação das Leis do Trabalho](http://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)

### Principais Normas Suportadas
- **NR-06**: Equipamentos de Proteção Individual (EPI)

**🛡️ SafeBot - Sistema Inteligente de Segurança do Trabalho**