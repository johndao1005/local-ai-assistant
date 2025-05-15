"""
Web search functionality for the Local AI Assistant.
This module handles web searches and result processing.
"""
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import time
from flask import current_app

class SearchCache:
    """Cache for search results to minimize repeated web requests."""
    
    def __init__(self, cache_dir='cache', max_age=3600):
        """
        Initialize the search cache.
        
        Args:
            cache_dir (str): Directory to store cache files
            max_age (int): Maximum age of cache entries in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.max_age = max_age
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get(self, query):
        """
        Get cached search results for a query.
        
        Args:
            query (str): The search query
            
        Returns:
            dict or None: Cached results or None if not in cache or expired
        """
        # Create a filename from the query
        filename = os.path.join(self.cache_dir, 
                               f"{hash(query)}.json")
        
        # Check if cache file exists and is not expired
        if os.path.exists(filename):
            # Check file age
            file_age = time.time() - os.path.getmtime(filename)
            if file_age < self.max_age:
                try:
                    with open(filename, 'r') as f:
                        return json.load(f)
                except:
                    return None
        
        return None
    
    def save(self, query, results):
        """
        Save search results to cache.
        
        Args:
            query (str): The search query
            results (dict): The search results to cache
        """
        filename = os.path.join(self.cache_dir, 
                               f"{hash(query)}.json")
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f)
        except Exception as e:
            current_app.logger.error(f"Error saving to cache: {e}")


class WebSearch:
    """Web search implementation using requests and BeautifulSoup."""
    
    def __init__(self):
        """Initialize the web search module."""
        self.cache = SearchCache()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query, use_cache=True):
        """
        Search the web for information.
        
        Args:
            query (str): The search query
            use_cache (bool): Whether to use cached results if available
            
        Returns:
            dict: Search results with title, snippet, and URL
        """
        # Check cache first if enabled
        if use_cache:
            cached_results = self.cache.get(query)
            if cached_results:
                return cached_results
        
        # Prepare for web search
        search_results = []
        
        try:
            # Use DuckDuckGo as the search engine (more privacy-focused)
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results
                results = soup.find_all('div', class_='result')
                
                for result in results[:5]:  # Limit to top 5 results
                    title_element = result.find('a', class_='result__a')
                    snippet_element = result.find('a', class_='result__snippet')
                    
                    if title_element and snippet_element:
                        title = title_element.get_text(strip=True)
                        snippet = snippet_element.get_text(strip=True)
                        url = title_element.get('href')
                        
                        search_results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url
                        })
            
            # Cache the results
            if search_results and use_cache:
                self.cache.save(query, search_results)
            
            return search_results
            
        except Exception as e:
            current_app.logger.error(f"Search error: {e}")
            return []
    
    def get_webpage_content(self, url):
        """
        Get the main content from a webpage.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            str: Extracted main content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Get text
                text = soup.get_text()
                
                # Break into lines and remove leading/trailing space
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Remove blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                # Limit text length
                return text[:3000] + "..." if len(text) > 3000 else text
            
            return f"Error: Could not retrieve webpage (Status code: {response.status_code})"
            
        except Exception as e:
            return f"Error retrieving webpage: {e}"