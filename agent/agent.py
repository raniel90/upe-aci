"""
NR-06 Operational Playground - Sistema Operacional para Equipamentos de Proteção Individual
Casos de uso práticos baseados na Norma Regulamentadora 06
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.tools.python import PythonTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from dotenv import load_dotenv

load_dotenv()

agent_storage: str = "tmp/agents.db"

# =============================================================================
# CONFIGURAÇÃO DE MEMÓRIA E KNOWLEDGE BASE
# =============================================================================

# Vector database para knowledge base
vector_db = LanceDb(
    table_name="pdf_documents",
    uri="tmp/lancedb",
)

# Função para criar memória especializada para cada agente
def create_agent_memory(agent_name: str, memory_description: str):
    """Cria memória específica para cada agente especializado"""
    return Memory(
        model=OpenAIChat(id="gpt-4o-mini"),
        db=SqliteMemoryDb(
            table_name=f"{agent_name}_memories", 
            db_file="tmp/agent_memories.db"
        ),
        # Configurações de memória otimizadas
        delete_memories=False,  # Mantém histórico para aprendizado
        clear_memories=False,   # Preserva conhecimento acumulado
    )

pdf_knowledge_base = PDFKnowledgeBase(
    path=[
        {
            "path": "data/pdfs/nr-06-atualizada-2022-1.pdf",
            "metadata": {
                "document_type": "norma_regulamentadora",
                "nr_number": "06",
                "year": 2022,
                "topic": "equipamentos_protecao_individual",
                "language": "portuguese",
            },
        }
    ],
    vector_db=vector_db,
)

# =============================================================================
# AGENTES ESPECIALIZADOS EM CASOS OPERACIONAIS NR-06
# =============================================================================

# 1. AGENTE SELEÇÃO DE EPIs
epi_selector = Agent(
    name="🎯 Seletor de EPIs",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("epi_selector", "Memória de seleções de EPIs e padrões de risco"),
    user_id="epi_specialist",  # ID para agrupar memórias
    instructions=[
        "Você é especialista em SELEÇÃO DE EPIs conforme NR-06",
        "MEMÓRIA: Lembre-se de seleções anteriores para padrões similares de risco",
        "APRENDIZADO: Use experiências passadas para melhorar recomendações futuras",
        "PROCESSO: Analise os riscos → Recomende EPIs específicos → Justifique legalmente",
        "FORMATO: Use tabela com colunas: Risco Identificado | EPI Recomendado | Artigo NR-06 | Observações",
        "DETALHES: Inclua tipo de CA, especificações técnicas, periodicidade de troca",
        "FOCO: Seja prático e específico para implementação imediata",
        "Sempre cite artigos específicos da NR-06 que fundamentam a recomendação"
    ],
    storage=SqliteStorage(table_name="epi_selector", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 2. AGENTE AUDITORIA DE CONFORMIDADE  
audit_agent = Agent(
    name="📋 Auditor NR-06",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("audit_agent", "Memória de auditorias, não conformidades e padrões por setor"),
    user_id="audit_specialist",
    instructions=[
        "Você é especialista em AUDITORIA DE CONFORMIDADE NR-06",
        "MEMÓRIA: Lembre-se de auditorias anteriores e padrões de não conformidade por setor",
        "APRENDIZADO: Use histórico para identificar pontos críticos recorrentes",
        "PROCESSO: Gere checklists → Classifique não conformidades → Sugira ações corretivas",
        "FORMATO: Checklist numerado com: Item | Artigo NR-06 | Status | Criticidade | Ação Requerida",
        "CLASSIFICAÇÃO: Crítica (risco iminente) | Alta (30 dias) | Média (60 dias) | Baixa (90 dias)",
        "PERSONALIZAÇÃO: Adapte por setor/atividade específica baseado em experiências passadas",
        "Inclua prazos legais e consequências do descumprimento"
    ],
    storage=SqliteStorage(table_name="audit_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 3. AGENTE TREINAMENTOS
training_agent = Agent(
    name="🎓 Designer de Treinamentos",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("training_agent", "Memória de programas de treinamento e efetividade por cargo"),
    user_id="training_specialist",
    instructions=[
        "Você é especialista em TREINAMENTOS DE EPIs conforme NR-06",
        "MEMÓRIA: Lembre-se de programas anteriores e sua efetividade por cargo/setor",
        "EVOLUÇÃO: Aprimore treinamentos baseado no feedback e resultados passados",
        "PROCESSO: Analise função → Crie programa → Gere conteúdo → Desenvolva avaliação",
        "FORMATO: Programa com: Objetivos | Conteúdo Programático | Duração | Metodologia | Avaliação",
        "CONTEÚDO: Base legal, tipos de EPI, uso correto, conservação, limitações",
        "AVALIAÇÃO: Inclua 10 questões práticas com gabarito",
        "Personalize por cargo/função específica citando artigos da NR-06"
    ],
    storage=SqliteStorage(table_name="training_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 4. AGENTE INVESTIGAÇÃO DE ACIDENTES
incident_agent = Agent(
    name="🔍 Investigador de Acidentes",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("incident_agent", "Memória de acidentes investigados e padrões de causas"),
    user_id="incident_specialist",
    instructions=[
        "Você é especialista em INVESTIGAÇÃO DE ACIDENTES relacionados a EPIs",
        "MEMÓRIA: Lembre-se de acidentes similares e padrões de causas identificados",
        "PADRÕES: Identifique tendências recorrentes para prevenção proativa",
        "PROCESSO: Analise o acidente → Identifique falhas → Determine responsabilidades → Sugira prevenção",
        "ANÁLISE: Falhas em: seleção, fornecimento, treinamento, uso, fiscalização, manutenção",
        "RESPONSABILIDADES: Cite artigos da NR-06 sobre obrigações empregador/empregado",
        "FORMATO: Relatório estruturado para CAT com causas, responsáveis e medidas preventivas",
        "FOCO: Prevenção de recorrência baseada na legislação e experiências anteriores"
    ],
    storage=SqliteStorage(table_name="incident_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 5. AGENTE CONSULTOR LEGAL
legal_agent = Agent(
    name="⚖️ Consultor Legal NR-06",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("legal_agent", "Memória de consultas legais e interpretações jurídicas"),
    user_id="legal_specialist",
    instructions=[
        "Você é especialista em ASPECTOS LEGAIS da NR-06",
        "MEMÓRIA: Lembre-se de consultas anteriores e interpretações jurídicas estabelecidas",
        "CONSISTÊNCIA: Mantenha coerência nas orientações legais para casos similares",
        "PROCESSO: Identifique situação → Cite base legal → Explique responsabilidades → Oriente ação",
        "RESPONSABILIDADES: Diferencie claramente obrigações empregador vs empregado",
        "CONSEQUÊNCIAS: Explique multas, sanções e implicações trabalhistas",
        "FORMATO: Parecer legal estruturado com fundamentação na NR-06",
        "ORIENTAÇÃO: Forneça passos práticos para regularização baseados em casos anteriores"
    ],
    storage=SqliteStorage(table_name="legal_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 6. AGENTE GERADOR DE PROCEDIMENTOS
procedure_agent = Agent(
    name="📝 Gerador de POPs",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    memory=create_agent_memory("procedure_agent", "Memória de procedimentos criados e melhores práticas"),
    user_id="procedure_specialist",
    tools=[PythonTools()],  # Para cálculos e formatação
    instructions=[
        "Você é especialista em PROCEDIMENTOS OPERACIONAIS para gestão de EPIs",
        "MEMÓRIA: Lembre-se de procedimentos anteriores e adaptações bem-sucedidas",
        "OTIMIZAÇÃO: Aprimore POPs baseado em implementações passadas e feedback",
        "PROCESSO: Analise necessidade → Crie procedimento → Inclua formulários → Defina controles",
        "PROCEDIMENTOS: Recebimento, distribuição, treinamento, uso, manutenção, substituição",
        "FORMATO: POP estruturado com: Objetivo | Responsáveis | Procedimento | Registros | Anexos",
        "BASE LEGAL: Fundamente todos os passos em artigos da NR-06",
        "CONTROLES: Inclua indicadores e formas de monitoramento baseados em experiências anteriores"
    ],
    storage=SqliteStorage(table_name="procedure_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# =============================================================================
# PLAYGROUND CONFIGURATION
# =============================================================================

# Lista de todos os agentes especializados
ALL_AGENTS = [
    epi_selector,      # Seleção de EPIs
    audit_agent,       # Auditoria de conformidade
    training_agent,    # Treinamentos personalizados
    incident_agent,    # Investigação de acidentes
    legal_agent,       # Consultoria legal
    procedure_agent,   # Geração de POPs
]

playground_app = Playground(agents=ALL_AGENTS)
app = playground_app.get_app()

def load_knowledge_base():
    """Carrega a base de conhecimento da NR-06 (executar uma vez)"""
    print("🔄 Carregando base de conhecimento da NR-06...")
    pdf_knowledge_base.load(recreate=True)
    print("✅ Base de conhecimento carregada com sucesso!")

# =============================================================================
# HEALTH CHECK ENDPOINT (Requerido para produção)
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint para monitoramento de produção"""
    return {
        "status": "healthy",
        "service": "nr06-playground",
        "agents_count": len(ALL_AGENTS),
        "knowledge_base": "loaded",
        "memory_enabled": True,
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint com informações do sistema"""
    return {
        "message": "🛡️ NR-06 Operational Playground",
        "description": "Sistema operacional para Equipamentos de Proteção Individual",
        "agents": [agent.name for agent in ALL_AGENTS],
        "playground_url": "/playground",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import sys
    import os
    
    # Detectar ambiente
    environment = os.getenv("ENVIRONMENT", "development")
    
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        load_knowledge_base()
    else:
        print("🛡️  NR-06 OPERATIONAL PLAYGROUND")
        print("=" * 50)
        print(f"🌍 Environment: {environment}")
        print("📚 AGENTES ESPECIALIZADOS DISPONÍVEIS:")
        print("  🎯 Seletor de EPIs - Recomenda EPIs por risco")
        print("  📋 Auditor NR-06 - Gera checklists de auditoria")  
        print("  🎓 Designer de Treinamentos - Cria programas de capacitação")
        print("  🔍 Investigador de Acidentes - Analisa acidentes com EPIs")
        print("  ⚖️  Consultor Legal - Esclarece aspectos legais")
        print("  📝 Gerador de POPs - Cria procedimentos operacionais")
        print("=" * 50)
        print("💡 Para carregar a base de conhecimento: python agent.py load")
        print("🚀 Iniciando playground...")
        
        # Configuração baseada no ambiente
        if environment == "production":
            # Produção: usar configurações otimizadas
            playground_app.serve(
                app="playground:app", 
                host="0.0.0.0",
                port=8000,
                reload=False,
                access_log=True
            )
        else:
            # Desenvolvimento: usar reload
            playground_app.serve(
                app="playground:app", 
                reload=True,
                port=7777  # Porta padrão Agno para desenvolvimento
            )
