"""
Knowledge Graph vs Traditional RAG Demo

This script demonstrates the differences between Traditional RAG and Knowledge Graph-based RAG
using the CloudStore API documentation as sample data.
"""

import os
import asyncio
import random
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

from traditional_rag import TraditionalRAG
from knowledge_graph import KnowledgeGraphRAG
from comparison import compare_systems, run_comparison_suite, plot_comparison_metrics, visualize_graph

console = Console()


# Sample questions that highlight KG advantages
DEMO_QUESTIONS = [
    "What is PEP 8 and why is it important in Python projects?",
    "What is the recommended indentation and line length in Python?",
    "Why should variable and function names be descriptive?",
    "Why should global variables be avoided?",
    "When should constants be used, and how should they be named?",
    "What are the differences between list, tuple, set, and dictionary?"
]


def print_suggestions_table():
    """Print suggested questions in a Rich table."""
    table = Table(title="Suggested questions", box=box.ROUNDED, show_header=True)
    table.add_column("#", style="cyan", width=4)
    table.add_column("Question", style="white")
    for i, q in enumerate(DEMO_QUESTIONS, 1):
        table.add_row(str(i), q)
    console.print(table)


def display_comparison_interactive(comparison: Dict[str, Any]) -> None:
    """Display comparison results in an interactive, step-by-step layout (demo.py only)."""
    n = len(DEMO_QUESTIONS)
    console.print("\n" + "=" * 80)
    console.print("[bold green]COMPARISON RESULTS[/bold green]")
    console.print("=" * 80)

    console.print(Panel(comparison["question"], title="[bold]Question[/bold]", border_style="yellow"))

    console.print("\n[bold cyan]Traditional RAG Answer:[/bold cyan]")
    console.print(Panel(comparison["rag_result"]["answer"], border_style="blue"))

    console.input("\n[dim]Press Enter to see Knowledge Graph answer...[/dim]")

    console.print("\n[bold magenta]Knowledge Graph RAG Answer:[/bold magenta]")
    console.print(Panel(comparison["kg_result"]["answer"], border_style="magenta"))

    console.input("\n[dim]Press Enter to see metrics...[/dim]")

    m = comparison["comparison_metrics"]
    rag_time, kg_time = m["rag_time"], m["kg_time"]
    speedup = m["speedup"]
    time_diff = "RAG faster" if speedup < 1 else f"KG faster ({speedup:.2f}x)"

    table = Table(title="Performance Metrics", box=box.ROUNDED, show_header=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Traditional RAG", style="blue")
    table.add_column("Knowledge Graph RAG", style="magenta")
    table.add_column("Difference", style="green")
    table.add_row("Query Time", f"{rag_time:.2f}s", f"{kg_time:.2f}s", time_diff)
    table.add_row(
        "Retrieved Items",
        f"{m['rag_sources']} chunks",
        f"{m['kg_facts']} facts",
        f"+{m['kg_facts'] - m['rag_sources']}",
    )
    table.add_row("Entities Identified", "N/A", str(m["kg_entities"]), "KG advantage")
    table.add_row("Relationships Found", "N/A", str(m["kg_relationships"]), "KG advantage")
    console.print("\n", table)

    console.print("\n[bold yellow]Key Insights:[/bold yellow]")
    if m["kg_entities"] > 0:
        console.print(f"  • KG identified {m['kg_entities']} entities and their relationships")
    if m["kg_facts"] > m["rag_sources"]:
        console.print(f"  • KG retrieved {m['kg_facts'] - m['rag_sources']} more relevant facts")
    console.print("  • KG provides structured, relationship-aware context")
    console.print("  • Traditional RAG provides chunk-based context\n")


def setup_environment():
    """Load and validate environment variables."""
    load_dotenv()

    required_vars = [
        "OPENAI_API_KEY",
        "NEO4J_URI",
        "NEO4J_USERNAME",
        "NEO4J_PASSWORD"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        console.print(f"[bold red]Error: Missing required environment variables:[/bold red]")
        for var in missing_vars:
            console.print(f"  - {var}")
        console.print("\n[yellow]Please create a .env file based on .env.example[/yellow]")
        return False

    return True


async def initialize_systems():
    """Initialize both RAG systems."""
    console.print("\n[bold cyan]Initializing Systems...[/bold cyan]\n")

    # Load configuration
    openai_api_key = os.getenv("OPENAI_API_KEY")
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    # Initialize Traditional RAG
    console.print("[yellow]1. Initializing Traditional RAG...[/yellow]")
    rag_system = TraditionalRAG(
        openai_api_key=openai_api_key,
        model_name=model_name,
        embedding_model=embedding_model
    )

    # Load and index documents
    doc_path = Path("sample_data/py_best_practice.txt")
    if not doc_path.exists():
        console.print(f"[bold red]Error: Sample data not found at {doc_path}[/bold red]")
        return None, None

    documents = rag_system.load_documents(str(doc_path))
    rag_system.build_index(documents)
    console.print("[green][OK] Traditional RAG initialized[/green]\n")

    # Initialize Knowledge Graph RAG
    console.print("[yellow]2. Initializing Knowledge Graph RAG...[/yellow]")
    kg_system = KnowledgeGraphRAG(
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_username,
        neo4j_password=neo4j_password,
        openai_api_key=openai_api_key,
        model_name=model_name
    )

    # Build required Neo4j indexes and constraints
    await kg_system.graphiti.build_indices_and_constraints()

    # Check if we should rebuild the graph
    stats = kg_system.get_graph_statistics()
    if stats['total_nodes'] > 0:
        console.print(f"[yellow]Found existing graph with {stats['total_nodes']} nodes[/yellow]")
        rebuild = Confirm.ask("Do you want to rebuild the knowledge graph?", default=False)
        if rebuild:
            kg_system.clear_graph()
            stats = kg_system.get_graph_statistics()

    # Build knowledge graph if needed
    if stats['total_nodes'] == 0:
        console.print("[yellow]Building knowledge graph (this may take a few minutes)...[/yellow]")
        # Split documents for KG
        doc_texts = [doc.page_content for doc in documents]
        await kg_system.add_documents_to_graph(doc_texts, source="py_best_practice")

        stats = kg_system.get_graph_statistics()
        console.print(f"[green][OK] Knowledge Graph initialized[/green]")
        console.print(f"  - Nodes: {stats['total_nodes']}")
        console.print(f"  - Relationships: {stats['total_relationships']}")
        console.print(f"  - Entities: {stats['num_entities']}")
        console.print(f"  - Episodes: {stats['num_episodes']}\n")
    else:
        console.print(f"[green][OK] Using existing Knowledge Graph[/green]")
        console.print(f"  - Nodes: {stats['total_nodes']}")
        console.print(f"  - Relationships: {stats['total_relationships']}")
        console.print(f"  - Entities: {stats['num_entities']}")
        console.print(f"  - Episodes: {stats['num_episodes']}\n")

    return rag_system, kg_system


async def run_single_comparison(rag_system, kg_system):
    """Run a single question comparison."""
    console.print("\n[bold cyan]Single Question Comparison[/bold cyan]\n")

    print_suggestions_table()
    n = len(DEMO_QUESTIONS)
    console.print(
        f"\n[yellow]Enter number [bold]1-{n}[/bold] for a suggestion, [bold]0[/bold] for a random question, "
        "or type your own question.[/yellow]"
    )

    while True:
        user_input = Prompt.ask("Question").strip()
        if not user_input:
            console.print("[red]Please enter a number or a question.[/red]")
            continue
        if user_input.isdigit():
            num = int(user_input)
            if num == 0:
                question = random.choice(DEMO_QUESTIONS)
                break
            if 1 <= num <= n:
                question = DEMO_QUESTIONS[num - 1]
                break
            console.print(f"[red]Please enter a number between 1 and {n}, or 0 for random.[/red]")
            continue
        question = user_input
        break

    console.print(Panel(question, title="[bold]Using question[/bold]", border_style="green"))
    console.print("\n[yellow]Querying both systems...[/yellow]\n")

    result = await compare_systems(rag_system, kg_system, question, verbose=False)
    display_comparison_interactive(result)


async def run_full_comparison_suite(rag_system, kg_system):
    """Run the full comparison suite with all demo questions."""
    console.print("\n[bold cyan]Running Full Comparison Suite[/bold cyan]\n")
    console.print(f"This will test both systems with {len(DEMO_QUESTIONS)} predefined questions.\n")

    confirm = Confirm.ask("Continue?", default=True)
    if not confirm:
        return

    # Run suite
    results = await run_comparison_suite(rag_system, kg_system, DEMO_QUESTIONS)

    # Generate visualizations
    console.print("\n[yellow]Generating comparison visualizations...[/yellow]")
    plot_comparison_metrics(results, "comparison_metrics.png")
    console.print("[green][OK] Metrics plot saved to: comparison_metrics.png[/green]")


def visualize_knowledge_graph(kg_system):
    """Generate knowledge graph visualization."""
    console.print("\n[bold cyan]Generating Knowledge Graph Visualization[/bold cyan]\n")

    visualize_graph(
        neo4j_uri=os.getenv("NEO4J_URI"),
        neo4j_user=os.getenv("NEO4J_USERNAME"),
        neo4j_password=os.getenv("NEO4J_PASSWORD"),
        output_file="knowledge_graph.html",
        max_nodes=100
    )

    console.print("[green][OK] Visualization saved to: knowledge_graph.html[/green]")
    console.print("[yellow]Open this file in a web browser to explore the graph interactively[/yellow]")


async def interactive_mode(rag_system, kg_system):
    """Run interactive question-answering mode."""
    console.print("\n[bold cyan]Interactive Mode[/bold cyan]\n")
    console.print(
        "[yellow]Ask questions about the Python best practices / sample docs.[/yellow]\n"
        "[dim]Type [bold]list[/bold] for suggestions, [bold]exit[/bold] to quit.[/dim]\n"
    )

    while True:
        question = Prompt.ask("\n[bold]Your question[/bold]").strip()

        if question.lower() in ["exit", "quit", "q"]:
            break

        if question.lower() in ["list", "suggest", "suggestions"]:
            print_suggestions_table()
            continue

        if not question:
            console.print("[red]Please enter a question (or 'list' / 'exit').[/red]")
            continue

        console.print("\n[yellow]Querying both systems...[/yellow]\n")
        result = await compare_systems(rag_system, kg_system, question, verbose=False)
        display_comparison_interactive(result)
        console.print("[dim]Ask another, type [bold]list[/bold] for ideas, or [bold]exit[/bold] to quit.[/dim]")


async def main():
    """Main demo function."""
    console.print(Panel.fit(
        "[bold green]Knowledge Graph vs Traditional RAG Demo[/bold green]\n"
        "Demonstrating the advantages of Knowledge Graph-based RAG over Traditional RAG",
        border_style="green"
    ))

    # Setup
    if not setup_environment():
        return

    # Initialize systems
    rag_system, kg_system = await initialize_systems()
    if not rag_system or not kg_system:
        return

    # Main menu
    while True:
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]Demo Menu[/bold cyan]")
        console.print("=" * 80)
        console.print("1. Run single question comparison")
        console.print("2. Run full comparison suite (all demo questions)")
        console.print("3. Visualize knowledge graph")
        console.print("4. Interactive mode (ask your own questions)")
        console.print("5. View graph statistics")
        console.print("6. Exit")

        choice = Prompt.ask("\n[bold]Select an option[/bold]", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            await run_single_comparison(rag_system, kg_system)
        elif choice == "2":
            await run_full_comparison_suite(rag_system, kg_system)
        elif choice == "3":
            visualize_knowledge_graph(kg_system)
        elif choice == "4":
            await interactive_mode(rag_system, kg_system)
        elif choice == "5":
            stats = kg_system.get_graph_statistics()
            console.print("\n[bold cyan]Knowledge Graph Statistics:[/bold cyan]")
            console.print(f"  - Total Nodes: {stats['total_nodes']}")
            console.print(f"  - Total Relationships: {stats['total_relationships']}")
            console.print(f"  - Entities: {stats['num_entities']}")
            console.print(f"  - Episodes: {stats['num_episodes']}")
        elif choice == "6":
            console.print("\n[bold green]Thank you for using the demo![/bold green]")
            kg_system.close()
            break


if __name__ == "__main__":
    asyncio.run(main())