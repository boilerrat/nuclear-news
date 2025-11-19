"""Main crew implementation for Nuclear Industry Intelligence System.

This module defines the NuclearIntelligenceCrew class that orchestrates
the multi-agent workflow for discovering, analyzing, synthesizing, and
formatting nuclear industry intelligence reports.
"""

import logging
from pathlib import Path
from typing import Optional

import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool, SerperDevTool

from nuclear_intelligence.tools.crawl4ai_tool import Crawl4AITool

logger = logging.getLogger(__name__)


@CrewBase
class NuclearIntelligenceCrew:
    """Crew for nuclear industry intelligence gathering and synthesis.

    This crew orchestrates a sequential workflow of specialized agents:
    1. Research Agent: Discovers relevant information from diverse sources
    2. Analysis Agent: Evaluates content for relevance and significance
    3. Synthesis Agent: Creates coherent narratives from analyzed content
    4. Report Formatting Agent: Formats final reports for distribution

    Attributes:
        research_agent: Agent responsible for information discovery
        analysis_agent: Agent responsible for content evaluation
        synthesis_agent: Agent responsible for narrative synthesis
        report_formatting_agent: Agent responsible for report formatting
        information_discovery_task: Task for discovering relevant information
        content_analysis_task: Task for analyzing discovered content
        content_synthesis_task: Task for synthesizing analyzed content
        report_generation_task: Task for generating formatted reports
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, output_dir: Optional[str] = None):
        """Initialize the Nuclear Intelligence Crew.

        Args:
            output_dir: Optional directory path for output files.
                       Defaults to 'outputs' in project root.
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "outputs"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize tools
        self.search_tool = SerperDevTool()
        self.crawl_tool = Crawl4AITool()
        self.file_writer = FileWriterTool()

        # Configure LLM with valid model name
        # Default to gpt-4o-mini if not specified in environment
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.llm = LLM(model=model_name)

    @agent
    def research_agent(self) -> Agent:
        """Create and configure the Research Agent.

        Returns:
            Configured Research Agent with search and scraping tools
        """
        return Agent(
            config=self.agents_config["research_agent"],
            tools=[self.search_tool, self.crawl_tool],
            verbose=True,
        )

    @agent
    def analysis_agent(self) -> Agent:
        """Create and configure the Analysis Agent.

        Returns:
            Configured Analysis Agent for content evaluation
        """
        return Agent(
            config=self.agents_config["analysis_agent"],
            verbose=True,
        )

    @agent
    def synthesis_agent(self) -> Agent:
        """Create and configure the Synthesis Agent.

        Returns:
            Configured Synthesis Agent for narrative creation
        """
        return Agent(
            config=self.agents_config["synthesis_agent"],
            verbose=True,
        )

    @agent
    def report_formatting_agent(self) -> Agent:
        """Create and configure the Report Formatting Agent.

        Returns:
            Configured Report Formatting Agent with file writing capability
        """
        return Agent(
            config=self.agents_config["report_formatting_agent"],
            tools=[self.file_writer],
            verbose=True,
        )

    @task
    def information_discovery(self) -> Task:
        """Create the information discovery task.

        Returns:
            Task for discovering relevant nuclear industry information
        """
        return Task(
            config=self.tasks_config["information_discovery"],
            agent=self.research_agent(),
        )

    @task
    def content_analysis(self) -> Task:
        """Create the content analysis task.

        Returns:
            Task for analyzing discovered content
        """
        return Task(
            config=self.tasks_config["content_analysis"],
            agent=self.analysis_agent(),
        )

    @task
    def content_synthesis(self) -> Task:
        """Create the content synthesis task.

        Returns:
            Task for synthesizing analyzed content into narratives
        """
        return Task(
            config=self.tasks_config["content_synthesis"],
            agent=self.synthesis_agent(),
        )

    @task
    def report_generation(self) -> Task:
        """Create the report generation task.

        Returns:
            Task for generating formatted reports
        """
        return Task(
            config=self.tasks_config["report_generation"],
            agent=self.report_formatting_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Create and configure the crew with sequential process.

        Returns:
            Configured Crew ready for execution
        """
        return Crew(
            agents=[
                self.research_agent(),
                self.analysis_agent(),
                self.synthesis_agent(),
                self.report_formatting_agent(),
            ],
            tasks=[
                self.information_discovery(),
                self.content_analysis(),
                self.content_synthesis(),
                self.report_generation(),
            ],
            process=Process.sequential,
            llm=self.llm,
            verbose=True,
        )

    def kickoff(
        self,
        topic: str,
        time_window: str = "past month",
        **kwargs,
    ) -> str:
        """Execute the crew workflow with specified parameters.

        Args:
            topic: The topic or area of focus for intelligence gathering
            time_window: Time window for information discovery (e.g., "past week", "past month")
            **kwargs: Additional keyword arguments passed to crew.kickoff()

        Returns:
            Final report output from the crew execution
        """
        logger.info(f"Starting intelligence gathering for topic: {topic}")
        logger.info(f"Time window: {time_window}")

        inputs = {
            "topic": topic,
            "time_window": time_window,
        }

        result = self.crew().kickoff(inputs=inputs, **kwargs)
        logger.info("Intelligence gathering completed")

        return result

