"""
Configuração de produção para o sistema NR-06
"""
import os
from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.storage.postgres import PostgresStorage
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# =============================================================================
# CONFIGURAÇÃO DE PRODUÇÃO
# =============================================================================

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nr06_user:nr06_pass@localhost:5432/nr06_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Configurar Sentry para monitoramento de erros
if SENTRY_DSN and ENVIRONMENT == "production":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=ENVIRONMENT,
    )

# Configurações de caminhos
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdfs"

# Assegurar que diretórios existem
PDF_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# CONFIGURAÇÃO DE BANCO DE DADOS DE PRODUÇÃO
# =============================================================================

def create_production_vector_db():
    """Cria vector database PostgreSQL para produção"""
    return PgVector(
        table_name="nr06_documents",
        db_url=DATABASE_URL,
        # Configurações otimizadas para produção
        search_type="cosine",
        dimensions=1536,
    )

def create_production_memory(agent_name: str):
    """Cria memória PostgreSQL para produção"""
    return Memory(
        model=OpenAIChat(id="gpt-4o-mini"),
        db=PostgresMemoryDb(
            table_name=f"{agent_name}_memories",
            db_url=DATABASE_URL
        ),
        delete_memories=False,
        clear_memories=False,
    )

def create_production_storage(table_name: str):
    """Cria storage PostgreSQL para produção"""
    return PostgresStorage(
        table_name=table_name,
        db_url=DATABASE_URL
    )

# =============================================================================
# KNOWLEDGE BASE DE PRODUÇÃO
# =============================================================================

def create_production_knowledge_base():
    """Cria knowledge base otimizado para produção"""
    vector_db = create_production_vector_db()
    
    return PDFKnowledgeBase(
        path=[{
            "path": str(PDF_DIR / "nr-06-atualizada-2022-1.pdf"),
            "metadata": {
                "document_type": "norma_regulamentadora",
                "nr_number": "06",
                "year": 2022,
                "topic": "equipamentos_protecao_individual",
                "language": "portuguese",
                "environment": ENVIRONMENT
            }
        }],
        vector_db=vector_db,
    )

# =============================================================================
# AGENTES DE PRODUÇÃO
# =============================================================================

