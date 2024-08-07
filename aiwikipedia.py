import wikipedia
import json

def wikipedia_search(query):
    """Perform a Wikipedia search"""
    print(f"Using Wikipedia for {query}")
    try:
        page = wikipedia.page(query)
        summary = wikipedia.summary(query, sentences=2)
        return json.dumps({"title": page.title, "summary": summary, "url": page.url})
    except:
        return json.dumps({"error": "No Wikipedia page found for the query"})

print(wikipedia_search("Gandhi Jayanti"))