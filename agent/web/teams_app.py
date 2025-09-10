#!/usr/bin/env python3
"""
SafeBot Teams Web Application
Interface web usando Agno Playground para teams multi-agente especializados em NR-06
"""
import os
import sys
from typing import List
from agno.agent import Agent
from agno.team import Team
from agno.playground import Playground
from dotenv import load_dotenv

# Importar factory do core
sys.path.append('..')
from core.teams import SafeBotTeamsFactory

# Carregar variáveis de ambiente
load_dotenv()

class SafeBotTeamsWebApp:
    """Aplicação web com teams multi-agente especializados em NR-06"""
    
    def __init__(self):
        self.factory = SafeBotTeamsFactory()
        self.teams = self._create_teams()
        self.playground = Playground(
            teams=self.teams,
            name="SafeBot NR-06 Playground", 
            description="Sistema inteligente com roteamento para especialistas em NR-06",
            app_id="safebot-nr06-playground"
        )
        self.app = self.playground.get_app()
        self._setup_endpoints()
    
    def _create_teams(self) -> List[Team]:
        """Cria team único que roteia para agentes especializados"""
        
        teams = []
        
        # Team único de roteamento para especialistas NR-06
        safety_team = self.factory.create_quick_consultation_team()
        teams.append(safety_team)
        
        return teams
    
    def _setup_endpoints(self):
        """Configura endpoints adicionais da aplicação"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint para monitoramento"""
            return {
                "status": "healthy",
                "service": "safebot-nr06-teams-web",
                "teams_count": len(self.teams),
                "knowledge_base": "loaded",
                "memory_enabled": True,
                "version": "2.0.0-teams"
            }
        
        @self.app.get("/")
        async def root():
            """Root endpoint com informações do sistema"""
            return {
                "message": "🛡️ SafeBot NR-06 - Web Application",
                "description": "Sistema inteligente com roteamento para especialistas em NR-06",
                "team": self.teams[0].name if self.teams else "N/A",
                "specialists": len(self.teams[0].members) if self.teams and hasattr(self.teams[0], 'members') else 0,
                "playground_url": "/playground",
                "docs_url": "/docs",
                "architecture": "intelligent-routing"
            }
        
        @self.app.get("/team")
        async def get_team_info():
            """Informações do team de roteamento"""
            if not self.teams:
                return {"error": "Nenhum team disponível"}
                
            team = self.teams[0]
            return {
                "name": team.name,
                "mode": team.mode if hasattr(team, 'mode') else "route",
                "description": "Roteia consultas para especialistas adequados",
                "specialists": [
                    {
                        "name": member.name if hasattr(member, 'name') else "Unknown",
                        "role": member.role if hasattr(member, 'role') else "Specialist"
                    }
                    for member in (team.members if hasattr(team, 'members') else [])
                ],
                "specialists_count": len(team.members) if hasattr(team, 'members') else 0,
                "has_knowledge": hasattr(team, 'knowledge') and team.knowledge is not None,
                "has_memory": hasattr(team, 'memory') and team.memory is not None,
                "tools_count": len(team.tools) if hasattr(team, 'tools') and team.tools else 0
            }
    
    def get_app(self):
        """Retorna a aplicação FastAPI"""
        return self.app
    
    def serve(self, **kwargs):
        """Inicia o servidor web"""
        return self.playground.serve(**kwargs)

def create_app():
    """Factory function para criar a aplicação web"""
    return SafeBotTeamsWebApp()

def main():
    """Função principal para executar a aplicação web"""
    print("🛡️ SAFEBOT NR-06 - WEB APPLICATION")
    print("=" * 60)
    
    # Verificar configurações
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    environment = os.getenv("ENVIRONMENT", "development")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY não configurado!")
        return
    
    print("✅ Configurações verificadas")
    print(f"🌍 Environment: {environment}")
    print(f"🤖 OpenAI: {'✅' if openai_key else '❌'}")
    print(f"🧠 Anthropic: {'✅' if anthropic_key else '⚠️ Opcional'}")
    
    # Verificar se knowledge base existe
    if not os.path.exists("../data/pdfs/nr-06-atualizada-2022-1.pdf"):
        print("⚠️ Arquivo da NR-06 não encontrado!")
        print("A aplicação funcionará, mas sem a base de conhecimento completa.")
    
    try:
        # Criar aplicação
        web_app = create_app()
        
        print("🎯 SISTEMA DE ROTEAMENTO INTELIGENTE:")
        if web_app.teams:
            team = web_app.teams[0]
            mode = team.mode if hasattr(team, 'mode') else "route"
            members_count = len(team.members) if hasattr(team, 'members') else 0
            print(f"  {team.name} ({mode.upper()})")
            print(f"  └── {members_count} especialistas disponíveis")
            
            if hasattr(team, 'members'):
                for member in team.members:
                    name = member.name if hasattr(member, 'name') else "Unknown"
                    print(f"      • {name}")
        
        print("=" * 60)
        print("💡 Para carregar a base de conhecimento: python -c 'from core.teams import load_knowledge_base; load_knowledge_base()'")
        print("🚀 Iniciando aplicação web...")
        
        # Configuração baseada no ambiente
        if environment == "production":
            # Produção: usar configurações otimizadas
            web_app.serve(
                app="web.teams_app:app", 
                host="0.0.0.0",
                port=8000,
                reload=False,
                access_log=True
            )
        else:
            # Desenvolvimento: usar reload
            web_app.serve(
                app="web.teams_app:app", 
                reload=True,
                port=7777  # Porta padrão Agno para desenvolvimento
            )
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicação interrompida pelo usuário.")
        print("👋 SafeBot NR-06 Web desativado!")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

# Instância global da aplicação
app_instance = create_app()
app = app_instance.get_app()

if __name__ == "__main__":
    main()
