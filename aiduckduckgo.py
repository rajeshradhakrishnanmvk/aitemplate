from duckduckgo_search import DDGS

def duckduckgo_search(query):
    """Perform a DuckDuckGo search using the duckduckgo_search library"""
    print(f"Using DuckDuckGo for {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return f"No results found for '{query}'. The search may have been too specific or there might be no relevant information available."

        formatted_results = "\n".join([f"{result['title']}: {result['body']}" for result in results])
        return f"Here are some search results for '{query}':\n{formatted_results}"
    
    except Exception as e:
        return f"An error occurred while searching for '{query}': {str(e)}"

print(duckduckgo_search("What is the capital of Greenland?"))