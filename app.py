#!/usr/bin/env python3
"""
Valorant Stats Scraper - Terminal UI Application
Interactive application for fetching and processing Valorant player statistics
"""

from textual.app import ComposeResult, RenderableType
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Label, RichLog
from textual.binding import Binding
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
import os


class StatusBar(Static):
    """Display current status"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_text = "Ready"
    
    def update_status(self, text: str):
        self.status_text = text
        self.update(self._render_status())
    
    def _render_status(self):
        return Panel(
            Align.center(Text(self.status_text, style="bold cyan")),
            style="green",
            height=3
        )
    
    def render(self) -> RenderableType:
        return self._render_status()


class LogViewer(RichLog):
    """Custom log viewer with styling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, markup=True)
        self.write(Panel(
            Align.center(Text("Valorant Stats Scraper - v1.0", style="bold magenta")),
            title="[bold cyan]Welcome[/bold cyan]",
            style="blue"
        ))
        self.write("\n[dim]Ready to process player statistics[/dim]\n")


class ValorantApp:
    """Main Valorant Terminal Application using Textual"""
    
    def __init__(self):
        from textual.app import App as TextualApp
        
        class App(TextualApp):
            CSS = """
            Screen {
                layout: vertical;
            }
            
            #main_container {
                height: 1fr;
            }
            
            #sidebar {
                width: 30;
                border: solid $accent;
                background: $boost;
            }
            
            .menu_title {
                dock: top;
                height: 1;
                background: $primary;
                text-align: center;
            }
            
            Button {
                margin: 0 1;
                width: 100%;
                margin-top: 1;
            }
            
            #content {
                width: 1fr;
                border: solid $accent;
            }
            
            #status_bar {
                height: 5;
            }
            
            .log_container {
                background: $surface;
                border-top: solid $accent;
            }
            """
            
            BINDINGS = [
                Binding("q", "quit", "Quit", show=True),
            ]
            
            def on_mount(self):
                self.title = "Valorant Stats Scraper"
                self.sub_title = "Interactive Terminal UI"
            
            def compose(self) -> ComposeResult:
                yield Header(show_clock=True)
                
                with Horizontal(id="main_container"):
                    with Vertical(id="sidebar", classes="sidebar"):
                        yield Label("[bold cyan]═══ MENU ═══[/bold cyan]", classes="menu_title")
                        yield Button("▶ Fetch Stats", id="fetch_stats", variant="primary")
                        yield Button("▶ Fetch Premier", id="fetch_premier", variant="primary")
                        yield Button("▶ Export to Excel", id="export_excel", variant="primary")
                        yield Button("▶ View Results", id="view_results", variant="default")
                        yield Button("▶ Clear Logs", id="clear_logs", variant="default")
                        yield Button("✕ Exit", id="exit_app", variant="error")
                    
                    with Vertical(id="content"):
                        yield StatusBar(id="status_bar")
                        yield LogViewer(id="log_viewer", classes="log_container")
                
                yield Footer()
            
            def on_button_pressed(self, event: Button.Pressed) -> None:
                """Handle button presses"""
                button_id = event.button.id
                log_viewer = self.query_one("#log_viewer", LogViewer)
                status_bar = self.query_one("#status_bar", StatusBar)
                
                if button_id == "fetch_stats":
                    self._fetch_stats(log_viewer, status_bar)
                elif button_id == "fetch_premier":
                    self._fetch_premier(log_viewer, status_bar)
                elif button_id == "export_excel":
                    self._export_excel(log_viewer, status_bar)
                elif button_id == "view_results":
                    self._view_results(log_viewer, status_bar)
                elif button_id == "clear_logs":
                    log_viewer.clear()
                    status_bar.update_status("Logs cleared")
                elif button_id == "exit_app":
                    self.exit()
            
            def _fetch_stats(self, log_viewer: LogViewer, status_bar: StatusBar):
                """Fetch competitive stats"""
                try:
                    from main import fetch_competitive_stats
                    status_bar.update_status("⏳ Fetching competitive stats...")
                    log_viewer.write("[bold cyan]→ Starting competitive stats fetch...[/bold cyan]")
                    
                    count = fetch_competitive_stats(log_viewer)
                    log_viewer.write(f"[green]✓ Fetched stats for {count} players[/green]")
                    status_bar.update_status(f"✓ Completed: {count} players")
                except Exception as e:
                    log_viewer.write(f"[red]✗ Error: {str(e)}[/red]")
                    status_bar.update_status(f"✗ Error: {str(e)}")
            
            def _fetch_premier(self, log_viewer: LogViewer, status_bar: StatusBar):
                """Fetch premier stats"""
                try:
                    from premier import fetch_premier_stats
                    status_bar.update_status("⏳ Fetching premier stats...")
                    log_viewer.write("[bold yellow]→ Starting premier stats fetch...[/bold yellow]")
                    
                    count = fetch_premier_stats(log_viewer)
                    log_viewer.write(f"[green]✓ Fetched premier stats for {count} players[/green]")
                    status_bar.update_status(f"✓ Completed: {count} players")
                except Exception as e:
                    log_viewer.write(f"[red]✗ Error: {str(e)}[/red]")
                    status_bar.update_status(f"✗ Error: {str(e)}")
            
            def _export_excel(self, log_viewer: LogViewer, status_bar: StatusBar):
                """Export stats to Excel"""
                try:
                    from estadisticas import exportar_stats_a_xlsx
                    status_bar.update_status("⏳ Exporting to Excel...")
                    log_viewer.write("[bold magenta]→ Starting Excel export...[/bold magenta]")
                    
                    exportar_stats_a_xlsx()
                    log_viewer.write("[green]✓ Excel files exported successfully[/green]")
                    status_bar.update_status("✓ Excel export completed")
                except Exception as e:
                    log_viewer.write(f"[red]✗ Error: {str(e)}[/red]")
                    status_bar.update_status(f"✗ Error: {str(e)}")
            
            def _view_results(self, log_viewer: LogViewer, status_bar: StatusBar):
                """View current results"""
                log_viewer.write("[bold blue]═══ RESULTS SUMMARY ═══[/bold blue]")
                
                if os.path.exists('stats'):
                    files = [f for f in os.listdir('stats') if f.endswith('.json')]
                    log_viewer.write(f"\n[cyan]Competitive Stats: {len(files)} files[/cyan]")
                    for file in files[:5]:
                        log_viewer.write(f"  • {file}")
                    if len(files) > 5:
                        log_viewer.write(f"  ... and {len(files) - 5} more")
                
                if os.path.exists('stats_premier'):
                    files = [f for f in os.listdir('stats_premier') if f.endswith('.json')]
                    log_viewer.write(f"\n[yellow]Premier Stats: {len(files)} files[/yellow]")
                    for file in files[:5]:
                        log_viewer.write(f"  • {file}")
                    if len(files) > 5:
                        log_viewer.write(f"  ... and {len(files) - 5} more")
                
                status_bar.update_status("Viewing results")
        
        self.app = App()
    
    def run(self):
        """Run the application"""
        self.app.run()


def main():
    """Entry point"""
    app = ValorantApp()
    app.run()


if __name__ == "__main__":
    main()
