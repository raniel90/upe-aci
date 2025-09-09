#!/usr/bin/env python3
"""
SafeBot NR-06 - Launcher Principal
Ponto de entrada unificado para todos os canais (Web, Telegram, CLI)
"""
import sys
import os
from typing import Optional

def show_help():
    """Mostra ajuda sobre como usar o SafeBot"""
    help_text = """
🛡️ SAFEBOT NR-06 - SISTEMA MODULAR

🎯 CANAIS DISPONÍVEIS:

1. 📱 TELEGRAM BOT (Recomendado)
   python safebot.py telegram
   • Bot real 24/7 no Telegram
   • Múltiplos usuários simultâneos
   • Memória individual por usuário
   • Comandos: /start, /help, /status

2. 🌐 WEB APPLICATION  
   python safebot.py web
   • Interface web com Agno Playground
   • 6 agentes especializados
   • Ideal para desenvolvimento e testes
   • Acesso via http://localhost:7777

3. 🔧 UTILITÁRIOS
   python safebot.py load-kb
   • Carrega base de conhecimento NR-06
   • Execute antes do primeiro uso

4. ℹ️ INFORMAÇÕES
   python safebot.py info
   • Mostra informações do sistema
   • Verifica configurações

📋 CONFIGURAÇÃO NECESSÁRIA:
export OPENAI_API_KEY=sua-chave-aqui
export TELEGRAM_TOKEN=seu-token-aqui  # Apenas para Telegram

🏗️ ARQUITETURA MODULAR:
├── core/agent.py        # Factory de agentes reutilizável
├── telegram/bot.py      # Bot específico do Telegram  
├── web/app.py          # Interface web com Playground
└── safebot.py          # Launcher unificado (este arquivo)

💡 VANTAGENS:
• DRY: Código compartilhado no core
• Modular: Cada canal isolado
• Flexível: Fácil adicionar novos canais
• Manutenível: Responsabilidades separadas
    """
    print(help_text)

def show_info():
    """Mostra informações do sistema"""
    print("🛡️ SAFEBOT NR-06 - INFORMAÇÕES DO SISTEMA")
    print("=" * 60)
    
    # Verificar configurações
    openai_key = os.getenv("OPENAI_API_KEY")
    telegram_token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    
    print("📋 CONFIGURAÇÕES:")
    print(f"• OPENAI_API_KEY: {'✅ Configurado' if openai_key else '❌ Não configurado'}")
    print(f"• TELEGRAM_TOKEN: {'✅ Configurado' if telegram_token else '⚠️ Não configurado'}")
    
    # Verificar arquivos
    print("\n📁 ARQUIVOS:")
    nr06_path = "data/pdfs/nr-06-atualizada-2022-1.pdf"
    print(f"• NR-06 PDF: {'✅ Encontrado' if os.path.exists(nr06_path) else '❌ Não encontrado'}")
    
    # Verificar estrutura
    print("\n🏗️ ESTRUTURA:")
    directories = ["core", "telegram", "web", "data", "tmp"]
    for directory in directories:
        exists = os.path.exists(directory)
        print(f"• {directory}/: {'✅' if exists else '❌'}")
    
    print("\n🎯 CANAIS DISPONÍVEIS:")
    print("• telegram - Bot real do Telegram")
    print("• web - Interface web com Playground")
    
    print("\n💡 Use 'python safebot.py help' para mais informações")

def run_telegram():
    """Executa o bot do Telegram"""
    try:
        from telegram_bot.bot import main as telegram_main
        telegram_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Telegram: {e}")
        print("💡 Verifique se python-telegram-bot está instalado: pip install python-telegram-bot")
    except Exception as e:
        print(f"❌ Erro ao executar bot Telegram: {e}")

def run_web():
    """Executa a aplicação web"""
    try:
        from web.app import main as web_main
        web_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Web: {e}")
        print("💡 Verifique se as dependências estão instaladas")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação web: {e}")

def load_knowledge_base():
    """Carrega a base de conhecimento"""
    try:
        from core.agent import load_knowledge_base
        success = load_knowledge_base(recreate=True)
        if success:
            print("✅ Base de conhecimento carregada com sucesso!")
        else:
            print("⚠️ Falha ao carregar base de conhecimento")
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Core: {e}")
    except Exception as e:
        print(f"❌ Erro ao carregar knowledge base: {e}")

def main():
    """Função principal do launcher"""
    
    if len(sys.argv) < 2:
        print("🛡️ SAFEBOT NR-06 - LAUNCHER")
        print("=" * 40)
        print("Use: python safebot.py <comando>")
        print("\nComandos disponíveis:")
        print("• telegram  - Executar bot do Telegram")
        print("• web      - Executar aplicação web")  
        print("• load-kb  - Carregar base de conhecimento")
        print("• info     - Mostrar informações do sistema")
        print("• help     - Mostrar ajuda completa")
        print("\n💡 Use 'python safebot.py help' para mais detalhes")
        return
    
    command = sys.argv[1].lower()
    
    # Comandos disponíveis
    commands = {
        "telegram": run_telegram,
        "web": run_web,
        "load-kb": load_knowledge_base,
        "info": show_info,
        "help": show_help,
        "--help": show_help,
        "-h": show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Comando desconhecido: {command}")
        print("💡 Use 'python safebot.py help' para ver comandos disponíveis")

if __name__ == "__main__":
    main()
