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
🛡️ SAFEBOT NR-06 - SISTEMA MULTI-AGENTE

🎯 CANAIS DISPONÍVEIS:

1. 📱 TELEGRAM BOT (Recomendado)
   python safebot.py telegram
   • Bot real 24/7 no Telegram
   • Múltiplos usuários simultâneos
   • Memória individual por usuário
   • Comandos: /start, /help, /status

2. 🤝 TELEGRAM TEAMS (Novo!)
   python safebot.py telegram-teams
   • Bot com sistema multi-agente
   • 3 teams especializados (Quick, Comprehensive, Research)
   • Colaboração entre especialistas
   • Análises mais completas e precisas

3. 🌐 WEB APPLICATION  
   python safebot.py web
   • Interface web com Agno Playground
   • 6 agentes especializados
   • Ideal para desenvolvimento e testes
   • Acesso via http://localhost:7777

4. 🌐 WEB TEAMS (Novo!)
   python safebot.py web-teams
   • Interface web com sistema multi-agente
   • API REST para teams
   • Documentação em /docs
   • Acesso via http://localhost:7777

5. 🔧 UTILITÁRIOS
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

🏗️ NOVA ARQUITETURA MULTI-AGENTE:
├── core/
│   ├── agent.py         # Factory de agentes individuais
│   └── teams.py         # Factory de teams multi-agente (NOVO!)
├── telegram_bot/
│   ├── bot.py          # Bot individual
│   └── teams_bot.py    # Bot com teams (NOVO!)
├── web/
│   ├── app.py          # Interface individual
│   └── teams_app.py    # Interface com teams (NOVO!)
├── examples/
│   └── teams_examples.py # Exemplos práticos (NOVO!)
└── safebot.py          # Launcher unificado

🤝 TEAMS DISPONÍVEIS:
• Quick Team (ROUTE): Consultas rápidas e direcionadas
• Comprehensive Team (COORDINATE): Análises completas
• Research Team (COLLABORATE): Pesquisa colaborativa

💡 VANTAGENS DOS TEAMS:
• Especialização: Cada agente foca em sua área
• Colaboração: Agentes trabalham juntos
• Precisão: Respostas mais completas e precisas
• Flexibilidade: 3 modos diferentes de operação
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
    print(
        f"• OPENAI_API_KEY: {'✅ Configurado' if openai_key else '❌ Não configurado'}"
    )
    print(
        f"• TELEGRAM_TOKEN: {'✅ Configurado' if telegram_token else '⚠️ Não configurado'}"
    )

    # Verificar arquivos
    print("\n📁 ARQUIVOS:")
    nr06_path = "data/pdfs/nr-06-atualizada-2022-1.pdf"
    print(
        f"• NR-06 PDF: {'✅ Encontrado' if os.path.exists(nr06_path) else '❌ Não encontrado'}"
    )

    # Verificar estrutura
    print("\n🏗️ ESTRUTURA:")
    directories = ["core", "telegram_bot", "web", "data", "tmp"]
    for directory in directories:
        exists = os.path.exists(directory)
        print(f"• {directory}/: {'✅' if exists else '❌'}")

    print("\n🎯 CANAIS DISPONÍVEIS:")
    print("• telegram - Bot individual do Telegram")
    print("• telegram-teams - Bot com sistema multi-agente")
    print("• web - Interface web com Playground")
    print("• web-teams - Interface web com teams")

    print("\n💡 Use 'python safebot.py help' para mais informações")


def run_telegram():
    """Executa o bot do Telegram (individual)"""
    try:
        from telegram_bot.bot import main as telegram_main

        telegram_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Telegram: {e}")
        print(
            "💡 Verifique se python-telegram-bot está instalado: pip install python-telegram-bot"
        )
    except Exception as e:
        print(f"❌ Erro ao executar bot Telegram: {e}")


def run_telegram_teams():
    """Executa o bot do Telegram com teams"""
    try:
        from telegram_bot.teams_bot import main as telegram_teams_main

        telegram_teams_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Telegram Teams: {e}")
        print(
            "💡 Verifique se python-telegram-bot está instalado: pip install python-telegram-bot"
        )
    except Exception as e:
        print(f"❌ Erro ao executar bot Telegram Teams: {e}")


def run_web():
    """Executa a aplicação web (individual)"""
    try:
        from web.app import main as web_main

        web_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Web: {e}")
        print("💡 Verifique se as dependências estão instaladas")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação web: {e}")


def run_web_teams():
    """Executa a aplicação web com teams"""
    try:
        from web.teams_app import main as web_teams_main

        web_teams_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo Web Teams: {e}")
        print("💡 Verifique se as dependências estão instaladas")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação web teams: {e}")


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
        print("• telegram       - Executar bot individual do Telegram")
        print("• telegram-teams - Executar bot com sistema multi-agente")
        print("• web           - Executar aplicação web individual")
        print("• web-teams     - Executar aplicação web com teams")
        print("• load-kb       - Carregar base de conhecimento")
        print("• info          - Mostrar informações do sistema")
        print("• help          - Mostrar ajuda completa")
        print("\n💡 Use 'python safebot.py help' para mais detalhes")
        return

    command = sys.argv[1].lower()

    # Comandos disponíveis
    commands = {
        "telegram": run_telegram,
        "telegram-teams": run_telegram_teams,
        "web": run_web,
        "web-teams": run_web_teams,
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
