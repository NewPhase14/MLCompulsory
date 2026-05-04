from autogen import UserProxyAgent, ConversableAgent
from research_agent.config import LLM_CONFIG
from research_agent.tools.find_paper_tool import find_paper_tool


def create_research_agent() -> ConversableAgent:
    agent = ConversableAgent(
        name="Research Agent",
        system_message="You are a helpful AI assistant. "
"Ensure when user types before, ALWAYS set - before the year. For example, if user types 2020, interpret it as -2020 to search for papers published before 2020. "
"Ensure when user types after, ALWAYS set - after the year. For example, if user types 2020, interpret it as 2020- to search for papers published after 2020. "
"Ensure when user types between, ALWAYS set - between the years. For example, if user types 2015 and 2020, interpret it as 2015-2020 to search for papers published between 2015 and 2020."
"Ensure when user don't type anything else than the year, NEVER set any - before or after the year. For example, if user types 2020, interpret it as 2020 to search for papers published in 2020."
"""

PROCESS:
1. Acknowledge the search request
2. Use the find_paper tool to search for papers
3. Validate results against ALL constraints
4. Return ONLY papers that satisfy ALL requirements

OUTPUT FORMAT (for each valid paper):
- **Title**: [paper title]
- **Authors**: [author list]
- **Publication Year**: [year]
- **Citation Count**: [number]
- **Citation Source**: [e.g., Google Scholar, Scopus, Web of Science]
- **Paper Link**: [URL or "Not available"]
- **Match Explanation**: [brief explanation of why this paper matches the request, why it was selected, and how it meets the constraints]

VALIDATION RULES:
- Reject papers with publication year NOT matching the requested year
- Reject papers with citation count BELOW the minimum threshold
- Only return papers that meet ALL constraints
- If no papers satisfy all constraints, clearly state this
"""

"Don't include any other text in your response. "
"Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    agent.register_for_llm(
        name="find_paper",
        description="Search for academic papers. Parameters: query (string), publication_year (int), min_citations (int). Returns: list of papers with title, authors, year, citations, and URL.",
    )(find_paper_tool)

    return agent



if __name__ == "__main__":
    # Create the research agent
    agent = create_research_agent()

    # Create a user proxy for human input
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    )

    # Register tool for execution
    user_proxy.register_for_execution(name="find_paper")(find_paper_tool)

    # Get user input
    query = input("Enter research topic: ")
    publication_year = input("Enter publication year (Use before, after or between): ")
    min_citations = int(input("Enter minimum citation count: "))

    user_proxy.initiate_chat(
        agent,
        message=f"Find the best research paper about {query} published in {publication_year} with at least {min_citations} citations. "
                f"Return only the single best paper candidate with full details."
    )
