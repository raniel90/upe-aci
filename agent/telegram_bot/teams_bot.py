#!/usr/bin/env python3
"""
SafeBot Telegram Teams Bot
Bot do Telegram integrado com sistema de teams multi-agente
"""
import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Adicionar path para imports
sys.path.append(str(Path(__file__).parent.parent))

from core.teams import SafeBotTeamsFactory

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SafeBotTeamsBot:
    """Bot do Telegram com suporte a teams multi-agente"""
    
    def __init__(self):
        self.factory = SafeBotTeamsFactory()
        self.user_sessions: Dict[int, Dict] = {}
        
        # Inicializar teams
        self.teams = {
            'comprehensive': self.factory.create_comprehensive_safety_team(),
            'quick': self.factory.create_quick_consultation_team(),
            'research': self.factory.create_collaborative_research_team()
        }
    
    def get_user_session(self, user_id: int) -> Dict:
        """Obtém ou cria sessão do usuário"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'current_team': 'quick',  # Team padrão
                'conversation_count': 0,
                'preferred_mode': 'quick'
            }
        return self.user_sessions[user_id]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start com apresentação dos teams"""
        user = update.effective_user
        session = self.get_user_session(user.id)
        
        welcome_message = f"""
🛡️ <b>SafeBot Teams - Bem-vindo!</b>

Olá <b>{user.first_name}</b>! 👋

Sou o SafeBot com <b>sistema multi-agente</b> especializado em segurança do trabalho. 
Agora trabalho com <b>teams de especialistas</b> para oferecer análises ainda mais completas!

🤝 <b>MEUS TEAMS DISPONÍVEIS:</b>

🎯 <b>Quick Team</b> (Padrão)
• Consultas rápidas e direcionadas
• Roteamento inteligente por especialidade
• Ideal para perguntas específicas

🔬 <b>Comprehensive Team</b>
• Análises completas e abrangentes
• Coordenação de múltiplos especialistas
• Relatórios estruturados e detalhados

🧠 <b>Research Team</b>
• Pesquisa colaborativa avançada
• Múltiplas perspectivas especializadas
• Ideal para tópicos complexos

<b>Team atual:</b> {session['current_team'].title()} Team

Use /teams para trocar de team ou /help para mais comandos.
"""
        
        # Keyboard com opções principais
        keyboard = [
            [InlineKeyboardButton("🔄 Trocar Team", callback_data="change_team")],
            [InlineKeyboardButton("❓ Ajuda", callback_data="help")],
            [InlineKeyboardButton("📊 Status", callback_data="status")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    
    async def teams_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /teams para trocar entre teams"""
        session = self.get_user_session(update.effective_user.id)
        
        teams_message = """
🤝 <b>ESCOLHA SEU TEAM SAFEBOT:</b>

Selecione o team mais adequado para sua consulta:
"""
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Team", callback_data="team_quick")],
            [InlineKeyboardButton("🔬 Comprehensive Team", callback_data="team_comprehensive")],
            [InlineKeyboardButton("🧠 Research Team", callback_data="team_research")],
            [InlineKeyboardButton("ℹ️ Detalhes dos Teams", callback_data="team_details")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            teams_message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
🛡️ <b>SAFEBOT TEAMS - AJUDA</b>

<b>🤖 COMANDOS DISPONÍVEIS:</b>
/start - Iniciar bot e apresentação
/teams - Trocar entre teams
/status - Ver status atual e estatísticas
/help - Esta mensagem de ajuda

<b>🤝 TEAMS DISPONÍVEIS:</b>

<b>⚡ Quick Team (ROUTE)</b>
• <i>Especialista em:</i> Consultas rápidas
• <i>Ideal para:</i> Perguntas específicas sobre segurança
• <i>Tempo:</i> Resposta rápida e direcionada

<b>🔬 Comprehensive Team (COORDINATE)</b>  
• <i>Especialista em:</i> Análises completas
• <i>Ideal para:</i> Implementação de programas
• <i>Tempo:</i> Análise detalhada (mais demorada)

<b>🧠 Research Team (COLLABORATE)</b>
• <i>Especialista em:</i> Pesquisa colaborativa
• <i>Ideal para:</i> Tópicos complexos e inovadores
• <i>Tempo:</i> Pesquisa aprofundada

<b>💬 COMO USAR:</b>
1. Escolha o team adequado com /teams
2. Faça sua pergunta normalmente
3. O team processará com seus especialistas
4. Receba resposta otimizada para seu caso

<b>🎯 DICAS:</b>
• Use Quick Team para perguntas diretas
• Use Comprehensive Team para projetos
• Use Research Team para pesquisas avançadas
"""
        
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        user_id = update.effective_user.id
        session = self.get_user_session(user_id)
        
        status_text = f"""
📊 <b>STATUS SAFEBOT TEAMS</b>

<b>👤 Usuário:</b> {update.effective_user.first_name}
<b>🤝 Team Atual:</b> {session['current_team'].title()} Team
<b>💬 Conversas:</b> {session['conversation_count']}
<b>⚙️ Modo Preferido:</b> {session['preferred_mode'].title()}

<b>🛡️ SISTEMA:</b>
✅ Teams Multi-Agente Ativos
✅ Base de Conhecimento NR-06 
✅ Especialistas Disponíveis
✅ Memória Compartilhada

<b>🔧 ESPECIALISTAS ATIVOS:</b>
• EPI Specialist (Equipamentos)
• Compliance Auditor (Conformidade)  
• Training Specialist (Treinamentos)
• Risk Analyst (Análise de Riscos)
• Web Researcher (Pesquisas)

Use /teams para trocar de team conforme sua necessidade.
"""
        
        await update.message.reply_text(status_text, parse_mode='HTML')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para botões inline"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        session = self.get_user_session(user_id)
        
        if query.data == "change_team":
            await self.teams_command(update, context)
            
        elif query.data.startswith("team_"):
            team_name = query.data.replace("team_", "")
            session['current_team'] = team_name
            session['preferred_mode'] = team_name
            
            team_names = {
                'quick': 'Quick Team ⚡',
                'comprehensive': 'Comprehensive Team 🔬',
                'research': 'Research Team 🧠'
            }
            
            await query.edit_message_text(
                f"✅ <b>Team alterado!</b>\n\nAgora você está usando: <b>{team_names[team_name]}</b>\n\n"
                "Faça sua pergunta e o team processará com os especialistas adequados.",
                parse_mode='HTML'
            )
            
        elif query.data == "team_details":
            details_text = """
<b>🤝 DETALHES DOS TEAMS:</b>

<b>⚡ QUICK TEAM (Route Mode)</b>
• <i>Funcionamento:</i> Analisa sua pergunta e direciona para o especialista mais adequado
• <i>Especialistas:</i> EPI, Compliance, Training, Risk Analysis
• <i>Vantagem:</i> Resposta rápida e precisa
• <i>Use quando:</i> Tiver pergunta específica

<b>🔬 COMPREHENSIVE TEAM (Coordinate Mode)</b>
• <i>Funcionamento:</i> Coordenador consulta múltiplos especialistas e sintetiza resposta completa
• <i>Especialistas:</i> Todos + Web Research + Reasoning Tools
• <i>Vantagem:</i> Análise completa e estruturada
• <i>Use quando:</i> Precisar de análise abrangente

<b>🧠 RESEARCH TEAM (Collaborate Mode)</b>
• <i>Funcionamento:</i> Especialistas colaboram e chegam a consenso
• <i>Especialistas:</i> EPI, Risk Analysis, Web Research
• <i>Vantagem:</i> Múltiplas perspectivas integradas
• <i>Use quando:</i> Tópico for complexo ou inovador
"""
            await query.edit_message_text(details_text, parse_mode='HTML')
            
        elif query.data == "help":
            await self.help_command(update, context)
            
        elif query.data == "status":
            await self.status_command(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para mensagens"""
        user_id = update.effective_user.id
        session = self.get_user_session(user_id)
        user_message = update.message.text
        
        # Incrementar contador de conversas
        session['conversation_count'] += 1
        
        # Mostrar que está processando
        processing_msg = await update.message.reply_text(
            f"🤝 <b>{session['current_team'].title()} Team</b> está analisando...\n"
            f"⏳ <i>Consultando especialistas...</i>",
            parse_mode='HTML'
        )
        
        try:
            # Obter team atual
            current_team = self.teams[session['current_team']]
            
            # Processar com o team (simulação - na prática seria assíncrono)
            response = current_team.run(user_message)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Deletar mensagem de processamento
            await processing_msg.delete()
            
            # Preparar resposta formatada para Telegram
            formatted_response = self.format_for_telegram(response_text, session['current_team'])
            
            # Enviar resposta (pode precisar dividir se muito longa)
            await self.send_long_message(update, formatted_response)
            
            # Keyboard com ações pós-resposta
            keyboard = [
                [InlineKeyboardButton("🔄 Trocar Team", callback_data="change_team")],
                [InlineKeyboardButton("📊 Status", callback_data="status")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "💡 <i>Posso ajudar com mais alguma coisa?</i>",
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            
        except Exception as e:
            await processing_msg.delete()
            await update.message.reply_text(
                f"❌ <b>Erro no {session['current_team'].title()} Team:</b>\n"
                f"<i>{str(e)}</i>\n\n"
                "Tente novamente ou use /teams para trocar de team.",
                parse_mode='HTML'
            )
    
    def format_for_telegram(self, response: str, team_name: str) -> str:
        """Formata resposta para Telegram com HTML"""
        team_icons = {
            'quick': '⚡',
            'comprehensive': '🔬', 
            'research': '🧠'
        }
        
        icon = team_icons.get(team_name, '🤖')
        
        formatted = f"🛡️ <b>SafeBot {team_name.title()} Team</b> {icon}\n\n"
        
        # Converter markdown básico para HTML
        response = response.replace('**', '<b>').replace('**', '</b>')
        response = response.replace('*', '<i>').replace('*', '</i>')
        response = response.replace('`', '<code>').replace('`', '</code>')
        
        # Adicionar quebras de linha para melhor formatação
        response = response.replace('\n\n', '\n\n')
        
        formatted += response
        
        return formatted
    
    async def send_long_message(self, update: Update, text: str, max_length: int = 4000):
        """Envia mensagem longa dividindo se necessário"""
        if len(text) <= max_length:
            await update.message.reply_text(text, parse_mode='HTML')
        else:
            # Dividir mensagem em partes
            parts = []
            current_part = ""
            
            for line in text.split('\n'):
                if len(current_part + line + '\n') > max_length:
                    if current_part:
                        parts.append(current_part.strip())
                        current_part = line + '\n'
                    else:
                        # Linha muito longa, dividir forçadamente
                        parts.append(line[:max_length])
                        current_part = line[max_length:] + '\n'
                else:
                    current_part += line + '\n'
            
            if current_part:
                parts.append(current_part.strip())
            
            # Enviar partes
            for i, part in enumerate(parts):
                if i == 0:
                    await update.message.reply_text(part, parse_mode='HTML')
                else:
                    await update.message.reply_text(
                        f"<i>(continuação {i+1}/{len(parts)})</i>\n\n{part}",
                        parse_mode='HTML'
                    )

def main():
    """Função principal do bot"""
    # Verificar token
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("❌ Token do Telegram não encontrado!")
        print("💡 Configure TELEGRAM_BOT_TOKEN ou TELEGRAM_TOKEN no ambiente")
        return
    
    print("🛡️ Iniciando SafeBot Teams Bot...")
    
    # Verificar base de conhecimento
    nr06_path = "data/pdfs/nr-06-atualizada-2022-1.pdf"
    if not os.path.exists(nr06_path):
        print("⚠️ Arquivo da NR-06 não encontrado!")
        print(f"📄 Esperado em: {nr06_path}")
        print("🤖 Bot funcionará sem base de conhecimento completa.")
        input("⏸️ Pressione Enter para continuar...")
    
    # Criar bot
    bot = SafeBotTeamsBot()
    
    # Criar aplicação
    application = Application.builder().token(token).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("teams", bot.teams_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("status", bot.status_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    print("✅ SafeBot Teams Bot iniciado!")
    print("🤝 Teams disponíveis: Quick, Comprehensive, Research")
    print("🔄 Pressione Ctrl+C para parar")
    
    # Executar bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

