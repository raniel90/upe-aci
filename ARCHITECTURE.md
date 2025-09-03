# 🏗️ Arquitetura do Sistema NR-06

## 📋 Definição de Escopo dos Componentes

### 🎯 **Visão Geral do Sistema**

O **NR-06 Operational System** é um sistema especializado em Equipamentos de Proteção Individual (EPIs) baseado na Norma Regulamentadora 06. Utiliza o framework **Agno** para criar agentes de IA especializados que automatizam processos críticos de segurança do trabalho.

---

## 🧩 **Componentes da Arquitetura**

### **1. Camada de Apresentação (Frontend)**
- **Nginx Proxy Reverso**
  - **Função**: Load balancer, SSL termination, rate limiting
  - **Portas**: 80 (HTTP), 443 (HTTPS)
  - **Recursos**: Security headers, WebSocket support, static files
  - **Configuração**: `nginx.conf`

### **2. Camada de Aplicação (Backend)**
- **NR-06 FastAPI Application**
  - **Framework**: Agno + FastAPI + Uvicorn
  - **Porta**: 8000
  - **Linguagem**: Python 3.12
  - **Arquivo Principal**: `playground.py`
  - **Configuração Produção**: `production_config.py`

#### **2.1 Agentes Especializados (6 agentes)**

| Agente | Função | Responsabilidade |
|--------|--------|------------------|
| 🎯 **EPI Selector** | Seleção de EPIs | Recomenda EPIs específicos por tipo de risco identificado |
| 📋 **Auditor NR-06** | Auditoria de Conformidade | Gera checklists e classifica não conformidades |
| 🎓 **Training Designer** | Treinamentos | Cria programas de capacitação personalizados |
| 🔍 **Incident Investigator** | Investigação de Acidentes | Analisa acidentes relacionados a EPIs |
| ⚖️ **Legal Advisor** | Consultoria Legal | Esclarece aspectos legais da NR-06 |
| 📝 **POP Generator** | Procedimentos | Cria procedimentos operacionais padrão |

### **3. Camada de Dados (Data Layer)**

#### **3.1 Banco de Dados Principal**
- **PgVector (PostgreSQL 15 + Vector Extension)**
  - **Função**: Armazenamento de dados estruturados e embeddings
  - **Porta**: 5432
  - **Imagem**: `agnohq/pgvector:16` (oficial Agno)
  - **Dados**: Agentes, memórias, knowledge base

#### **3.2 Cache e Sessões**
- **Redis 7**
  - **Função**: Cache de aplicação, sessões de usuário
  - **Porta**: 6379
  - **Persistência**: AOF habilitado
  - **Configuração**: 256MB max memory, LRU eviction

#### **3.3 Armazenamento de Conhecimento**
- **Knowledge Base (PDF)**
  - **Arquivo**: `data/pdfs/nr-06-atualizada-2022-1.pdf`
  - **Processamento**: PyPDF para extração de texto
  - **Vetorização**: OpenAI Embeddings (text-embedding-ada-002)

- **Vector Database (LanceDB)**
  - **Localização**: `tmp/lancedb/`
  - **Tabelas**: `pdf_documents`, `agno_docs`
  - **Função**: Busca semântica de documentos

#### **3.4 Memória dos Agentes**
- **SQLite Local (Desenvolvimento)**
  - **Arquivo**: `tmp/agent_memories.db`
  - **Tabelas**: Uma por agente (ex: `epi_selector_memories`)

- **PostgreSQL (Produção)**
  - **Integração**: PostgresMemoryDb
  - **Persistência**: Memórias dos agentes entre sessões

### **4. Camada de Integração Externa**

#### **4.1 APIs Externas**
- **OpenAI API**
  - **Modelo**: GPT-4o-mini
  - **Função**: Processamento de linguagem natural
  - **Autenticação**: `OPENAI_API_KEY`

#### **4.2 Monitoramento (Opcional)**
- **Sentry**
  - **Função**: Error tracking, performance monitoring
  - **Integração**: FastAPI integration
  - **Configuração**: `SENTRY_DSN`

