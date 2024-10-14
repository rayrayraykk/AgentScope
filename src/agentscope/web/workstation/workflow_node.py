# -*- coding: utf-8 -*-
"""Workflow node opt."""
import ast
from abc import ABC
from enum import IntEnum
from functools import partial
from typing import List, Optional, Any
import json
import re
from textwrap import dedent
from agentscope import msghub
from agentscope.agents import (
    DialogAgent,
    UserAgent,
    TextToImageAgent,
    DictDialogAgent,
    ReActAgent,
)
from agentscope.manager import ModelManager
from agentscope.message import Msg
from agentscope.pipelines import (
    SequentialPipeline,
    ForLoopPipeline,
    WhileLoopPipeline,
    IfElsePipeline,
    SwitchPipeline,
)
from agentscope.pipelines.functional import placeholder
from agentscope.web.workstation.workflow_utils import (
    convert_str_to_callable,
    is_callable_expression,
)
from agentscope.service import (
    bing_search,
    google_search,
    read_text_file,
    write_text_file,
    execute_python_code,
    dashscope_text_to_audio,
    dashscope_text_to_image,
    ServiceToolkit,
    ServiceExecStatus,
)
from agentscope.studio.tools.image_composition import stitch_images_with_grid
from agentscope.studio.tools.image_motion import create_video_or_gif_from_image
from agentscope.studio.tools.video_composition import merge_videos
from agentscope.studio.tools.condition_operator import eval_condition_operator

from agentscope.studio.tools.web_post import web_post

DEFAULT_FLOW_VAR = "flow"


class WorkflowNodeType(IntEnum):
    """Enum for workflow node."""

    MODEL = 0
    AGENT = 1
    PIPELINE = 2
    SERVICE = 3
    MESSAGE = 4
    COPY = 5
    TOOL = 6
    START = 7
    IFELSE = 8


class WorkflowNode(ABC):
    """
    Abstract base class representing a generic node in a workflow.

    WorkflowNode is designed to be subclassed with specific logic implemented
    in the subclass methods. It provides an interface for initialization and
    execution of operations when the node is called.
    """

    node_type = None

    def __init__(
        self,
        node_id: str,
        opt_kwargs: dict,
        source_kwargs: dict,
        dep_opts: list,
    ) -> None:
        """
        Initialize nodes. Implement specific initialization logic in
        subclasses.
        """

        self.node_id = node_id
        self.opt_kwargs = opt_kwargs
        self.source_kwargs = source_kwargs
        self.dep_opts = dep_opts
        self.dep_vars = [opt.var_name for opt in self.dep_opts]
        self.var_name = f"{self.node_type.name.lower()}_{self.node_id}"
        self.source_kwargs.pop("condition_op", "")
        self.source_kwargs.pop("target_value", "")
        self._post_init()

    def _post_init(self) -> None:
        # Warning: Might cause error when args is still string
        for key, value in self.opt_kwargs.items():
            if is_callable_expression(value):
                self.opt_kwargs[key] = convert_str_to_callable(value)

    def __call__(self, x: Any = None):  # type: ignore[no-untyped-def]
        """
        Invokes the node's operations with the provided input.

        This method is designed to be called as a function. It delegates the
        actual execution of the node's logic to the _execute method.
        Subclasses should implement their specific logic in the
        `_execute` method.
        """
        return x


class ModelNode(WorkflowNode):
    """
    A node that represents a model in a workflow.

    The ModelNode can be used to load and execute a model as part of the
    workflow node. It initializes model configurations and performs
    model-related operations when called.
    """

    node_type = WorkflowNodeType.MODEL

    def _post_init(self) -> None:
        super()._post_init()
        ModelManager.get_instance().load_model_configs([self.opt_kwargs])


class StartNode(WorkflowNode):
    """
    A node that represents a start in a workflow.
    """

    node_type = WorkflowNodeType.START


