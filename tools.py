SEARCH_WIKIPEDIA_TOOL = {
    "name": "search_wikipedia",
    "description": (
        "Search English Wikipedia and return the top 3 matching articles. "
        "Each result includes the article title, the introduction paragraph "
        "as plain text, the article URL, and a flag indicating whether the "
        "page is a disambiguation page. Use specific search queries; you may "
        "call this tool multiple times with different queries to gather "
        "evidence or disambiguate entities."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The Wikipedia search query.",
            }
        },
        "required": ["query"],
    },
}
