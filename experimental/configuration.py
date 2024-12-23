"""Define the configurable parameters for the agent."""

from __future__ import annotations
from typing import Optional, Type, TypeVar
from langchain_core.runnables import RunnableConfig, ensure_config
from pydantic import BaseModel, Field

class BaseConfiguration(BaseModel):
    """Configuration class for indexing and retrieval operations.

    This class defines the parameters needed for configuring the indexing and
    retrieval processes, including embedding model selection, retriever provider choice, and search parameters.
    """

    @classmethod
    def from_runnable_config(
        cls: Type[T], config: Optional[RunnableConfig] = None
    ) -> T:
        """Create an IndexConfiguration instance from a RunnableConfig object.

        Args:
            cls (Type[T]): The class itself.
            config (Optional[RunnableConfig]): The configuration object to use.

        Returns:
            T: An instance of IndexConfiguration with the specified configuration.
        """
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        return cls(**configurable)


T = TypeVar("T", bound=BaseConfiguration)
