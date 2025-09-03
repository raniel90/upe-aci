#!/bin/bash
# Script de deployment para NR-06 System
# Seguindo boas práticas oficiais do Agno

set -e  # Parar em caso de erro

echo "🛡️  NR-06 SYSTEM DEPLOYMENT"
echo "=" * 50

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Verificar variáveis de ambiente obrigatórias
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY não está definida"
    echo "💡 Execute: export OPENAI_API_KEY=your_api_key"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# Função para desenvolvimento local
deploy_local() {
    echo "🔧 Deployment LOCAL (seguindo padrão Agno)"
    
    # Iniciar PgVector (imagem oficial Agno)
    echo "📦 Iniciando PgVector database..."
    docker run -d \
        -e POSTGRES_DB=ai \
        -e POSTGRES_USER=ai \
        -e POSTGRES_PASSWORD=ai \
        -e PGDATA=/var/lib/postgresql/data/pgdata \
        -v pgvolume:/var/lib/postgresql/data \
        -p 5532:5432 \
        --name pgvector \
        agnohq/pgvector:16 || echo "PgVector já está rodando"
    
    # Aguardar database estar pronto
    echo "⏳ Aguardando database estar pronto..."
    sleep 10
    
    # Carregar knowledge base
    echo "📚 Carregando knowledge base..."
    python playground.py load
    
    # Iniciar aplicação
    echo "🚀 Iniciando NR-06 Playground..."
    python playground.py
}

# Função para produção com Docker Compose
deploy_production() {
    echo "🏭 Deployment PRODUÇÃO (Docker Compose)"
    
    # Build da imagem
    echo "🔨 Building production image..."
    docker-compose -f docker-compose.prod.yml build
    
    # Iniciar serviços
    echo "🚀 Iniciando serviços de produção..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Aguardar serviços estarem prontos
    echo "⏳ Aguardando serviços estarem prontos..."
    sleep 30
    
    # Carregar knowledge base em produção
    echo "📚 Carregando knowledge base em produção..."
    docker-compose -f docker-compose.prod.yml exec nr06-playground python playground.py load
    
    # Mostrar status
    echo "📊 Status dos serviços:"
    docker-compose -f docker-compose.prod.yml ps
    
    echo "✅ Deployment concluído!"
    echo "🌐 Aplicação disponível em: http://localhost:8000"
    echo "📊 Health check: http://localhost:8000/health"
    echo "📖 API docs: http://localhost:8000/docs"
}

# Função para AWS (usando padrões Agno CLI)
deploy_aws() {
    echo "☁️  Deployment AWS (seguindo padrão Agno)"
    echo "⚠️  Este método requer configuração do Agno CLI"
    echo "📖 Consulte: https://docs.agno.com/workspaces/workspace-management/production-app"
    
    # Verificar se ag CLI está instalado
    if ! command -v ag &> /dev/null; then
        echo "❌ Agno CLI não encontrado"
        echo "💡 Instale com: pip install agno-cli"
        exit 1
    fi
    
    # Build e deploy com Agno CLI
    echo "🔨 Building production image para AWS..."
    ag ws up --env prd --infra aws --type image
    
    echo "🚀 Deploying para AWS..."
    ag ws up --env prd --infra aws
    
    echo "✅ Deployment AWS concluído!"
}

# Menu de opções
case "${1:-local}" in
    "local")
        deploy_local
        ;;
    "production")
        deploy_production
        ;;
    "aws")
        deploy_aws
        ;;
    *)
        echo "Usage: $0 {local|production|aws}"
        echo ""
        echo "Opções:"
        echo "  local      - Deployment local com PgVector"
        echo "  production - Deployment produção com Docker Compose"
        echo "  aws        - Deployment AWS com Agno CLI"
        exit 1
        ;;
esac
