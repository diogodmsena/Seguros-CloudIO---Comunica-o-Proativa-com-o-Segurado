"""
Script de Demonstração Interativa via Linha de Comando (CLI Didático).
Utiliza a biblioteca Rich para exibição visual estruturada de todos os agentes.
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.markdown import Markdown
from rich.prompt import Prompt

from src.agents.orchestrator import PipelineOrchestrator
from src.agents.collector_agent import WeatherCollectorAgent

console = Console()


def exibir_cabecalho():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🛡️ Seguros CloudIO - Desafio 5 (I2A2)[/bold cyan]\n"
        "[bold white]Ferramenta Inteligente para Comunicação Proativa com o Segurado[/bold white]\n"
        "[dim]Transformando seguros de um modelo reativo para uma abordagem preventiva com IA Multiagente[/dim]",
        border_style="cyan"
    ))


def menu_principal():
    exibir_cabecalho()
    collector = WeatherCollectorAgent()
    cenarios = collector.listar_cenarios_disponiveis()

    table = Table(title="🌦️ Cenários Meteorológicos de Demonstração Didática", show_lines=True)
    table.add_column("Opção", style="bold yellow", justify="center")
    table.add_column("ID", style="bold green")
    table.add_column("Nome do Cenário / Ameaça", style="bold white")
    table.add_column("Cidade / UF", style="cyan")

    for idx, c in enumerate(cenarios, 1):
        table.add_row(str(idx), c["id"], c["nome"], f"{c['cidade']} - {c['estado']}")

    table.add_row(str(len(cenarios) + 1), "TEMPO_REAL", "📡 Consulta API em Tempo Real (Open-Meteo)", "Qualquer Cidade")
    table.add_row("0", "SAIR", "🚪 Encerrar Demonstração", "-")

    console.print(table)
    escolha = Prompt.ask("\nEscolha uma opção de demonstração", default="1")
    return escolha, cenarios


def executar_demonstracao_cli():
    orchestrator = PipelineOrchestrator()

    while True:
        escolha, cenarios = menu_principal()

        if escolha == "0":
            console.print("\n[bold green]Obrigado por utilizar a demonstração Seguros CloudIO![/bold green]\n")
            break

        modo = "cenario"
        identificador = "CENARIO-01"

        try:
            opcao_num = int(escolha)
            if 1 <= opcao_num <= len(cenarios):
                identificador = cenarios[opcao_num - 1]["id"]
                modo = "cenario"
            elif opcao_num == len(cenarios) + 1:
                modo = "tempo_real"
                cidade_input = Prompt.ask("Digite o nome da cidade brasileira para consulta", default="São Paulo")
                identificador = cidade_input
            else:
                console.print("[red]Opção inválida.[/red]")
                time.sleep(1.5)
                continue
        except ValueError:
            console.print("[red]Entrada inválida.[/red]")
            time.sleep(1.5)
            continue

        console.print(f"\n[bold yellow]🚀 Iniciando Orquestração do Pipeline Multiagente ({modo.upper()}: {identificador})...[/bold yellow]\n")

        resultado = orchestrator.executar_pipeline(modo=modo, identificador=identificador)

        # Exibição dos Passos dos Agentes
        tree = Tree("[bold magenta]🤖 Rastro de Execução dos Agentes Especializados[/bold magenta]")
        for r in resultado.rastros_agentes:
            nodo = tree.add(f"[bold cyan]Passo {r.passo}: {r.nome_agente}[/bold cyan] [dim]({r.papel})[/dim] - [green]{r.tempo_ms:.1f}ms[/green]")
            nodo.add(f"[white]{r.detalhes}[/white]")
        console.print(tree)
        console.print()

        # Tabela de Alertas Climáticos
        if resultado.alertas_identificados:
            t_alertas = Table(title="⚠️ Alertas Críticos Identificados pelo Agente de Risco", show_lines=True)
            t_alertas.add_column("Tipo de Ameaça", style="bold red")
            t_alertas.add_column("Severidade", style="bold yellow")
            t_alertas.add_column("Local", style="cyan")
            t_alertas.add_column("Detalhamento Técnico", style="white")

            for a in resultado.alertas_identificados:
                t_alertas.add_row(a.tipo_ameaca.value, a.severidade.value, f"{a.cidade} - {a.estado}", a.descricao_motivo)
            console.print(t_alertas)
            console.print()

        # Notificações Geradas
        if resultado.notificacoes_geradas:
            console.print(f"[bold green]📱 Notificações Proativas Geradas via IA ({len(resultado.notificacoes_geradas)} destinatários):[/bold green]\n")
            for idx, notif in enumerate(resultado.notificacoes_geradas, 1):
                panel_content = (
                    f"[bold yellow]Destinatário:[/bold yellow] {notif.segurado_nome} ({notif.segurado_telefone})\n"
                    f"[bold yellow]Apólice:[/bold yellow] {notif.apolice_id} | [bold yellow]Ramo:[/bold yellow] {notif.ramo.value} ({notif.bem_assegurado})\n"
                    f"[bold yellow]Canal:[/bold yellow] {notif.canal.value} | [bold yellow]Severidade:[/bold yellow] {notif.severidade.value}\n"
                    f"[bold yellow]Custo Evitado Estimado:[/bold yellow] R$ {notif.custo_sinistro_evitado_estimado_reais:,.2f}\n"
                    f"--------------------------------------------------\n"
                    f"[bold cyan]📱 Mensagem Enviada:[/bold cyan]\n\n"
                    f"{notif.mensagem_texto}\n\n"
                    f"[bold green]💬 Feedback do Segurado (Simulado):[/bold green] \"{notif.feedback_cliente}\""
                )
                console.print(Panel(panel_content, title=f"Mensagem #{idx} - {notif.canal.value}", border_style="green"))
        else:
            console.print(Panel("[bold green]✅ Nenhuma notificação necessária. Condições climáticas sem ameaça aos bens cadastrados.[/bold green]", border_style="green"))

        # Métricas de Impacto
        m = resultado.metricas
        t_metricas = Table(title="📊 Métricas de Eficiência e Impacto do Pipeline", show_lines=True)
        t_metricas.add_column("Métrica", style="bold white")
        t_metricas.add_column("Valor Consolidado", style="bold green", justify="right")
        t_metricas.add_row("Total de Segurados Avaliados", str(m.total_segurados_avaliados))
        t_metricas.add_row("Segurados em Área de Risco", str(m.total_segurados_em_risco))
        t_metricas.add_row("Notificações Proativas Disparadas", str(m.total_notificacoes_geradas))
        t_metricas.add_row("Economia Estimada em Sinistros Prevenidos", f"R$ {m.economia_sinistros_estimada_reais:,.2f}")
        t_metricas.add_row("Tempo Total de Execução do Pipeline", f"{m.tempo_execucao_segundos:.2f} segundos")
        console.print(t_metricas)

        input("\nPressione [ENTER] para voltar ao menu principal...")


if __name__ == "__main__":
    executar_demonstracao_cli()
