"""
SafeBot NR-06 - Web Application
Interface web usando Agno Playground para agentes especializados em NR-06
"""
import os
import sys
from typing import List
from agno.agent import Agent
from agno.playground import Playground
from agno.tools.python import PythonTools
from dotenv import load_dotenv

# Importar factory do core
sys.path.append('..')
from core.agent import create_web_agent, safebot_factory

# Carregar variáveis de ambiente
load_dotenv()

class SafeBotWebApp:
    """Aplicação web com agentes especializados em NR-06"""
    
    def __init__(self):
        self.agents = self._create_specialized_agents()
        self.playground = Playground(agents=self.agents)
        self.app = self.playground.get_app()
        self._setup_endpoints()
    
    def _create_specialized_agents(self) -> List[Agent]:
        """Cria todos os agentes especializados para a interface web"""
        
        agents = []
        
        # 1. Seletor de EPIs
        epi_selector = create_web_agent(
            agent_type="epi_selector",
            custom_instructions=[
                "MEMÓRIA: Lembre-se de seleções anteriores para padrões similares de risco",
                "DETALHES: Inclua tipo de CA, especificações técnicas, periodicidade de troca",
                "FOCO: Seja prático e específico para implementação imediata"
            ]
        )
        agents.append(epi_selector)
        
        # 2. Auditor NR-06
        auditor = create_web_agent(
            agent_type="auditor",
            custom_instructions=[
                "MEMÓRIA: Lembre-se de auditorias anteriores e padrões de não conformidade",
                "PERSONALIZAÇÃO: Adapte por setor/atividade específica",
                "Inclua prazos legais e consequências do descumprimento"
            ]
        )
        agents.append(auditor)
        
        # 3. Designer de Treinamentos
        trainer = create_web_agent(
            agent_type="trainer",
            custom_instructions=[
                "MEMÓRIA: Lembre-se de programas anteriores e sua efetividade por cargo",
                "CONTEÚDO: Base legal, tipos de EPI, uso correto, conservação, limitações",
                "AVALIAÇÃO: Inclua 10 questões práticas com gabarito"
            ]
        )
        agents.append(trainer)
        
        # 4. Investigador de Acidentes
        investigator = create_web_agent(
            agent_type="investigator",
            custom_instructions=[
                "MEMÓRIA: Lembre-se de acidentes similares e padrões de causas",
                "PADRÕES: Identifique tendências recorrentes para prevenção proativa",
                "FOCO: Prevenção de recorrência baseada na legislação e experiências"
            ]
        )
        agents.append(investigator)
        
        # 5. Consultor Legal
        legal = create_web_agent(
            agent_type="legal",
            custom_instructions=[
                "MEMÓRIA: Lembre-se de consultas anteriores e interpretações jurídicas",
                "CONSISTÊNCIA: Mantenha coerência nas orientações legais",
                "CONSEQUÊNCIAS: Explique multas, sanções e implicações trabalhistas"
            ]
        )
        agents.append(legal)
        
        # 6. Gerador de POPs
        procedure = safebot_factory.create_base_agent(
            name="📝 Gerador de POPs",
            user_id="procedure_specialist",
            instructions=[
                "Você é especialista em PROCEDIMENTOS OPERACIONAIS para gestão de EPIs",
                "MEMÓRIA: Lembre-se de procedimentos anteriores e adaptações bem-sucedidas",
                "PROCESSO: Analise necessidade → Crie procedimento → Inclua formulários",
                "FORMATO: POP com: Objetivo | Responsáveis | Procedimento | Registros",
                "BASE LEGAL: Fundamente todos os passos em artigos da NR-06",
                "CONTROLES: Inclua indicadores e formas de monitoramento"
            ],
            table_name="procedure_web",
            tools=[PythonTools()]  # Para cálculos e formatação
        )
        agents.append(procedure)
        
        return agents
    
    def _setup_endpoints(self):
        """Configura endpoints adicionais da aplicação"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint para monitoramento"""
            return {
                "status": "healthy",
                "service": "safebot-nr06-web",
                "agents_count": len(self.agents),
                "knowledge_base": "loaded",
                "memory_enabled": True,
                "version": "2.0.0"
            }
        
        @self.app.get("/")
        async def root():
            """Root endpoint com informações do sistema"""
            return {
                "message": "🛡️ SafeBot NR-06 - Web Application",
                "description": "Sistema especializado para Equipamentos de Proteção Individual",
                "agents": [agent.name for agent in self.agents],
                "playground_url": "/playground",
                "docs_url": "/docs",
                "architecture": "modular"
            }
        
        @self.app.get("/agents")
        async def list_agents():
            """Lista todos os agentes disponíveis"""
            return {
                "agents": [
                    {
                        "name": agent.name,
                        "user_id": agent.user_id,
                        "has_knowledge": hasattr(agent, 'knowledge') and agent.knowledge is not None,
                        "has_memory": hasattr(agent, 'memory') and agent.memory is not None,
                        "tools_count": len(agent.tools) if hasattr(agent, 'tools') and agent.tools else 0
                    }
                    for agent in self.agents
                ]
            }
    
    def get_app(self):
        """Retorna a aplicação FastAPI"""
        return self.app
    
    def serve(self, **kwargs):
        """Inicia o servidor web"""
        return self.playground.serve(**kwargs)

def create_app():
    """Factory function para criar a aplicação web"""
    return SafeBotWebApp()

def main():
    """Função principal para executar a aplicação web"""
    print("🛡️ SAFEBOT NR-06 - WEB APPLICATION")
    print("=" * 60)
    
    # Verificar configurações
    openai_key = os.getenv("OPENAI_API_KEY")
    environment = os.getenv("ENVIRONMENT", "development")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY não configurado!")
        return
    
    print("✅ Configurações verificadas")
    print(f"🌍 Environment: {environment}")
    
    # Verificar se knowledge base existe
    if not os.path.exists("../data/pdfs/nr-06-atualizada-2022-1.pdf"):
        print("⚠️ Arquivo da NR-06 não encontrado!")
        print("A aplicação funcionará, mas sem a base de conhecimento completa.")
    
    try:
        # Criar aplicação
        web_app = create_app()
        
        print("📚 AGENTES ESPECIALIZADOS DISPONÍVEIS:")
        for agent in web_app.agents:
            print(f"  {agent.name}")
        
        print("=" * 60)
        print("💡 Para carregar a base de conhecimento: python -c 'from core.agent import load_knowledge_base; load_knowledge_base()'")
        print("🚀 Iniciando aplicação web...")
        
        # Configuração baseada no ambiente
        if environment == "production":
            # Produção: usar configurações otimizadas
            web_app.serve(
                app="web.app:app", 
                host="0.0.0.0",
                port=8000,
                reload=False,
                access_log=True
            )
        else:
            # Desenvolvimento: usar reload
            web_app.serve(
                app="web.app:app", 
                reload=True,
                port=7777  # Porta padrão Agno para desenvolvimento
            )
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicação interrompida pelo usuário.")
        print("👋 SafeBot Web desativado!")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

# Instância global da aplicação
app_instance = create_app()
app = app_instance.get_app()

if __name__ == "__main__":
    main()