---

## 🔧 **Tecnologias e Dependências**

### **Core Framework**
```python
agno = "*"                    # Framework principal de agentes
fastapi = "^0.116.1"         # API REST
uvicorn = "^0.35.0"          # ASGI server
gunicorn = "^23.0.0"         # Production WSGI server
```

### **IA e Processamento**
```python
openai = "^1.102.0"          # Integração OpenAI
pypdf = "^5.1.0"             # Processamento de PDFs
lancedb = "^0.24.3"          # Vector database
```

### **Banco de Dados**
```python
sqlalchemy = "^2.0.43"       # ORM
psycopg2-binary = "^2.9.9"   # PostgreSQL driver
redis = "^5.0.0"             # Cache client
```

### **Produção e Monitoramento**
```python
sentry-sdk = "^2.0.0"        # Error monitoring
prometheus-client = "^0.20.0" # Metrics
python-dotenv = "^1.0.0"     # Environment variables
```

---

## 🚀 **Estratégia de Deployment - Digital Ocean**

### **1. Preparação da VM**

#### **1.1 Especificações Mínimas Recomendadas**
- **CPU**: 2 vCPUs
- **RAM**: 4 GB
- **Storage**: 50 GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Network**: 1 Gbps

#### **1.2 Preparação do Ambiente**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker e Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose-plugin

# Configurar firewall
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### **2. Deploy do Projeto**

#### **2.1 Clonagem e Configuração**
```bash
# Clonar repositório
git clone <seu-repositorio> nr06-system
cd nr06-system

# Configurar environment
cp production.env .env
nano .env  # Configurar OPENAI_API_KEY e outras variáveis

# Garantir que o PDF da NR-06 está presente
ls -la data/pdfs/nr-06-atualizada-2022-1.pdf
```

#### **2.2 Execução do Deploy**
```bash
# Dar permissão de execução
chmod +x deploy.sh

# Executar deploy de produção
./deploy.sh production
```

#### **2.3 Verificação do Deploy**
```bash
# Verificar serviços rodando
docker-compose -f docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker-compose.prod.yml logs -f

# Testar health check
curl http://localhost:8000/health

# Testar aplicação
curl http://localhost:8000/
```

### **3. Configurações de Produção**

#### **3.1 Variáveis de Ambiente Obrigatórias**
```bash
# .env file
ENVIRONMENT=production
OPENAI_API_KEY=sk-proj-your-key-here
DATABASE_URL=postgresql+psycopg://ai:ai@pgvector:5432/ai
REDIS_URL=redis://redis:6379/0
```

#### **3.2 Configurações Opcionais de Segurança**
```bash
# Monitoramento
SENTRY_DSN=https://your-sentry-dsn-here

# SSL (se configurar certificados)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### **4. Acesso e URLs**

#### **4.1 URLs de Acesso**
- **Aplicação Principal**: `http://your-vm-ip:80/playground`
- **API Documentation**: `http://your-vm-ip:80/docs`
- **Health Check**: `http://your-vm-ip:80/health`
- **Root Info**: `http://your-vm-ip:80/`

#### **4.2 Configuração de Domínio (Opcional)**
```bash
# Configurar DNS
# your-domain.com → VM IP

# Atualizar nginx.conf
server_name your-domain.com;

# Configurar SSL com Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 **Características de Segurança**

### **Implementadas**
- ✅ **Containers não-root**: Usuário `appuser` (UID 1000)
- ✅ **Health checks**: Monitoramento automático de serviços
- ✅ **Rate limiting**: 10 req/s via Nginx
- ✅ **Security headers**: X-Frame-Options, X-Content-Type-Options
- ✅ **Environment isolation**: Variáveis separadas por ambiente
- ✅ **Restart policies**: `unless-stopped` para todos os serviços

### **Recomendações Adicionais**
- 🔒 **SSL/TLS**: Configurar certificados para HTTPS
- 🛡️ **Firewall**: Restringir acesso apenas a portas necessárias
- 📊 **Monitoring**: Implementar Sentry para error tracking
- 🔑 **Secrets Management**: Usar Docker secrets ou vault
- 📝 **Backup**: Configurar backup automático dos volumes

---

## 📊 **Monitoramento e Manutenção**

### **Health Checks**
```bash
# Verificar status dos serviços
docker-compose -f docker-compose.prod.yml ps

