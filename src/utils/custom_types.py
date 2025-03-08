from collections.abc import Awaitable, Callable
from typing import Any


AsyncFunc = Callable[..., Awaitable[Any]]

