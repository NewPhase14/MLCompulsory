from dataclasses import dataclass
from typing import List, Optional
import requests
from research_agent.config import SEMANTIC_CONFIG

@dataclass
class Paper:
    title: str
    authors: List[str]
    year: int
    tldr: str | None
    citation_count: int
    url: str

def find_paper_tool(query: str, year: str, minimum_citations: int) -> List[Paper]:
    rsp = requests.get(
        'https://api.semanticscholar.org/graph/v1/paper/search',
        headers={'X-API-KEY': SEMANTIC_CONFIG['api_key']},
        params={
            'query': query,
            'year': year,
            'minCitationCount': int(minimum_citations),
            'fields': 'title,authors,year,url,citationCount,tldr'
        }
    )

    if rsp.status_code != 200:
        raise RuntimeError(f"Semantic Scholar API error {rsp.status_code}: {rsp.text}")

    results = rsp.json()
    total = results.get('total', 0)
    if not total:
        return []

    papers_raw = results.get('data', [])
    papers: List[Paper] = []
    for paper in papers_raw:
        authors = [a.get('name', '') for a in paper.get('authors', [])]
        tldr_obj = paper.get('tldr')
        tldr_text = None
        if isinstance(tldr_obj, dict):
            tldr_text = tldr_obj.get('text')
        elif isinstance(tldr_obj, str):
            tldr_text = tldr_obj
        papers.append(
            Paper(
                title=paper.get('title'),
                authors=authors,
                year=paper.get('year'),
                tldr=tldr_text,
                citation_count=paper.get('citationCount'),
                url=paper.get('url')
            )
        )

    return papers