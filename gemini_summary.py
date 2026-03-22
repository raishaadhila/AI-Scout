from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an AI news analyst. You will receive a list of news articles numbered from 1 to N.
Your job is to summarize each article into one concise sentence in the SAME ORDER as the input.
Output format (strictly follow this):
1. [summary of article 1]
2. [summary of article 2]
...and so on.
Do NOT merge, skip, or reorder any article. One summary per article, same numbering."""

def summarize(articles: list[tuple[str, str, str, str]]) -> list[tuple[str, str]]:
    """
    articles: list of (keyword, title, description, url)
    returns: list of (summary, url) in same order
    """
    if not articles:
        return []

    numbered = "\n".join(
        f"{i+1}. [{kw}] {title}: {description}" for i, (kw, title, description, url) in enumerate(articles)
    )
    prompt = f"{SYSTEM_PROMPT}\n\nArticles:\n{numbered}"

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    lines = [l.strip() for l in response.text.strip().split("\n") if l.strip()]

    summaries = []
    for i, (_, _, _, url) in enumerate(articles):
        summary = lines[i] if i < len(lines) else f"{i+1}. (no summary)"
        summaries.append((summary, url))
    return summaries
