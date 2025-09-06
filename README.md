# 🤖 SafeBot - Sistema Inteligente de Segurança do Trabalho

Sistema inteligente para análise de normas regulamentadoras em Saúde e Segurança do Trabalho (SST). Uma plataforma especializada que utiliza inteligência artificial para interpretar, auditar e garantir conformidade com normas regulamentadoras de SST através de agentes especializados.

## 🏗️ **Estrutura do Projeto**

```
aci/
├── agent/          # Backend - Sistema de agentes IA especializados
│   ├── agent.py
│   ├── pyproject.toml
│   ├── docker-compose.yml
│   └── ...
├── ui/             # Frontend - Interface React/Next.js moderna
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
```

## 🎯 **Agentes Especializados em SST**

- **📋 Auditor de Normas Regulamentadoras** - Analisa conformidade com NRs e identifica não conformidades
- **⚖️ Consultor em Legislação SST** - Interpreta normas regulamentadoras e legislação trabalhista
- **📝 Gerador de Procedimentos SST** - Cria POPs, PTRs e documentação técnica de segurança
- **🔍 Investigador de Acidentes** - Analisa relatórios de acidentes e identifica causas raiz
- **🎓 Designer de Treinamentos SST** - Desenvolve programas de capacitação em segurança
- **📊 Analista de Riscos Ocupacionais** - Avalia riscos e categoriza perigos no ambiente de trabalho

## 🚀 **Setup e Execução**

### 🔧 **Desenvolvimento Local**

#### 1. Backend (Sistema de Agentes)
```bash
cd agent/

# Instalar dependências Python
poetry install

# Configurar ambiente
cp env.example .env
# Edite .env com sua OPENAI_API_KEY

# Executar o sistema
poetry run python agent.py
# ou usar o script de deploy
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
#### Frontend (UI)
- **Desenvolvimento**: http://localhost:3000
- **Produção**: http://localhost:3000 (ou porta configurada)

#### Backend (SafeBot API)
- **Desenvolvimento**: http://localhost:7777
- **Produção**: http://localhost:8000
- **Nuvem**: https://your-domain.com

### Health Checks
- **SafeBot Local**: http://localhost:7777/health
- **SafeBot Produção**: http://localhost:8000/health
- **SafeBot Nuvem**: https://your-domain.com/health

### Endpoints Principais
- **Dashboard SafeBot**: `/` - Interface de análise de normas regulamentadoras
- **Console de Agentes**: `/playground` - Interação com agentes SafeBot especializados
- **Documentação API**: `/docs` - API interativa e especificações técnicas
- **Status do SafeBot**: `/health` - Monitoramento e métricas de performance

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
OPENAI_API_KEY=sk-...           # Chave da OpenAI para agentes IA
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

### Sistema Backend
```bash
# Iniciar sistema de agentes
cd agent/
poetry run python agent.py

# Monitorar logs do sistema
docker-compose -f docker-compose.prod.yml logs -f

# Reiniciar sistema
docker-compose -f docker-compose.prod.yml restart nr06-playground

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
# Terminal 1: SafeBot Backend
cd agent/
poetry run python agent.py

# Terminal 2: SafeBot Frontend
cd ui/
npm run dev

# Acesse: http://localhost:3000 (SafeBot UI) + http://localhost:7777 (SafeBot API)
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
- **NR-07**: Programa de Controle Médico de Saúde Ocupacional (PCMSO)
- **NR-09**: Programa de Prevenção de Riscos Ambientais (PPRA)
- **NR-12**: Segurança no Trabalho em Máquinas e Equipamentos
- **NR-15**: Atividades e Operações Insalubres
- **NR-16**: Atividades e Operações Perigosas
- **NR-17**: Ergonomia
- **NR-18**: Condições e Meio Ambiente de Trabalho na Indústria da Construção
- **NR-23**: Proteção Contra Incêndios
- **NR-33**: Segurança e Saúde nos Trabalhos em Espaços Confinados
- **NR-35**: Trabalho em Altura

---

**🤖 SafeBot - Sistema Inteligente de Segurança do Trabalho para Normas Regulamentadoras**