class MsgNode(WorkflowNode):
    """
    A node that manages messaging within a workflow.

    MsgNode is responsible for handling messages, creating message objects,
    and performing message-related operations when the node is invoked.
    """

    node_type = WorkflowNodeType.MESSAGE

    def _post_init(self) -> None:
        super()._post_init()
        self.msg = Msg(**self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.msg


class DialogAgentNode(WorkflowNode):
    """
    A node representing a DialogAgent within a workflow.
    """

    node_type = WorkflowNodeType.AGENT

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = DialogAgent(**self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class UserAgentNode(WorkflowNode):
    """
    A node representing a UserAgent within a workflow.
    """

    node_type = WorkflowNodeType.AGENT

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = UserAgent(**self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class TextToImageAgentNode(WorkflowNode):
    """
    A node representing a TextToImageAgent within a workflow.
    """

    node_type = WorkflowNodeType.AGENT

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = TextToImageAgent(**self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class DictDialogAgentNode(WorkflowNode):
    """
    A node representing a DictDialogAgent within a workflow.
    """

    node_type = WorkflowNodeType.AGENT

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = DictDialogAgent(**self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class ReActAgentNode(WorkflowNode):
    """
    A node representing a ReActAgent within a workflow.
    """

    node_type = WorkflowNodeType.AGENT

    def _post_init(self) -> None:
        super()._post_init()
        # Build tools
        self.service_toolkit = ServiceToolkit()
        for tool in self.dep_opts:
            if not hasattr(tool, "service_func"):
                raise TypeError(f"{tool} must be tool!")
            self.service_toolkit.add(tool.service_func)
        self.pipeline = ReActAgent(
            service_toolkit=self.service_toolkit,
            **self.opt_kwargs,
        )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class MsgHubNode(WorkflowNode):
    """
    A node that serves as a messaging hub within a workflow.

    MsgHubNode is responsible for broadcasting announcements to participants
    and managing the flow of messages within a workflow's node.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        super()._post_init()
        self.announcement = Msg(
            name=self.opt_kwargs["announcement"].get("name", "Host"),
            content=self.opt_kwargs["announcement"].get("content", "Welcome!"),
            role="system",
        )
        assert len(self.dep_opts) == 1 and hasattr(
            self.dep_opts[0],
            "pipeline",
        ), (
            "MsgHub members must be a list of length 1, with the first "
            "element being an instance of PipelineBaseNode"
        )

        self.pipeline = self.dep_opts[0]
        self.participants = get_all_agents(self.pipeline)
        self.participants_var = get_all_agents(self.pipeline, return_var=True)

    def __call__(self, x: dict = None) -> dict:
        with msghub(self.participants, announcement=self.announcement):
            x = self.pipeline(x)
        return x


class PlaceHolderNode(WorkflowNode):
    """
    A placeholder node within a workflow.

    This node acts as a placeholder and can be used to pass through information
    or data without performing any significant operation.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = placeholder

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class SequentialPipelineNode(WorkflowNode):
    """
    A node representing a sequential node within a workflow.

    SequentialPipelineNode executes a series of operators or nodes in a
    sequence, where the output of one node is the input to the next.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = SequentialPipeline(operators=self.dep_opts)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class ForLoopPipelineNode(WorkflowNode):
    """
    A node representing a for-loop structure in a workflow.

    ForLoopPipelineNode allows the execution of a pipeline node multiple times,
    iterating over a given set of inputs or a specified range.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        # Not call super post init to avoid converting callable
        self.condition_op = self.opt_kwargs.pop("condition_op", "")
        self.target_value = self.opt_kwargs.pop("target_value", "")
        self.opt_kwargs["break_func"] = partial(
            eval_condition_operator,
            operator=self.condition_op,
            target_value=self.target_value,
        )

        assert (
            len(self.dep_opts) == 1
        ), "ForLoopPipelineNode can only contain one PipelineNode."
        self.pipeline = ForLoopPipeline(
            loop_body_operators=self.dep_opts[0],
            **self.opt_kwargs,
        )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class WhileLoopPipelineNode(WorkflowNode):
    """
    A node representing a while-loop structure in a workflow.

    WhileLoopPipelineNode enables conditional repeated execution of a node
    node based on a specified condition.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        super()._post_init()
        assert (
            len(self.dep_opts) == 1
        ), "WhileLoopPipelineNode can only contain one PipelineNode."
        self.pipeline = WhileLoopPipeline(
            loop_body_operators=self.dep_opts[0],
            **self.opt_kwargs,
        )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class IfElsePipelineNode(WorkflowNode):
    """
    A node representing an if-else conditional structure in a workflow.

    IfElsePipelineNode directs the flow of execution to different node
    nodes based on a specified condition.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        # Not call super post init to avoid converting callable
        self.condition_op = self.opt_kwargs.pop("condition_op", "")
        self.target_value = self.opt_kwargs.pop("target_value", "")
        self.opt_kwargs["condition_func"] = partial(
            eval_condition_operator,
            operator=self.condition_op,
            target_value=self.target_value,
        )

        assert (
            0 < len(self.dep_opts) <= 2
        ), "IfElsePipelineNode must contain one or two PipelineNode."
        if len(self.dep_opts) == 1:
            self.pipeline = IfElsePipeline(
                if_body_operators=self.dep_opts[0],
                **self.opt_kwargs,
            )
        elif len(self.dep_opts) == 2:
            self.pipeline = IfElsePipeline(
                if_body_operators=self.dep_opts[0],
                else_body_operators=self.dep_opts[1],
                **self.opt_kwargs,
            )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class SwitchPipelineNode(WorkflowNode):
    """
    A node representing a switch-case structure within a workflow.

    SwitchPipelineNode routes the execution to different node nodes
    based on the evaluation of a specified key or condition.
    """

    node_type = WorkflowNodeType.PIPELINE

    def _post_init(self) -> None:
        super()._post_init()
        assert 0 < len(self.dep_opts), (
            "SwitchPipelineNode must contain at least " "one PipelineNode."
        )
        case_operators = {}
        self.case_operators_var = {}

        if len(self.dep_opts) == len(self.opt_kwargs["cases"]):
            # No default_operators provided
            default_operators = placeholder
            self.default_var_name = "placeholder"
        elif len(self.dep_opts) == len(self.opt_kwargs["cases"]) + 1:
            # default_operators provided
            default_operators = self.dep_opts.pop(-1)
            self.default_var_name = self.dep_vars.pop(-1)
        else:
            raise ValueError(
                f"SwitchPipelineNode deps {self.dep_opts} not matches "
                f"cases {self.opt_kwargs['cases']}.",
            )

        for key, value, var in zip(
            self.opt_kwargs["cases"],
            self.dep_opts,
            self.dep_vars,
        ):
            case_operators[key] = value.pipeline
            self.case_operators_var[key] = var
        self.opt_kwargs.pop("cases")
        self.source_kwargs.pop("cases")
        self.pipeline = SwitchPipeline(
            case_operators=case_operators,
            default_operators=default_operators,  # type: ignore[arg-type]
            **self.opt_kwargs,
        )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class CopyNode(WorkflowNode):
    """
    A node that duplicates the output of another node in the workflow.

    CopyNode is used to replicate the results of a parent node and can be
    useful in workflows where the same output is needed for multiple
    subsequent operations.
    """

    node_type = WorkflowNodeType.COPY

    def _post_init(self) -> None:
        super()._post_init()
        assert len(self.dep_opts) == 1, "CopyNode can only have one parent!"
        self.pipeline = self.dep_opts[0]
        self.var_name = self.pipeline.var_name

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class BingSearchServiceNode(WorkflowNode):
    """
    Bing Search Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = partial(bing_search, **self.opt_kwargs)


class GoogleSearchServiceNode(WorkflowNode):
    """
    Google Search Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = partial(google_search, **self.opt_kwargs)


class PythonServiceNode(WorkflowNode):
    """
    Execute python Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = execute_python_code


class ReadTextServiceNode(WorkflowNode):
    """
    Read Text Service Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = read_text_file


class WriteTextServiceNode(WorkflowNode):
    """
    Write Text Service Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = write_text_file


class PostNode(WorkflowNode):
    """Post Node"""

    node_type = WorkflowNodeType.TOOL

    def _post_init(self) -> None:
        super()._post_init()
        if "kwargs" in self.opt_kwargs:
            kwargs = ast.literal_eval(self.opt_kwargs["kwargs"].strip())
            del self.opt_kwargs["kwargs"]
            self.opt_kwargs.update(**kwargs)

        self.pipeline = partial(web_post, **self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class TextToAudioServiceNode(WorkflowNode):
    """
    Text to Audio Service Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = partial(dashscope_text_to_audio, **self.opt_kwargs)


class TextToImageServiceNode(WorkflowNode):
    """
    Text to Image Service Node
    """

    node_type = WorkflowNodeType.SERVICE

    def _post_init(self) -> None:
        super()._post_init()
        self.service_func = partial(dashscope_text_to_image, **self.opt_kwargs)


class ImageCompositionNode(WorkflowNode):
    """
    Image Composition Node
    """

    node_type = WorkflowNodeType.TOOL

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = partial(stitch_images_with_grid, **self.opt_kwargs)

    def __call__(self, x: list = None) -> dict:
        if isinstance(x, dict):
            x = [x]
        return self.pipeline(x)


class ImageMotionNode(WorkflowNode):
    """
    Image Motion Node
    """

    node_type = WorkflowNodeType.TOOL

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = partial(
            create_video_or_gif_from_image,
            **self.opt_kwargs,
        )

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class VideoCompositionNode(WorkflowNode):
    """
    Video Composition Node
    """

    node_type = WorkflowNodeType.TOOL

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = partial(merge_videos, **self.opt_kwargs)

    def __call__(self, x: dict = None) -> dict:
        return self.pipeline(x)


class CodeNode(WorkflowNode):
    """
    Python Code Node
    """

    node_type = WorkflowNodeType.TOOL

    def _post_init(self) -> None:
        super()._post_init()
        self.pipeline = execute_python_code
        self.code_tags = "{{code}}"
        self.input_tags = "{{inputs}}"
        self.output_tags = "<<RESULT>>"

    def template(self) -> str:
        """
        Code template
        """
        template = dedent(
            f"""
            {self.code_tags}
            import json

            if isinstance({self.input_tags}, str):
                inputs_obj = json.loads({self.input_tags})
            else:
                inputs_obj = {self.input_tags}

            output_obj = main(*inputs_obj)

            output_json = json.dumps(output_obj, indent=4)
            result = f'''{self.output_tags}{{output_json}}{self.output_tags}'''
            print(result)
            """,
        )
        return template

    def extract_result(self, content: str) -> Any:
        """
        Extract result from content
        """
        result = re.search(
            rf"{self.output_tags}(.*){self.output_tags}",
            content,
            re.DOTALL,
        )
        if not result:
            raise ValueError("Failed to parse result")
        result = result.group(1)
        return result

    def __call__(self, x: list = None) -> dict:
        if isinstance(x, dict):
            x = [x]

        code = self.template().replace(
            self.code_tags,
            self.opt_kwargs.get("code", ""),
        )
        inputs = json.dumps(x, ensure_ascii=True).replace("null", "None")
        code = code.replace(self.input_tags, inputs)
        try:
            out = self.pipeline(code)
            if out.status == ServiceExecStatus.SUCCESS:
                content = self.extract_result(out.content)
                return json.loads(content)
            return out
        except Exception as e:
            raise RuntimeError(
                f"Code id: {self.node_id},error executing :{e}",
            ) from e


class IfElseNode(WorkflowNode):
    """
    Python Code Node
    """

    node_type = WorkflowNodeType.IFELSE

    def _post_init(self) -> None:
        super()._post_init()
        self.condition_op = self.opt_kwargs.pop("condition_op", "")
        self.target_value = self.opt_kwargs.pop("target_value", "")
        self.pipeline = partial(
            eval_condition_operator,
            operator=self.condition_op,
            target_value=self.target_value,
        )

    def __call__(self, x: dict = None) -> dict:
        x["branch"] = self.pipeline(x)
        return x


NODE_NAME_MAPPING = {
    "start": StartNode,
    "dashscope_chat": ModelNode,
    "openai_chat": ModelNode,
    "post_api_chat": ModelNode,
    "post_api_dall_e": ModelNode,
    "dashscope_image_synthesis": ModelNode,
    "Message": MsgNode,
    "DialogAgent": DialogAgentNode,
    "UserAgent": UserAgentNode,
    "TextToImageAgent": TextToImageAgentNode,
    "DictDialogAgent": DictDialogAgentNode,
    "ReActAgent": ReActAgentNode,
    "Placeholder": PlaceHolderNode,
    "MsgHub": MsgHubNode,
    "SequentialPipeline": SequentialPipelineNode,
    "ForLoopPipeline": ForLoopPipelineNode,
    "WhileLoopPipeline": WhileLoopPipelineNode,
    "IfElsePipeline": IfElsePipelineNode,
    "SwitchPipeline": SwitchPipelineNode,
    "CopyNode": CopyNode,
    "BingSearchService": BingSearchServiceNode,
    "GoogleSearchService": GoogleSearchServiceNode,
    "PythonService": PythonServiceNode,
    "ReadTextService": ReadTextServiceNode,
    "WriteTextService": WriteTextServiceNode,
    "Post": PostNode,
    "TextToAudioService": TextToAudioServiceNode,
    "TextToImageService": TextToImageServiceNode,
    "ImageComposition": ImageCompositionNode,
    "IF/ELSE": IfElseNode,
    "Code": CodeNode,
    "ImageMotion": ImageMotionNode,
    "VideoComposition": VideoCompositionNode,
}


def get_all_agents(
    node: WorkflowNode,
    seen_agents: Optional[set] = None,
    return_var: bool = False,
) -> List:
    """
    Retrieve all unique agent objects from a pipeline.

    Recursively traverses the pipeline to collect all distinct agent-based
    participants. Prevents duplication by tracking already seen agents.

    Args:
        node (WorkflowNode): The WorkflowNode from which to extract agents.
        seen_agents (set, optional): A set of agents that have already been
            seen to avoid duplication. Defaults to None.

    Returns:
        list: A list of unique agent objects found in the pipeline.
    """
    if seen_agents is None:
        seen_agents = set()

    all_agents = []

    for participant in node.pipeline.participants:
        if participant.node_type == WorkflowNodeType.COPY:
            participant = participant.pipeline

        if participant.node_type == WorkflowNodeType.AGENT:
            if participant.pipeline not in seen_agents:
                if return_var:
                    all_agents.append(participant.var_name)
                else:
                    all_agents.append(participant.pipeline)
                seen_agents.add(participant.pipeline)
        elif participant.node_type == WorkflowNodeType.PIPELINE:
            nested_agents = get_all_agents(
                participant,
                seen_agents,
                return_var=return_var,
            )
            all_agents.extend(nested_agents)
        else:
            raise TypeError(type(participant))

    return all_agents
