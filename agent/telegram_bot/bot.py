"""
SafeBot NR-06 - Telegram Bot
Bot real do Telegram que responde automaticamente usando Agno e NR-06
"""
import os
import logging
from typing import Dict
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from agno.tools.telegram import TelegramTools
from dotenv import load_dotenv

# Importar factory do core
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.agent import create_telegram_agent

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

class SafeBotTelegram:
    """Bot real do Telegram que responde automaticamente"""
    
    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.user_agents: Dict[str, object] = {}  # Cache de agentes por usuário
        
    def get_user_agent(self, user_id: str):
        """Obtém ou cria agente para um usuário específico"""
        if user_id not in self.user_agents:
            # Criar TelegramTools para este usuário
            telegram_tools = TelegramTools(
                token=self.telegram_token,
                chat_id=user_id  # Usar user_id como chat_id
            )
            
            # Criar agente usando o factory
            self.user_agents[user_id] = create_telegram_agent(
                user_id=user_id,
                telegram_tools=[telegram_tools]
            )
            
            logger.info(f"Novo agente criado para usuário {user_id}")
        
        return self.user_agents[user_id]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /start"""
        user = update.effective_user
        user_id = str(user.id)
        
        logger.info(f"Comando /start recebido de {user.first_name} (ID: {user_id})")
        
        welcome_message = f"""
🛡️ <b>Olá, {user.first_name}!</b>

Bem-vindo ao SafeBot NR-06! 👋

Sou seu assistente especializado em <b>Equipamentos de Proteção Individual</b> (NR-06).

<b>Como posso ajudar você hoje?</b>
• 🎯 Seleção de EPIs por risco
• 📋 Auditoria de conformidade  
• 🎓 Treinamentos personalizados
• 🔍 Investigação de acidentes
• ⚖️ Consultoria legal
• 📝 Procedimentos operacionais

<b>Digite sua pergunta ou situação!</b> 💬
Exemplo: <i>"Preciso EPIs para soldador"</i>
        """
        
        await update.message.reply_text(welcome_message, parse_mode='HTML')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /help"""
        help_text = """
🆘 <b>Comandos Disponíveis:</b>

/start - Iniciar conversa com o SafeBot
/help - Mostrar esta ajuda
/status - Ver status da sua sessão

<b>💡 Como usar:</b>
Simplesmente digite sua pergunta sobre EPIs!

<b>🎯 Exemplos:</b>
• "Preciso EPIs para soldador"
• "Como fazer auditoria NR-06?"
• "EPIs para ambiente químico"
• "Treinamento de capacete"

Estou aqui para ajudar! 🛡️
        """
        
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /status"""
        user = update.effective_user
        user_id = str(user.id)
        
        # Estatísticas básicas
        agent_exists = user_id in self.user_agents
        
        status_text = f"""
📊 <b>Status da Sessão - {user.first_name}</b>

• <b>Agente ativo:</b> {'✅' if agent_exists else '❌'}
• <b>User ID:</b> {user_id}
• <b>Memória:</b> {'Ativa' if agent_exists else 'Inativa'}

<b>SafeBot NR-06</b> está pronto para ajudar! 🛡️
        """
        
        await update.message.reply_text(status_text, parse_mode='HTML')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para mensagens do usuário"""
        user = update.effective_user
        user_id = str(user.id)
        message_text = update.message.text
        
        logger.info(f"Mensagem recebida de {user.first_name} (ID: {user_id}): {message_text[:50]}...")
        
        try:
            # Mostrar "digitando..."
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Obter agente do usuário
            agent = self.get_user_agent(user_id)
            
            # Processar mensagem com o agente
            response = agent.run(message_text)
            
            # Enviar resposta dividindo mensagens longas se necessário
            await self._send_response(update, response.content)
            
            logger.info(f"Resposta enviada para {user.first_name}")
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem de {user.first_name}: {e}")
            await update.message.reply_text(
                "❌ Desculpe, ocorreu um erro. Tente novamente em alguns instantes.",
                parse_mode='HTML'
            )
    
    async def _send_response(self, update: Update, response_text: str):
        """Envia resposta dividindo mensagens longas se necessário"""
        max_length = 4000  # Limite do Telegram
        
        if len(response_text) <= max_length:
            await update.message.reply_text(response_text, parse_mode='HTML')
        else:
            # Dividir mensagem longa
            parts = self._split_message(response_text, max_length)
            for i, part in enumerate(parts):
                if i == 0:
                    await update.message.reply_text(part, parse_mode='HTML')
                else:
                    await update.message.reply_text(f"<i>(continuação)</i>\n\n{part}", parse_mode='HTML')
    
    def _split_message(self, text: str, max_length: int):
        """Divide mensagem longa em partes menores"""
        if len(text) <= max_length:
            return [text]
        
        parts = []
        current_part = ""
        
        # Dividir por linhas para manter formatação
        lines = text.split('\n')
        
        for line in lines:
            if len(current_part) + len(line) + 1 <= max_length:
                if current_part:
                    current_part += '\n'
                current_part += line
            else:
                if current_part:
                    parts.append(current_part)
                current_part = line
        
        if current_part:
            parts.append(current_part)
        
        return parts
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handler para erros globais"""
        logger.error(f"Exception while handling an update: {context.error}")
    
    def run_bot(self):
        """Executa o bot do Telegram"""
        print("🤖 INICIANDO SAFEBOT NR-06 TELEGRAM")
        print("=" * 60)
        
        try:
            # Criar aplicação usando o padrão builder
            application = Application.builder().token(self.telegram_token).build()
            
            # Adicionar handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("status", self.status_command))
            
            # Handler para mensagens de texto
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Handler para erros
            application.add_error_handler(self.error_handler)
            
            print("✅ Bot configurado com sucesso!")
            print("📱 O bot está ativo e escutando mensagens...")
            print("💬 Usuários podem enviar /start para começar")
            print("⏹️ Pressione Ctrl+C para parar")
            print("=" * 60)
            
            # Executar bot com polling
            application.run_polling()
            
        except Exception as e:
            print(f"❌ Erro ao inicializar bot: {e}")
            print("💡 Verifique se o TELEGRAM_TOKEN está correto")
            print("💡 Certifique-se de que python-telegram-bot está instalado: pip install python-telegram-bot")

def main():
    """Função principal para executar o bot"""
    print("🛡️ SAFEBOT NR-06 - TELEGRAM BOT")
    print("=" * 50)
    
    # Verificar configurações
    telegram_token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not telegram_token:
        print("❌ TELEGRAM_TOKEN não configurado!")
        print("\n📝 Configure a variável de ambiente:")
        print("export TELEGRAM_TOKEN=seu-bot-token-aqui")
        return
    
    if not openai_key:
        print("❌ OPENAI_API_KEY não configurado!")
        return
    
    print("✅ Configurações verificadas")
    
    # Verificar se knowledge base existe
    nr06_path = os.path.join(os.path.dirname(__file__), "..", "data", "pdfs", "nr-06-atualizada-2022-1.pdf")
    if not os.path.exists(nr06_path):
        print("⚠️ Arquivo da NR-06 não encontrado!")
        print(f"Procurado em: {nr06_path}")
        print("O bot funcionará, mas sem a base de conhecimento completa.")
        input("Pressione Enter para continuar mesmo assim...")
    
    try:
        # Criar e executar bot
        bot = SafeBotTelegram(telegram_token)
        bot.run_bot()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Bot interrompido pelo usuário.")
        print("👋 SafeBot desativado!")
    except Exception as e:
        print(f"❌ Erro ao executar bot: {e}")

if __name__ == "__main__":
    main()
