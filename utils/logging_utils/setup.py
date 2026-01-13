import logging
from rich.logging import RichHandler

def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()

    # prevent double handlers if main reloads / runs twice
    if any(isinstance(h, RichHandler) for h in root.handlers):
        root.setLevel(level)
        return

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )

    logging.getLogger("urllib3").setLevel(logging.WARNING)
