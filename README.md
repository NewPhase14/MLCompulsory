## Setup instructions

1. Clone the repository:

2. Create a virtual environment:

3. Install the required dependencies:
```bash 
pip install -r requirements.txt
```

## Configuration

1. Create a config.py file in the root of the research_agent folder and add the following content:

2. Replace the placeholder values in the LLM_CONFIG and SEMANTIC_CONFIG dictionaries with your actual API keys.

   
- Semantic Scholar API Key
      Get your API key from: https://www.semanticscholar.org/product/api
- Mistral API Key
      Get your API key from: https://mistral.ai/

```python
LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": "[Insert your Mistral API key here]",
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}
SEMANTIC_CONFIG = {
            "api_key": "[Insert your Semantic Scholar API key here]",
}
```

## How to run the agent

1. Run the paper_research_agent.py script to start the agent
2. The agent will prompt you to enter a research query. Type in your query and press Enter.
3. The agent will need an [Topic], [Year] and [Citation_Count] to find relevant papers. You can provide this information in the following format:
   - Topic: [Your research topic]
   - Year: [Publication year range, e.g., Acceptable formats: "2020", "Before 2015", "After 2018" and "Between 2020 and 2022"]
   - Citation_Count: [Minimum number of citations, e.g., 100]
4. The agent will then use the find_paper_tool to search for relevant papers based on the provided information and return a list of papers that match the criteria.

## Evaluation
| Evaluation promt [Topic] [Publication_year] [Citation_count]    | Relevance | Year constraint | Citation constraint | Avoided hallucination | Useful explanation | Notes                                                                                                                                                                                          |
|-----------------------------------------------------------------|-----------|----------------|------------------|-----------------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Machine learning, 2015, 1000                                    | ✓         | ✓ | ✓                | ✓                     | ✓                  | Broad topic                                                                                                                                                                                    |
| Attention is all you need transformer architecture, 2017, 20000 | ✓         | ✓ | ✓                | ✓                     | ✓                  | Narrow topic                                                                                                                                                                                   |
| Neural networks, Before 2010, 500                               | ✓         | ✓ | ✓ | x                     | ✓                  | Before constraint (This test did hallucination by giving the wrong citation source)                                                                                                            |
| Diffusion models, After 2020, 100                               | ✓         | ✓ | ✓ | ✓                     | ✓                  | After constraint                                                                                                                                                                               |
| Butterflies, Between 2015 and 2020, 400                         | ✓         | ✓ | ✓ | ✓                     | ✓                  | Between constraint                                                                                                                                                                             |
| Atoms, After 2000, 200000                                       |           |  |  |                       |                    | No result case (Didn't find any papers, we recieved error from tool not the agent)                                                                                                             |
| AI, 2018, 100                                                   | ✓         | ✓ | ✓ | ✓                     | ✓ | Ambiguous Query (Broad topic, so the agent picked a paper about an AI framework)                                                                                                               |
| Quantum computing, -2020, 100                                   | ✓         | ✓ | ✓ | ✓                     | ✓ | Invalid year format (The agent was able to understand the year constraint which should be equal to using the before constraint)                                                                |
| Co2 emissions, 2000-2020, 100                                   | ✓         | ✓ | ✓ | ✓                     | ✓ | Invalid year format (The agent was able to understand the year constraint which should be equal to using the between constraint)                                                               |
| Wolf population europe, 2000-, 300                                   | x         | ✓ | ✓ | x                     | ✓ | Invalid year format (The agent was able to understand that the year constraint should be after 2000. But it didn't find a valid paper, agent just returned a paper about languages in europe.) |

## Group member contríbutions 
We have worked together on the project, so many of the contributions were collaborative. However, here is a breakdown of the main contributions from each group member:

- [Jeppe Hallen Baden]: Implemented the find_paper_tool which allows the agent to search for relevant papers using the Semantic Scholar API. 
- [Nikolaj Sørensen]: Implemented the paper_research_agent which is the agent that utilizes the find_paper_tool to research papers based on a given query.

