"""
SafeBot Teams - Sistema Multi-Agente para NR-06
Implementação de teams colaborativos especializados em segurança do trabalho
"""
import os
from typing import Optional, List, Dict, Any
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from dotenv import load_dotenv

load_dotenv()

class SafeBotTeamsFactory:
    """Factory para criar teams SafeBot especializados em NR-06"""
    
    def __init__(self, data_dir: str = "data", tmp_dir: str = "tmp"):
        self.data_dir = data_dir
        self.tmp_dir = tmp_dir
        self._vector_db = None
        self._knowledge_base = None
        self._shared_memory = None
        
    @property
    def vector_db(self) -> LanceDb:
        """Vector database compartilhado para todos os agentes"""
        if self._vector_db is None:
            self._vector_db = LanceDb(
                table_name="pdf_documents",
                uri=f"{self.tmp_dir}/lancedb",
            )
        return self._vector_db
    
    @property
    def knowledge_base(self) -> PDFKnowledgeBase:
        """Knowledge base da NR-06 compartilhada"""
        if self._knowledge_base is None:
            self._knowledge_base = PDFKnowledgeBase(
                path=[
                    {
                        "path": f"{self.data_dir}/pdfs/nr-06-atualizada-2022-1.pdf",
                        "metadata": {
                            "document_type": "norma_regulamentadora",
                            "nr_number": "06",
                            "year": 2022,
                            "topic": "equipamentos_protecao_individual",
                            "language": "portuguese",
                        }
                    }
                ],
                vector_db=self.vector_db
            )
        return self._knowledge_base
    
    @property
    def shared_memory(self) -> Memory:
        """Memória compartilhada para teams"""
        if self._shared_memory is None:
            self._shared_memory = Memory(
                db=SqliteMemoryDb(
                    table_name="safebot_team_memory",
                    db_file=f"{self.tmp_dir}/team_memories.db"
                )
            )
        return self._shared_memory
    
    def create_base_storage(self, agent_name: str) -> SqliteStorage:
        """Cria storage individual para cada agente"""
        return SqliteStorage(
            table_name=f"safebot_{agent_name.lower().replace(' ', '_')}",
            db_file=f"{self.tmp_dir}/agents.db"
        )
    
    # ============================================================================
    # AGENTES ESPECIALIZADOS PARA TEAMS
    # ============================================================================
    
    def create_epi_specialist_agent(self) -> Agent:
        """Agente especialista em EPIs específicos"""
        return Agent(
            name="EPI Specialist",
            role="Especialista em tipos específicos de EPIs e suas aplicações",
            model=OpenAIChat(id="gpt-4o-mini"),
            knowledge=self.knowledge_base,
            storage=self.create_base_storage("epi_specialist"),
            memory=self.shared_memory,
            instructions=[
                "Você é especialista em EPIs específicos da NR-06.",
                "Foque em: tipos de EPIs, especificações técnicas, aplicações corretas.",
                "Analise requisitos específicos por tipo de trabalho e ambiente.",
                "Forneça recomendações detalhadas sobre seleção de EPIs.",
                "Cite sempre os artigos específicos da NR-06.",
                "",
                "🛡️ ESPECIALIDADES:",
                "• Proteção da cabeça (capacetes, cascos)",
                "• Proteção auditiva (protetores auriculares)",
                "• Proteção respiratória (máscaras, respiradores)",
                "• Proteção dos olhos e face (óculos, viseiras)",
                "• Proteção das mãos e braços (luvas, mangotes)",
                "• Proteção dos pés e pernas (calçados, perneiras)",
                "• Proteção do tronco (aventais, jaquetas)",
                "• Proteção contra quedas (cinturões, trava-quedas)",
            ]
        )
    
    def create_compliance_auditor_agent(self) -> Agent:
        """Agente especialista em auditoria e conformidade"""
        return Agent(
            name="Compliance Auditor",
            role="Especialista em auditoria de conformidade com NR-06",
            model=OpenAIChat(id="gpt-4o-mini"),
            knowledge=self.knowledge_base,
            storage=self.create_base_storage("compliance_auditor"),
            memory=self.shared_memory,
            instructions=[
                "Você é auditor especialista em conformidade com a NR-06.",
                "Foque em: procedimentos de auditoria, checklist de conformidade, não conformidades.",
                "Analise situações e identifique gaps de conformidade.",
                "Forneça planos de ação para adequação à norma.",
                "Cite artigos específicos da NR-06 para cada não conformidade.",
                "",
                "⚖️ ESPECIALIDADES:",
                "• Auditoria de fornecimento de EPIs",
                "• Verificação de treinamentos obrigatórios",
                "• Controle de uso e conservação",
                "• Documentação e registros exigidos",
                "• Responsabilidades do empregador e empregado",
                "• Procedimentos disciplinares",
                "• Fiscalização e penalidades",
            ]
        )
    
    def create_training_specialist_agent(self) -> Agent:
        """Agente especialista em treinamentos e capacitação"""
        return Agent(
            name="Training Specialist",
            role="Especialista em treinamentos e capacitação sobre EPIs",
            model=OpenAIChat(id="gpt-4o-mini"),
            knowledge=self.knowledge_base,
            storage=self.create_base_storage("training_specialist"),
            memory=self.shared_memory,
            instructions=[
                "Você é especialista em treinamentos sobre EPIs da NR-06.",
                "Foque em: programas de treinamento, metodologias, avaliação de competências.",
                "Desenvolva conteúdos educativos e planos de capacitação.",
                "Analise necessidades de treinamento por função e ambiente.",
                "Cite requisitos de treinamento da NR-06.",
                "",
                "📚 ESPECIALIDADES:",
                "• Treinamento inicial obrigatório",
                "• Treinamento periódico de reciclagem",
                "• Capacitação por tipo de EPI",
                "• Metodologias de ensino para adultos",
                "• Avaliação de aprendizagem",
                "• Registro e controle de treinamentos",
                "• Materiais didáticos e recursos",
            ]
        )
    
    def create_risk_analyst_agent(self) -> Agent:
        """Agente especialista em análise de riscos"""
        return Agent(
            name="Risk Analyst",
            role="Especialista em análise de riscos ocupacionais",
            model=OpenAIChat(id="gpt-4o-mini"),
            knowledge=self.knowledge_base,
            storage=self.create_base_storage("risk_analyst"),
            memory=self.shared_memory,
            tools=[DuckDuckGoTools()],
            instructions=[
                "Você é especialista em análise de riscos ocupacionais relacionados à NR-06.",
                "Foque em: identificação de riscos, avaliação de exposição, medidas de controle.",
                "Analise ambientes de trabalho e suas exposições específicas.",
                "Recomende hierarquia de controles e EPIs adequados.",
                "Busque informações atualizadas sobre novos riscos quando necessário.",
                "",
                "⚠️ ESPECIALIDADES:",
                "• Riscos físicos (ruído, vibração, radiação)",
                "• Riscos químicos (gases, vapores, poeiras)",
                "• Riscos biológicos (microorganismos, parasitas)",
                "• Riscos mecânicos (impactos, cortes, perfurações)",
                "• Riscos de queda (trabalho em altura)",
                "• Hierarquia de controles (eliminação → EPI)",
                "• Avaliação quantitativa de exposição",
            ]
        )
    
    def create_web_researcher_agent(self) -> Agent:
        """Agente para pesquisas web complementares"""
        return Agent(
            name="Web Researcher",
            role="Pesquisador web para informações complementares sobre segurança",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[DuckDuckGoTools()],
            storage=self.create_base_storage("web_researcher"),
            memory=self.shared_memory,
            instructions=[
                "Você é pesquisador web especializado em segurança do trabalho.",
                "Busque informações atualizadas sobre EPIs, tecnologias, casos práticos.",
                "Complemente informações da NR-06 com dados atuais do mercado.",
                "Verifique sempre a confiabilidade das fontes.",
                "Foque em sites oficiais, fabricantes reconhecidos e órgãos técnicos.",
                "",
                "🔍 ESPECIALIDADES:",
                "• Novos produtos e tecnologias em EPIs",
                "• Casos práticos e estudos de caso",
                "• Fabricantes e fornecedores confiáveis",
                "• Normas técnicas complementares (ABNT, ANSI, etc.)",
                "• Tendências e inovações em segurança",
                "• Jurisprudência e decisões regulatórias recentes",
            ]
        )
    
    # ============================================================================
    # TEAMS ESPECIALIZADOS
    # ============================================================================
    
    def create_comprehensive_safety_team(self) -> Team:
        """
        Team abrangente para análise completa de segurança
        Modo: COORDINATE - O líder coordena especialistas e sintetiza respostas
        """
        return Team(
            name="Comprehensive Safety Team",
            mode="coordinate",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            members=[
                self.create_epi_specialist_agent(),
                self.create_compliance_auditor_agent(),
                self.create_training_specialist_agent(),
                self.create_risk_analyst_agent(),
                self.create_web_researcher_agent(),
            ],
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "Você é o coordenador de uma equipe de especialistas em segurança do trabalho NR-06.",
                "Coordene os especialistas para fornecer análises completas e abrangentes.",
                "Sintetize as respostas dos especialistas em um relatório unificado e estruturado.",
                "Garanta que todos os aspectos da questão sejam cobertos pelos especialistas adequados.",
                "Use raciocínio estruturado para organizar e priorizar informações.",
                "",
                "📋 PROCESSO DE COORDENAÇÃO:",
                "1. Analise a questão e identifique quais especialistas devem ser consultados",
                "2. Delegue tarefas específicas para cada especialista relevante",
                "3. Colete e analise as respostas de todos os especialistas",
                "4. Sintetize em um relatório final estruturado e abrangente",
                "5. Identifique lacunas ou necessidades de informações adicionais",
                "",
                "🎯 FORMATO DE RESPOSTA:",
                "• Use seções claras para cada aspecto analisado",
                "• Inclua recomendações práticas e acionáveis",
                "• Cite artigos específicos da NR-06 quando relevante",
                "• Forneça próximos passos ou ações recomendadas",
                "• Identifique riscos ou pontos críticos de atenção",
            ],
            success_criteria="Análise completa e abrangente da questão de segurança com recomendações práticas baseadas em múltiplas especialidades.",
            enable_agentic_context=True,
            share_member_interactions=True,
            show_members_responses=True,
            markdown=True,
            add_datetime_to_instructions=True,
        )
    
    def create_quick_consultation_team(self) -> Team:
        """
        Team para consultas rápidas e específicas
        Modo: ROUTE - Direciona para o especialista mais adequado
        """
        return Team(
            name="Quick Consultation Team",
            mode="route",
            model=OpenAIChat(id="gpt-4o"),
            members=[
                self.create_epi_specialist_agent(),
                self.create_compliance_auditor_agent(),
                self.create_training_specialist_agent(),
                self.create_risk_analyst_agent(),
            ],
            instructions=[
                "Você é um roteador inteligente de consultas sobre NR-06.",
                "Analise a questão do usuário e direcione para o especialista mais adequado:",
                "",
                "🎯 CRITÉRIOS DE ROTEAMENTO:",
                "• EPI Specialist: Questões sobre tipos, seleção, especificações de EPIs",
                "• Compliance Auditor: Questões sobre conformidade, auditoria, documentação",
                "• Training Specialist: Questões sobre treinamentos, capacitação, educação",
                "• Risk Analyst: Questões sobre riscos, exposições, análise de ambiente",
                "",
                "Se a questão envolver múltiplas especialidades, encaminhe para o especialista principal e mencione a necessidade de consulta adicional.",
            ],
            show_members_responses=True,
            markdown=True,
        )
    
    def create_collaborative_research_team(self) -> Team:
        """
        Team para pesquisa colaborativa sobre tópicos complexos
        Modo: COLLABORATE - Todos os membros trabalham na mesma questão
        """
        return Team(
            name="Collaborative Research Team",
            mode="collaborate",
            model=OpenAIChat(id="gpt-4o"),
            members=[
                self.create_epi_specialist_agent(),
                self.create_risk_analyst_agent(),
                self.create_web_researcher_agent(),
            ],
            instructions=[
                "Vocês são uma equipe de pesquisa colaborativa sobre segurança do trabalho.",
                "Trabalhem juntos para pesquisar e analisar tópicos complexos relacionados à NR-06.",
                "Cada membro deve contribuir com sua perspectiva especializada.",
                "Busquem consenso e complementem as análises uns dos outros.",
                "Produzam uma resposta unificada que combine todas as perspectivas.",
                "",
                "🤝 PROCESSO COLABORATIVO:",
                "1. Cada especialista analisa a questão de sua perspectiva",
                "2. Compartilhem descobertas e insights entre si",
                "3. Identifiquem áreas de concordância e divergência",
                "4. Busquem informações adicionais quando necessário",
                "5. Construam uma resposta consensual e abrangente",
            ],
            success_criteria="Consenso da equipe sobre a análise do tópico com contribuições de todas as especialidades.",
            enable_agentic_context=True,
            show_members_responses=True,
            markdown=True,
        )

# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA
# ============================================================================

def load_knowledge_base(recreate: bool = False) -> bool:
    """Carrega a base de conhecimento NR-06"""
    try:
        factory = SafeBotTeamsFactory()
        kb = factory.knowledge_base
        
        if recreate:
            print("🔄 Recriando base de conhecimento...")
            kb.load(recreate=True)
        else:
            print("📚 Carregando base de conhecimento...")
            kb.load()
        
        print("✅ Base de conhecimento carregada com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar base de conhecimento: {e}")
        return False

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Exemplo de uso dos teams
    factory = SafeBotTeamsFactory()
    
    # Team abrangente para análise completa
    safety_team = factory.create_comprehensive_safety_team()
    
    # Exemplo de consulta
    safety_team.print_response(
        "Preciso implementar um programa de EPIs para uma obra de construção civil. "
        "Quais são os principais EPIs necessários, como fazer o treinamento dos trabalhadores "
        "e como garantir a conformidade com a NR-06?",
        stream=True
    )

