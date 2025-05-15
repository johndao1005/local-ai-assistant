"""
Search API endpoint implementation.
This module handles search-related API requests.
"""
from flask import jsonify, request
from features.connectivity.search import WebSearch

# Initialize web search
web_search = WebSearch()

def search_endpoint(request):
    """
    Process search API requests.
    
    Args:
        request (Request): The Flask request object
        
    Returns:
        Response: The JSON response with search results
    """
    # Get request data
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Extract query and settings
    query = data.get('query', '')
    use_cache = data.get('use_cache', True)
    
    # Perform the search
    results = web_search.search(query, use_cache=use_cache)
    
    # Return the results
    return jsonify({'results': results})

def get_webpage_endpoint(request):
    """
    Process webpage content retrieval API requests.
    
    Args:
        request (Request): The Flask request object
        
    Returns:
        Response: The JSON response with webpage content
    """
    # Get request data
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Extract URL
    url = data.get('url', '')
    
    # Get webpage content
    content = web_search.get_webpage_content(url)
    
    # Return the content
    return jsonify({'content': content})