# -*- coding: utf-8 -*-
"""Import the entry point of AgentScope Studio."""
from ._app import init, as_studio
from ._app_online import as_workstation

__all__ = ["init", "as_studio"]
