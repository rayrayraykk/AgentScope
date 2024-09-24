# -*- coding: utf-8 -*-
"""A dummy agent."""
from typing import Optional, Union, Sequence

from ..message import Msg
from .agent import AgentBase


class BroadcastAgent(AgentBase):
    """A dummy agent used to only speak what he gets."""

    def __init__(
        self,
        name: str,
        content: str,
        sys_prompt: str = None,
        model_config_name: str = None,
        use_memory: bool = False,
        memory_config: Optional[dict] = None,
    ) -> None:
        """Initialize the dummy agent.

        Arguments:
            name (`str`):
                The name of the agent.
            sys_prompt (`Optional[str]`):
                The system prompt of the agent, which can be passed by args
                or hard-coded in the agent.
            model_config_name (`str`):
                The name of the model config, which is used to load model from
                configuration.
            use_memory (`bool`, defaults to `True`):
                Whether the agent has memory.
            memory_config (`Optional[dict]`):
                The config of memory.
        """
        super().__init__(
            name=name,
            sys_prompt=sys_prompt,
            model_config_name=model_config_name,
            use_memory=use_memory,
            memory_config=memory_config,
        )
        self.content = content

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        """Reply function of the agent. Processes the input data,
        generates a prompt using the current dialogue memory and system
        prompt, and invokes the language model to produce a response. The
        response is then formatted and added to the dialogue memory.

        Args:
            x (`Optional[Union[Msg, Sequence[Msg]]]`, defaults to `None`):
                The input message(s) to the agent, which also can be omitted if
                the agent doesn't need any input.

        Returns:
            `Msg`: The output message generated by the agent.
        """

        # Print/speak the message in this agent's voice
        # Support both streaming and non-streaming responses by "or"
        msg = Msg(name=self.name, content=self.content, role="assistant")
        self.speak(msg)

        return msg