def create_production_agents():
    """Cria todos os agentes configurados para produção"""
    knowledge_base = create_production_knowledge_base()
    
    agents = []
    
    # Configuração base para todos os agentes
    base_config = {
        "model": OpenAIChat(id="gpt-4o-mini"),
        "knowledge": knowledge_base,
        "search_knowledge": True,
        "add_datetime_to_instructions": True,
        "add_history_to_messages": True,
        "num_history_responses": 5,
        "markdown": True,
    }
    
    # 1. EPI Selector
    agents.append(Agent(
        name="🎯 Seletor de EPIs",
        memory=create_production_memory("epi_selector"),
        user_id="epi_specialist",
        storage=create_production_storage("epi_selector"),
        instructions=[
            "Você é especialista em SELEÇÃO DE EPIs conforme NR-06",
            "MEMÓRIA: Lembre-se de seleções anteriores para padrões similares de risco",
            "PROCESSO: Analise os riscos → Recomende EPIs específicos → Justifique legalmente",
            "FORMATO: Use tabela com: Risco | EPI | Artigo NR-06 | Observações",
            "Sempre cite artigos específicos da NR-06"
        ],
        **base_config
    ))
    
    # 2. Auditor
    agents.append(Agent(
        name="📋 Auditor NR-06",
        memory=create_production_memory("audit_agent"),
        user_id="audit_specialist",
        storage=create_production_storage("audit_agent"),
        instructions=[
            "Você é especialista em AUDITORIA DE CONFORMIDADE NR-06",
            "MEMÓRIA: Lembre-se de auditorias anteriores e padrões por setor",
            "PROCESSO: Gere checklists → Classifique não conformidades → Sugira ações",
            "CLASSIFICAÇÃO: Crítica | Alta (30d) | Média (60d) | Baixa (90d)",
        ],
        **base_config
    ))
    
    # 3. Training Designer
    agents.append(Agent(
        name="🎓 Designer de Treinamentos",
        memory=create_production_memory("training_agent"),
        user_id="training_specialist",
        storage=create_production_storage("training_agent"),
        instructions=[
            "Você é especialista em TREINAMENTOS DE EPIs conforme NR-06",
            "MEMÓRIA: Lembre-se de programas anteriores e efetividade",
            "PROCESSO: Analise função → Crie programa → Gere avaliação",
            "AVALIAÇÃO: Inclua 10 questões práticas com gabarito",
        ],
        **base_config
    ))
    
    # 4. Incident Investigator
    agents.append(Agent(
        name="🔍 Investigador de Acidentes",
        memory=create_production_memory("incident_agent"),
        user_id="incident_specialist",
        storage=create_production_storage("incident_agent"),
        instructions=[
            "Você é especialista em INVESTIGAÇÃO DE ACIDENTES com EPIs",
            "MEMÓRIA: Lembre-se de acidentes similares e padrões de causas",
            "PROCESSO: Analise → Identifique falhas → Determine responsabilidades",
            "FORMATO: Relatório estruturado para CAT",
        ],
        **base_config
    ))
    
    # 5. Legal Advisor
    agents.append(Agent(
        name="⚖️ Consultor Legal NR-06",
        memory=create_production_memory("legal_agent"),
        user_id="legal_specialist",
        storage=create_production_storage("legal_agent"),
        instructions=[
            "Você é especialista em ASPECTOS LEGAIS da NR-06",
            "MEMÓRIA: Mantenha consistência em interpretações jurídicas",
            "PROCESSO: Identifique situação → Cite base legal → Oriente ação",
            "FORMATO: Parecer legal estruturado",
        ],
        **base_config
    ))
    
    # 6. Procedure Generator
    agents.append(Agent(
        name="📝 Gerador de POPs",
        memory=create_production_memory("procedure_agent"),
        user_id="procedure_specialist",
        storage=create_production_storage("procedure_agent"),
        tools=[PythonTools()],
        instructions=[
            "Você é especialista em PROCEDIMENTOS OPERACIONAIS para EPIs",
            "MEMÓRIA: Lembre-se de procedimentos anteriores e otimizações",
            "PROCESSO: Analise necessidade → Crie procedimento → Defina controles",
            "FORMATO: POP estruturado com objetivos e responsáveis",
        ],
        **base_config
    ))
    
    return agents, knowledge_base

# =============================================================================
# APLICAÇÃO DE PRODUÇÃO
# =============================================================================

def create_production_app():
    """Cria aplicação configurada para produção"""
    agents, knowledge_base = create_production_agents()
    
    playground_app = Playground(
        agents=agents,
        # Configurações de produção
        debug=False if ENVIRONMENT == "production" else True,
    )
    
    app = playground_app.get_app()
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "environment": ENVIRONMENT,
            "agents_count": len(agents),
            "knowledge_base": "loaded" if knowledge_base else "not_loaded"
        }
    
    return app, knowledge_base

# Criar aplicação
app, pdf_knowledge_base = create_production_app()

def load_production_knowledge_base():
    """Carrega knowledge base em produção"""
    print("🔄 Carregando base de conhecimento NR-06 em produção...")
    pdf_knowledge_base.load(recreate=False)  # Não recriar em produção
    print("✅ Base de conhecimento carregada!")

if __name__ == "__main__":
    import sys
    import uvicorn
    
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        load_production_knowledge_base()
    else:
        print("🛡️  NR-06 PRODUCTION SYSTEM")
        print("=" * 50)
        print(f"🌍 Environment: {ENVIRONMENT}")
        print(f"🗄️  Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'SQLite'}")
        print("🚀 Starting production server...")
        
        # Configuração para desenvolvimento local
        if ENVIRONMENT != "production":
            uvicorn.run(
                "production_config:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                log_level="info"
            )
        else:
            # Em produção, usar gunicorn (configurado no Dockerfile)
            print("Use gunicorn in production (see Dockerfile)")
