from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an AI news analyst. You will receive a list of tweets numbered from 1 to N.
Your job is to summarize each tweet into one concise sentence in the SAME ORDER as the input.
Output format (strictly follow this):
1. [summary of tweet 1]
2. [summary of tweet 2]
...and so on.
Do NOT merge, skip, or reorder any tweet. One summary per tweet, same numbering."""

def summarize(tweets: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    """
    tweets: list of (keyword, content, url)
    returns: list of (summary, url) in same order
    """
    if not tweets:
        return []

    numbered = "\n".join(
        f"{i+1}. [{kw}] {content}" for i, (kw, content, url) in enumerate(tweets)
    )
    prompt = f"{SYSTEM_PROMPT}\n\nTweets:\n{numbered}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    lines = [l.strip() for l in response.text.strip().split("\n") if l.strip()]

    summaries = []
    for i, (_, _, url) in enumerate(tweets):
        summary = lines[i] if i < len(lines) else f"{i+1}. (no summary)"
        summaries.append((summary, url))
    return summaries
