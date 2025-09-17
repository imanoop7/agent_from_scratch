"""Web browsing tool that fetches a page and returns markdown content."""

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def browse_web(params):
	"""Fetch a URL and convert the main content to markdown.

	Removes common non-content elements and returns a front-matter style
	title followed by markdown text. Prints a short preview for visibility.
	"""
	url = params.get("url")
	print("\n\n" + "#" * 40)
	print(f"Browsing web: {url}")
	resp = requests.get(url, headers={
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	}, timeout=30)
	if not resp.ok:
		print(resp)
		return "Error retrieving website."

	# Parse and clean the HTML
	soup = BeautifulSoup(resp.text, "html.parser")
	for selector in ["script", "style", "nav", "footer", "iframe", ".ads"]:
		for el in soup.select(selector):
			el.decompose()

	# Title and main content extraction
	title = (soup.title.string.strip() if soup.title else "").strip()
	if not title:
		first_h1 = soup.find("h1")
		title = first_h1.get_text(strip=True) if first_h1 else ""

	main = soup.select_one("article, main, .content, #content, .post")
	html = str(main) if main else str(soup.body or soup)
	content_md = md(html, heading_style="ATX", code_language="", code_block_style="fenced")
	result = f"---\ntitle: '{title}'\n---\n\n{content_md}"
	print(result[:500])
	return result


browse_web_tool_config = {
	"type": "function",
	"function": {
		"name": "browseWeb",
		"description": "Visit a URL and return a markdown version of the browsed page content.",
		"parameters": {
			"type": "object",
			"properties": {
				"url": {"type": "string", "description": "The url of the web page to go get and return as markdown."}
			},
			"required": ["url"],
		}
	}
}
