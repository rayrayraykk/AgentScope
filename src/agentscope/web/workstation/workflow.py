# -*- coding: utf-8 -*-
""" Workflow"""
import argparse
import json
from typing import Any

from loguru import logger
from agentscope.web.workstation.workflow_dag import build_dag


def load_config(config_path: str) -> dict:
    """Load a JSON configuration file.

    Args:
        config_path: A string path to the JSON configuration file.

    Returns:
        A dictionary containing the loaded configuration.
    """
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config


def start_workflow(config: dict, **kwargs: Any) -> None:
    """Start the application workflow based on the given configuration.

    Args:
        config: A dictionary containing the application configuration.
        kwargs: Extra params.

    This function will initialize and launch the application.
    """
    logger.info("Launching...")

    dag = build_dag(config)
    dag.run(**kwargs)

    logger.info("Finished.")


def main() -> None:
    """Parse command-line arguments and launch the application workflow.

    This function sets up command-line argument parsing and checks if a
    configuration file path is provided. If the configuration file is
    found, it proceeds to load it and start the workflow.

    If no configuration file is provided, a FileNotFoundError is raised.
    """
    parser = argparse.ArgumentParser(description="AgentScope Launcher")
    parser.add_argument(
        "cfg",
        type=str,
        help="Path to the config file.",
        nargs="?",
    )

    parser.add_argument(
        "--run_id",
        type=str,
        help="run id",
        default=False,
        nargs="?",
        const="",
    )
    args = parser.parse_args()
    cfg_path = args.cfg
    run_id = args.run_id

    args = parser.parse_args()
    cfg_path = args.cfg

    if cfg_path:
        config = load_config(cfg_path)
        start_workflow(config, runtime_id=run_id)

    else:
        raise FileNotFoundError("Please provide config file.")


if __name__ == "__main__":
    main()
