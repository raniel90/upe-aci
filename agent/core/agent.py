import os
from typing import Optional, List
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from dotenv import load_dotenv

load_dotenv()

class SafeBotFactory:
    """Factory para criar agentes SafeBot especializados"""
    
    def __init__(self, data_dir: str = "data", tmp_dir: str = "tmp"):
        self.data_dir = data_dir
        self.tmp_dir = tmp_dir
        self._vector_db = None
        self._knowledge_base = None
    
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
        """Knowledge base compartilhada"""
        if self._knowledge_base is None:
            self._knowledge_base = PDFKnowledgeBase(
                path=[
                    {
                        "path": f"{self.data_dir}/pdfs/nr-06-atualizada-2022-1.pdf", # TODO: Alterar para o arquivo da NR-06
                        "metadata": {
                            "document_type": "norma_regulamentadora",
                            "nr_number": "06",
                            "year": 2022,
                            "topic": "equipamentos_protecao_individual",
                            "language": "portuguese",
                        },
                    }
                ],
                vector_db=self.vector_db,
            )
        return self._knowledge_base
    
    def create_memory(self, agent_name: str, user_id: str, memory_db_file: str = None) -> Memory:
        """Cria memória específica para um agente"""
        if memory_db_file is None:
            memory_db_file = f"{self.tmp_dir}/agent_memories.db"
            
        return Memory(
            model=OpenAIChat(id="gpt-4o-mini"),
            db=SqliteMemoryDb(
                table_name=f"{agent_name}_memory", 
                db_file=memory_db_file
            ),
            delete_memories=False,
            clear_memories=False,
        )
    
    def create_storage(self, table_name: str, db_file: str = None) -> SqliteStorage:
        """Cria storage para um agente"""
        if db_file is None:
            db_file = f"{self.tmp_dir}/agents.db"
            
        return SqliteStorage(table_name=table_name, db_file=db_file)
    
    def create_base_agent(
        self,
        name: str,
        user_id: str,
        instructions: List[str],
        table_name: str,
        tools: Optional[List] = None,
        enable_memory: bool = True,
        enable_knowledge: bool = True,
        memory_db_file: str = None,
        storage_db_file: str = None,
    ) -> Agent:
        """
        Cria um agente base com configurações padrão do SafeBot
        
        Args:
            name: Nome do agente
            user_id: ID único do usuário/contexto
            instructions: Lista de instruções específicas
            table_name: Nome da tabela para storage
            tools: Lista de ferramentas (opcional)
            enable_memory: Se deve habilitar memória
            enable_knowledge: Se deve habilitar knowledge base
            memory_db_file: Arquivo de banco para memória (opcional)
            storage_db_file: Arquivo de banco para storage (opcional)
        """
        
        agent_config = {
            "name": name,
            "model": OpenAIChat(id="gpt-4o-mini"),
            "user_id": user_id,
            "instructions": instructions,
            "storage": self.create_storage(table_name, storage_db_file),
            "add_datetime_to_instructions": True,
            "add_history_to_messages": True,
            "num_history_responses": 8,
            "markdown": True,
        }
        
        # Adicionar conhecimento se habilitado
        if enable_knowledge:
            agent_config["knowledge"] = self.knowledge_base
            agent_config["search_knowledge"] = True
        
        # Adicionar memória se habilitado
        if enable_memory:
            agent_config["memory"] = self.create_memory(
                table_name, user_id, memory_db_file
            )
            agent_config["enable_user_memories"] = True
        
        # Adicionar ferramentas se fornecidas
        if tools:
            agent_config["tools"] = tools
        
        return Agent(**agent_config)
    
    def create_telegram_agent(
        self,
        user_id: str,
        telegram_tools: List,
        custom_instructions: Optional[List[str]] = None,
        memory_db_file: str = None,
    ) -> Agent:
        """Cria agente otimizado para Telegram"""
        
        base_instructions = [
            "Você é o SafeBot, especialista em segurança e saúde do trabalho.",
            "Você está conversando via Telegram e deve ser conversacional, útil e amigável.",
            "",
            "🎯 SUAS ESPECIALIDADES:",
            "• Seleção e uso adequado de equipamentos de proteção",
            "• Auditoria de conformidade em segurança do trabalho", 
            "• Criação de treinamentos personalizados",
            "• Investigação de acidentes e incidentes",
            "• Consultoria legal em normas de segurança",
            "• Geração de procedimentos operacionais (POPs)",
            "",
            "📱 FORMATAÇÃO TELEGRAM (CRÍTICO - SIGA EXATAMENTE):",
            "• Use APENAS HTML para formatação: <b>negrito</b>, <i>itálico</i>, <code>código</code>",
            "• PROIBIDO usar markdown (_ * ` ## **) - quebra a formatação!",
            "• Para listas, use APENAS: • ✅ ❌ 🔸 (símbolos + espaço)",
            "• Para títulos: <b>TÍTULO EM MAIÚSCULAS</b> 🔸",
            "• Para citações: <code>Art. X.X.X</code>",
            "• Para alertas: <b>⚠️ ATENÇÃO:</b>",
            "• Para itálico em listas: • ✅ <i>Texto em itálico</i>",
            "• NUNCA misture HTML com markdown na mesma resposta",
            "• Teste mental: se vê _ ou * ou `, está ERRADO!",
            "• Use quebras de linha duplas para separar seções",
            "",
            "💬 ESTILO TELEGRAM:",
            "• Seja amigável e profissional",
            "• Use emojis para tornar a conversa dinâmica: 🛡️ ⚠️ ✅ ❌ 💡 🔍 👋",
            "• Mantenha mensagens claras e organizadas",
            "• Faça perguntas para entender melhor o contexto",
            "• Lembre-se das conversas anteriores",
            "• Evite textos muito longos - divida em mensagens menores se necessário",
            "",
            "🔍 PROCESSO:",
            "1. Cumprimente novos usuários de forma amigável",
            "2. Identifique a necessidade específica",
            "3. Consulte a base de conhecimento de segurança do trabalho",
            "4. Forneça respostas práticas e fundamentadas",
            "5. Ofereça ajuda adicional quando apropriado",
            "",
            "📋 FORMATO DE RESPOSTA TELEGRAM:",
            "• Use <b>títulos em negrito</b> para seções",
            "• Liste itens com • seguido de espaço, nunca use -",
            "• Cite artigos como <code>Art. 6.3.1</code>",
            "• Use <i>texto em itálico</i> para observações (apenas HTML)",
            "• Para listas com itálico: • ✅ <i>Descrição em itálico</i>",
            "• Termine com pergunta ou oferta de ajuda adicional",
            "• Mantenha formatação consistente em HTML",
            "",
            "⚖️ SEMPRE:",
            "• Base suas respostas nas normas de segurança atualizadas",
            "• Cite artigos específicos quando relevante",
            "• Mantenha tom conversacional e acessível",
            "• Seja proativo em ajudar",
            "• Use formatação HTML adequada para Telegram"
        ]
        
        # Combinar instruções base com personalizadas
        if custom_instructions:
            instructions = base_instructions + [""] + custom_instructions
        else:
            instructions = base_instructions
        
        return self.create_base_agent(
            name=f"🛡️ SafeBot - User {user_id}",
            user_id=user_id,
            instructions=instructions,
            table_name=f"user_{user_id}_sessions",
            tools=telegram_tools,
            memory_db_file=memory_db_file or f"{self.tmp_dir}/telegram_memory.db",
            storage_db_file=f"{self.tmp_dir}/telegram_sessions.db",
        )
    
    def create_web_agent(
        self,
        agent_type: str = "general",
        custom_instructions: Optional[List[str]] = None,
    ) -> Agent:
        """Cria agente otimizado para interface web"""
        
        agent_configs = {
            "epi_selector": {
                "name": "🎯 Seletor de EPIs",
                "instructions": [
                    "Você é especialista em SELEÇÃO DE EPIs conforme NR-06",
                    "PROCESSO: Analise os riscos → Recomende EPIs específicos → Justifique legalmente",
                    "FORMATO: Use tabela com colunas: Risco | EPI | Artigo NR-06 | Observações",
                    "Sempre cite artigos específicos da NR-06 que fundamentam a recomendação"
                ]
            },
            "auditor": {
                "name": "📋 Auditor NR-06",
                "instructions": [
                    "Você é especialista em AUDITORIA DE CONFORMIDADE NR-06",
                    "PROCESSO: Gere checklists → Classifique não conformidades → Sugira ações",
                    "FORMATO: Checklist com: Item | Artigo NR-06 | Status | Criticidade | Ação",
                    "CLASSIFICAÇÃO: Crítica | Alta (30 dias) | Média (60 dias) | Baixa (90 dias)"
                ]
            },
            "trainer": {
                "name": "🎓 Designer de Treinamentos",
                "instructions": [
                    "Você é especialista em TREINAMENTOS DE EPIs conforme NR-06",
                    "PROCESSO: Analise função → Crie programa → Gere conteúdo → Desenvolva avaliação",
                    "FORMATO: Objetivos | Conteúdo | Duração | Metodologia | Avaliação",
                    "Personalize por cargo/função específica citando artigos da NR-06"
                ]
            },
            "investigator": {
                "name": "🔍 Investigador de Acidentes",
                "instructions": [
                    "Você é especialista em INVESTIGAÇÃO DE ACIDENTES relacionados a EPIs",
                    "PROCESSO: Analise acidente → Identifique falhas → Determine responsabilidades",
                    "ANÁLISE: Falhas em seleção, fornecimento, treinamento, uso, fiscalização",
                    "FORMATO: Relatório estruturado para CAT com causas e medidas preventivas"
                ]
            },
            "legal": {
                "name": "⚖️ Consultor Legal NR-06",
                "instructions": [
                    "Você é especialista em ASPECTOS LEGAIS da NR-06",
                    "PROCESSO: Identifique situação → Cite base legal → Explique responsabilidades",
                    "RESPONSABILIDADES: Diferencie obrigações empregador vs empregado",
                    "FORMATO: Parecer legal estruturado com fundamentação na NR-06"
                ]
            },
            "procedure": {
                "name": "📝 Gerador de POPs",
                "instructions": [
                    "Você é especialista em PROCEDIMENTOS OPERACIONAIS para gestão de EPIs",
                    "PROCESSO: Analise necessidade → Crie procedimento → Inclua formulários",
                    "FORMATO: POP com: Objetivo | Responsáveis | Procedimento | Registros",
                    "BASE LEGAL: Fundamente todos os passos em artigos da NR-06"
                ]
            },
            "general": {
                "name": "🛡️ SafeBot NR-06 - Geral",
                "instructions": [
                    "Você é o SafeBot, especialista geral em NR-06",
                    "Ajude com qualquer questão relacionada a Equipamentos de Proteção Individual",
                    "Seja claro, objetivo e sempre cite a base legal quando relevante"
                ]
            }
        }
        
        config = agent_configs.get(agent_type, agent_configs["general"])
        
        # Combinar instruções base com personalizadas
        if custom_instructions:
            instructions = config["instructions"] + [""] + custom_instructions
        else:
            instructions = config["instructions"]
        
        return self.create_base_agent(
            name=config["name"],
            user_id=f"{agent_type}_web_user",
            instructions=instructions,
            table_name=f"{agent_type}_web",
        )
    
    def load_knowledge_base(self, recreate: bool = False):
        """Carrega a base de conhecimento da NR-06"""
        print("🔄 Carregando base de conhecimento da NR-06...")
        
        # Verificar se o arquivo existe
        pdf_path = f"{self.data_dir}/pdfs/nr-06-atualizada-2022-1.pdf"
        if not os.path.exists(pdf_path):
            print(f"⚠️ Arquivo não encontrado: {pdf_path}")
            print("O sistema funcionará, mas sem a base de conhecimento completa.")
            return False
        
        try:
            self.knowledge_base.load(recreate=recreate)
            print("✅ Base de conhecimento carregada com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar base de conhecimento: {e}")
            return False

# Instância global do factory
safebot_factory = SafeBotFactory()

# Funções de conveniência para compatibilidade
def create_telegram_agent(user_id: str, telegram_tools: List, **kwargs) -> Agent:
    """Função de conveniência para criar agente Telegram"""
    return safebot_factory.create_telegram_agent(user_id, telegram_tools, **kwargs)

def create_web_agent(agent_type: str = "general", **kwargs) -> Agent:
    """Função de conveniência para criar agente Web"""
    return safebot_factory.create_web_agent(agent_type, **kwargs)

def load_knowledge_base(recreate: bool = False) -> bool:
    """Função de conveniência para carregar knowledge base"""
    return safebot_factory.load_knowledge_base(recreate)