# Verificar health endpoint
curl http://localhost:8000/health

# Verificar logs
docker-compose -f docker-compose.prod.yml logs -f nr06-playground
```

### **Backup de Dados**
```bash
# Backup do PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U ai ai > backup.sql

# Backup dos volumes
docker run --rm -v nr06_pgvector_data:/data -v $(pwd):/backup alpine tar czf /backup/pgvector_backup.tar.gz /data
```

### **Escalabilidade**
```bash
# Escalar horizontalmente
docker-compose -f docker-compose.prod.yml up --scale nr06-playground=3

# Monitorar recursos
docker stats
```

---

## 🎯 **Casos de Uso Operacionais**

### **Fluxo de Trabalho Típico**
1. **Usuário acessa** `/playground`
2. **Seleciona agente** especializado conforme necessidade
3. **Interage via chat** com conhecimento da NR-06
4. **Agente processa** com memória e conhecimento específico
5. **Retorna resultado** estruturado e fundamentado legalmente

### **Exemplos de Interação**
- "Preciso selecionar EPIs para soldador em ambiente confinado"
- "Gere checklist de auditoria para indústria química"
- "Crie treinamento de EPI para operadores de empilhadeira"
- "Investigue acidente por falha no uso de capacete"
- "Esclareça responsabilidades legais do empregador"
- "Crie POP para distribuição de EPIs"

---

## 📁 **Estrutura de Arquivos Críticos**

```
/Users/sroa/Documents/gitworkspace/phd/aci/
├── 🐳 docker-compose.prod.yml    # Orquestração de produção
├── 🐳 Dockerfile                # Build da aplicação
├── 🌐 nginx.conf                # Configuração proxy
├── 🚀 deploy.sh                 # Script de deployment
├── 🛡️ playground.py            # Aplicação principal
├── ⚙️ production_config.py      # Configuração produção
├── 📄 production.env           # Variáveis ambiente
├── 📊 pyproject.toml           # Dependências Python
└── 📁 data/pdfs/              # Knowledge base (NR-06)
    └── nr-06-atualizada-2022-1.pdf
```

---

## ✅ **Checklist de Deploy na Digital Ocean**

### **Pré-Deploy**
- [ ] VM criada com especificações mínimas
- [ ] Docker e Docker Compose instalados
- [ ] Firewall configurado (22, 80, 443)
- [ ] Repositório clonado
- [ ] Arquivo `.env` configurado com `OPENAI_API_KEY`
- [ ] PDF da NR-06 presente em `data/pdfs/`

### **Deploy**
- [ ] `./deploy.sh production` executado com sucesso
- [ ] Todos os containers rodando: `docker-compose ps`
- [ ] Health check respondendo: `curl localhost:8000/health`
- [ ] Knowledge base carregada
- [ ] Playground acessível via browser

### **Pós-Deploy**
- [ ] Configurar backup automático
- [ ] Configurar monitoramento (Sentry)
- [ ] Configurar SSL se necessário
- [ ] Testar todos os 6 agentes especializados
- [ ] Documentar URLs de acesso

---

## 🔄 **Comandos de Manutenção**

```bash
# Restart completo
docker-compose -f docker-compose.prod.yml restart

# Update da aplicação
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Backup rápido
./backup.sh  # (criar script separado)

# Recarregar knowledge base
docker-compose -f docker-compose.prod.yml exec nr06-playground python playground.py load
```

Este documento define a arquitetura completa do sistema, componentes utilizados e estratégia de deployment otimizada para Digital Ocean com Docker Compose.
