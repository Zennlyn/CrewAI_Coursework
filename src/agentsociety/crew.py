from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai_tools import JSONSearchTool
from pydantic import BaseModel
from crewai.rag.embeddings.providers.cohere.types import CohereProviderSpec
from typing import List
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

from dotenv import load_dotenv
load_dotenv()

embedding_model: CohereProviderSpec = {
    "provider": "cohere",
    "config": {
        "api_key": "FFeP6vnkyMqoezDi9aMfZST7AOxLL3E5jvVBb6WC",
        "model_name": "embed-english-v3.0"
    }
}

pdf_source = PDFKnowledgeSource(file_paths=["Yelp Data Translation.pdf"])

user_source = JSONKnowledgeSource(
    file_paths=["JSON Files/user_subset.json"],
    chunk_size=30
)

review_source = JSONKnowledgeSource(
    file_paths=["JSON Files/review_subset.json"],
    chunk_size=80
)

analyst_source = JSONKnowledgeSource(
    file_paths=["JSON Files/item_subset.json"],
    chunk_size=100
)

class Output(BaseModel):
    stars: int | float
    text: str

@CrewBase
class Agentsociety():
    """Agentsociety crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def user_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['user_profiler'], 
            verbose=True,
            knowledge_sources=[user_source, review_source],
            embedder=embedding_model
        )
    
    @agent
    def item_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['item_analyst'], 
            verbose=True,
            knowledge_sources=[analyst_source],
            embedder=embedding_model
        )
    
    @agent
    def prediction_modeler(self) -> Agent:
        return Agent(
            config=self.agents_config['prediction_modeler'], 
            verbose=True,
        )

    @task
    def analyze_user_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_user_task'],
        )

    @task
    def analyze_item_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_item_task']
        )

    @task
    def prediction_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['predict_review_task'],
            output_json=Output,
            output_file="./output.json"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agentsociety crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[pdf_source],
            embedder=embedding_model
        )