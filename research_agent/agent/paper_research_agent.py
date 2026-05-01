from autogen import ConversableAgent, UserProxyAgent
from research_agent.config import LLM_CONFIG
from research_agent.tools.find_paper_tool import find_paper_tool


def create_research_agent() -> ConversableAgent:
    agent = ConversableAgent(
        name="Research Agent",
        system_message="You are a helpful AI assistant specialized in finding academic papers. "
                       "Your task is to search for relevant academic papers based on user queries. "
                       "Use the paper_search tool to find papers. "
                       "Analyze the results and identify the BEST paper candidate based on relevance, citation count, and recency. "
                       "Return the best paper with its title, authors, year, citation count, and a brief summary. "
                       "Return 'TERMINATE' when the task is complete.",
        llm_config=LLM_CONFIG,
    )

    # Register tool for LLM to see it
    agent.register_for_llm(
        name="find_paper_tool",
        description="Search for academic papers based on a query with optional filters for year and citation count."
    )(find_paper_tool)

    # Register tool for execution
    agent.register_for_execution(name="find_paper_tool")(find_paper_tool)

    return agent


if __name__ == "__main__":
    # Create the research agent
    agent = create_research_agent()

    # Create a user proxy for human input
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        code_execution_config=False,
    )

    # Get user input
    topic = input("Enter research topic: ")
    publication_year = (input("Enter publication year: "))
    min_citations = int(input("Enter minimum citation count: "))

    # Start a chat with the agent using user-provided parameters
    user_proxy.initiate_chat(
        agent,
        message=f"Find the best research paper about {topic} published in {publication_year} with at least {min_citations} citations. "
                f"Return only the single best paper candidate with full details."
    )
