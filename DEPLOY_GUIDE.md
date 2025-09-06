# 🚀 Guia de Deploy - Digital Ocean

## 📋 **Pré-requisitos**

### **1. Recursos da VM Digital Ocean**
- **Droplet**: Ubuntu 22.04 LTS
- **Tamanho Mínimo**: 2 vCPUs, 4GB RAM, 50GB SSD
- **Tamanho Recomendado**: 4 vCPUs, 8GB RAM, 100GB SSD
- **Região**: Próxima aos usuários finais

### **2. Preparação Inicial da VM**

```bash
# Conectar via SSH
ssh root@your-vm-ip

# Atualizar sistema
apt update && apt upgrade -y

# Instalar dependências básicas
apt install -y curl wget git nano htop unzip

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install -y docker-compose-plugin

# Configurar usuário para Docker
usermod -aG docker $USER

# Configurar firewall
ufw allow 22     # SSH
ufw allow 80     # HTTP  
ufw allow 443    # HTTPS
ufw --force enable
```

---

## 🛠️ **Processo de Deploy**

### **Passo 1: Clonar e Configurar**

```bash
# Clonar repositório
git clone <seu-repositorio-url> nr06-system
cd nr06-system

# Verificar se o PDF da NR-06 está presente
ls -la data/pdfs/nr-06-atualizada-2022-1.pdf

# Configurar environment
cp production.env .env

# Editar variáveis de ambiente
nano .env
```

**Configuração obrigatória do `.env`:**
```bash
ENVIRONMENT=production
OPENAI_API_KEY=sk-proj-your-real-openai-key-here
DATABASE_URL=postgresql+psycopg://ai:ai@pgvector:5432/ai
REDIS_URL=redis://redis:6379/0
```

### **Passo 2: Deploy com Docker Compose**

```bash
# Dar permissão de execução ao script
chmod +x deploy.sh

# Executar deploy de produção
./deploy.sh production
```

**O que acontece durante o deploy:**
1. ✅ Build da imagem Docker da aplicação
2. ✅ Iniciação do PgVector (PostgreSQL + Vector extension)
3. ✅ Iniciação do Redis para cache
4. ✅ Iniciação do Nginx como proxy reverso
5. ✅ Carregamento da knowledge base da NR-06
6. ✅ Verificação de health checks

### **Passo 3: Verificação do Deploy**

```bash
# Verificar status dos containers
docker-compose -f docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker-compose.prod.yml logs -f

# Testar health check
curl http://localhost:8000/health

# Testar aplicação
curl http://localhost:8000/
```

**Saída esperada do health check:**
```json
{
  "status": "healthy",
  "service": "nr06-playground", 
  "agents_count": 6,
  "knowledge_base": "loaded",
  "memory_enabled": true,
  "version": "1.0.0"
}
```

---

## 🌐 **Configuração de Acesso Externo**

### **1. Acesso via IP Público**
```bash
# Descobrir IP público da VM
curl ifconfig.me

# Acessar aplicação
http://YOUR-VM-IP/playground
```

### **2. Configuração de Domínio (Opcional)**

```bash
# 1. Configurar DNS
# Criar registro A: your-domain.com → VM-IP

# 2. Atualizar nginx.conf
nano nginx.conf
# Alterar: server_name your-domain.com;

# 3. Configurar SSL gratuito
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com

# 4. Reiniciar nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

---

## 🔧 **Comandos de Manutenção**

### **Operações Básicas**
```bash
# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Iniciar serviços
docker-compose -f docker-compose.prod.yml up -d

# Restart de um serviço específico
docker-compose -f docker-compose.prod.yml restart nr06-playground

# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f nr06-playground
```

### **Atualizações**
```bash
# Atualizar código
git pull origin main

# Rebuild e restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Recarregar knowledge base (se necessário)
docker-compose -f docker-compose.prod.yml exec nr06-playground python agent.py load
```

### **Backup e Restore**
```bash
# Backup do PostgreSQL
docker-compose -f docker-compose.prod.yml exec pgvector pg_dump -U ai ai > backup-$(date +%Y%m%d).sql

# Backup dos volumes
docker run --rm -v nr06_pgvector_data:/data -v $(pwd):/backup alpine tar czf /backup/volumes-backup-$(date +%Y%m%d).tar.gz /data

# Restore (se necessário)
cat backup-20241201.sql | docker-compose -f docker-compose.prod.yml exec -T pgvector psql -U ai -d ai
```

---

## 📊 **Monitoramento**

### **Health Checks Automáticos**
- **Aplicação**: Verifica a cada 30s se `/health` responde
- **PostgreSQL**: Verifica conexão a cada 10s
- **Redis**: Ping a cada 10s
- **Nginx**: Verifica se proxy está funcionando

### **Logs Importantes**
```bash
# Logs da aplicação
docker-compose -f docker-compose.prod.yml logs nr06-playground

# Logs do banco
docker-compose -f docker-compose.prod.yml logs pgvector

# Logs do nginx
docker-compose -f docker-compose.prod.yml logs nginx

# Logs do Redis
docker-compose -f docker-compose.prod.yml logs redis
```

### **Métricas de Sistema**
```bash
# Uso de recursos
docker stats

# Espaço em disco
df -h

# Uso de memória
free -h

# Processos Docker
docker ps
```

---

## 🆘 **Troubleshooting**

### **Problemas Comuns**

#### **1. Container não inicia**
```bash
# Verificar logs de erro
docker-compose -f docker-compose.prod.yml logs container-name

# Verificar configurações
docker-compose -f docker-compose.prod.yml config
```

#### **2. Knowledge base não carrega**
```bash
# Verificar se PDF existe
ls -la data/pdfs/nr-06-atualizada-2022-1.pdf

# Recarregar manualmente
docker-compose -f docker-compose.prod.yml exec nr06-playground python agent.py load
```

#### **3. Erro de conexão com banco**
```bash
# Verificar se PostgreSQL está rodando
docker-compose -f docker-compose.prod.yml ps pgvector

# Testar conexão
docker-compose -f docker-compose.prod.yml exec pgvector psql -U ai -d ai -c "SELECT version();"
```

#### **4. Aplicação não responde**
```bash
# Verificar se porta está aberta
netstat -tlnp | grep :8000

# Restart da aplicação
docker-compose -f docker-compose.prod.yml restart nr06-playground

# Verificar health check interno
docker-compose -f docker-compose.prod.yml exec nr06-playground curl localhost:8000/health
```

---

## 🔄 **Processo de Rollback**

```bash
# 1. Parar serviços atuais
docker-compose -f docker-compose.prod.yml down

# 2. Voltar para commit anterior
git checkout HEAD~1

# 3. Rebuild e restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 4. Verificar funcionamento
curl http://localhost:8000/health
```

---

## 📞 **Suporte e Documentação**

- **Agno Framework**: https://docs.agno.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Digital Ocean**: https://docs.digitalocean.com/

Este guia cobre todo o processo de deploy e manutenção do sistema NR-06 em produção na Digital Ocean.
