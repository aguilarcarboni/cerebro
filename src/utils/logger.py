from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme
import logging

class Logger:
    """
    Custom logger for the project
    """
    def __init__(self):
        custom_theme = Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "bold red",
            "critical": "bold white on red",
        })
        self.console = Console(theme=custom_theme)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(console=self.console, rich_tracebacks=True)]
        )
        self.logger = logging.getLogger("rich")

    def info(self, message):
        self.logger.debug(f"[blue]{message}[/blue]", extra={'markup': True})

    def success(self, message):
        self.logger.debug(f"[green]{message}[/green]", extra={'markup': True})

    def warning(self, message):
        self.logger.debug(f"[yellow]{message}[/yellow]", extra={'markup': True})

    def announcement(self, message, type='info'):
        if type == 'info':
            self.logger.info(f"[blue]{message}[/blue]", extra={'markup': True})
        elif type == 'matrix':
            self.logger.info(f"[green]{message}[/green]", extra={'markup': True})
        else:
            raise ValueError("Invalid type. Choose 'info' or 'success'.")

    def error(self, message):
        self.logger.error(f"[red]{message}[/red]\n", extra={'markup': True})

logger = Logger()