import requests
from research_agent.config import SEMANTIC_CONFIG

def find_paper_tool():
    result_limit = 10
    query = input("Enter your research query: ")
    year = input("Enter your research year: ")
    minimum_citations = input("Enter your minimum citations: ")


    rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/search',
                       headers={'X-API-KEY': SEMANTIC_CONFIG['api_key']},
                       params={'query': query, 'limit': result_limit, 'year': year, 'minCitationCount': int(minimum_citations), 'fields': 'title,url,citationCount'})
    if rsp.status_code == 200:
        results = rsp.json()
        total = results['total']
        if not total:
            print("No papers found for the given query.")
        else:
            print(f'Found {total} papers for {query}, showing up to {result_limit} results.')
            papers = results['data']
            print_papers(papers)
    else:
        print(rsp.status_code, rsp.text)

def print_papers(papers):
    for idx, paper in enumerate(papers):
        print(f"{idx} {paper['title']} {paper['url']} {paper['citationCount']}")

if __name__ == '__main__':
    find_paper_tool()