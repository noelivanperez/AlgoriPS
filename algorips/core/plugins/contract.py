"""Plugin contract definitions."""

from abc import ABC, abstractmethod
from typing import Any


class BasePlugin(ABC):
    """Base class for all plugins.

    Each plugin must implement the required methods. The :meth:`register`
    method is called by :class:`PluginManager` to allow the plugin to
    extend the CLI and GUI.
    """

    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the plugin."""

    @abstractmethod
    def version(self) -> str:
        """Return the plugin version."""

    @abstractmethod
    def register(self, cli: Any, gui_registry: Any) -> None:
        """Register hooks with CLI and GUI.

        Parameters
        ----------
        cli:
            CLI application object where commands can be registered.
        gui_registry:
            Registry or router used by the GUI to expose plugin features.
        """

    @property
    def description(self) -> str:
        """Short summary of what the plugin provides."""
        return ""

    @property
    def dependencies(self) -> list[str]:
        """List optional external dependencies required by the plugin."""
        return []
