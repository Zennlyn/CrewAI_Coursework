#!/usr/bin/env python
import sys
import warnings

import json

from datetime import datetime

from agentsociety.crew import Agentsociety

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def load_first_test_case(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data or len(data) == 0:
        raise ValueError("Test dataset is empty")

    first_row = data[0]

    # Adjust keys depending on your dataset structure
    user_id = first_row.get("user_id")
    item_id = first_row.get("item_id")

    if user_id is None or item_id is None:
        raise ValueError("Missing user_id or item_id in dataset")

    return user_id, item_id

def run():
    """
    Run the crew.
    """
    # user_id, item_id = load_first_test_case("/home/zen/Documents/llm_course/agentsociety/knowledge/JSON Files/test_review_subset.json")
    user_id, item_id = "LQUk3WFBgEfwIYkNDh5l1Q", "KueYmi7Vrr0Hyt0_iIux4Q"
    print(f"user_id: {user_id}, item_id: {item_id}")
    inputs = {
        'user_id': user_id,
        'item_id': item_id
    }

    try:
        Agentsociety().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    user_id, item_id = load_first_test_case("../../knowledge/JSON Files/test_review_subset.json")
    inputs = {
        'user_id': user_id,
        'item_id': item_id
    }
    try:
        Agentsociety().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Agentsociety().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    user_id, item_id = load_first_test_case("../../knowledge/JSON Files/test_review_subset.json")
    inputs = {
        'user_id': user_id,
        'item_id': item_id
    }

    try:
        Agentsociety().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = Agentsociety().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
