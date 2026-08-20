"""Logging and performance decorators."""
from __future__ import annotations
import functools
import logging
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def timed(func: F) -> F:
    """Log execution time for a function."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logging.getLogger(func.__module__).info("%s completed in %.3fs", func.__name__, elapsed)
        return result
    return wrapper  # type: ignore[return-value]

def logged(func: F) -> F:
    """Log function entry and exit."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        log = logging.getLogger(func.__module__)
        log.info("Starting %s", func.__name__)
        try:
            result = func(*args, **kwargs)
            log.info("Finished %s", func.__name__)
            return result
        except Exception:
            log.exception("%s failed", func.__name__)
            raise
    return wrapper  # type: ignore[return-value]
