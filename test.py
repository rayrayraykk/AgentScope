import agentscope
from agentscope.agents import ReActAgent, UserAgent
from agentscope.manager import ModelManager
from agentscope.pipelines import SequentialPipeline
from agentscope.service import ServiceToolkit, execute_python_code


def main():
    agentscope.init(
        logger_level="DEBUG",
    )
    ModelManager.get_instance().load_model_configs(
        [
            {
                "config_name": "qwen",
                "messages_key": "input",
                "model_name": "qwen-max",
                "model_type": "dashscope_chat",
                "seed": 0,
                "temperature": 0,
            }
        ]
    )
    flow = None

    agent_4 = UserAgent(name="User")
    service_6 = execute_python_code
    agent_5_service_toolkit = ServiceToolkit()
    agent_5_service_toolkit.add(service_6)
    agent_5 = ReActAgent(
        max_iters=10,
        model_config_name="qwen",
        name="Assistant",
        sys_prompt="You are an assistant. ",
        verbose="True",
        service_toolkit=agent_5_service_toolkit,
    )

    pipeline_3 = SequentialPipeline([agent_4, agent_5, agent_4])

    flow_1_0 = pipeline_3(flow_1)


if __name__ == "__main__":
    main()
