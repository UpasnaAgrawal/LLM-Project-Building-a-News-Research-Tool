from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()

grok_api_key = os.getenv("GROK_API_KEY")
grok_api_base = os.getenv("GROK_API_BASE")
newsapi_key = os.getenv("NEWSAPI_KEY")

# ✅ Use ChatOpenAI, not OpenAI
llm = ChatOpenAI(
    api_key=grok_api_key,
    base_url=grok_api_base,
    model="llama3-70b-8192"  #
)

template = """
You are an AI assistant helping an equity research analyst. Given the following query and the provided news article summaries, provide an overall summary.
Query: {query}
Summaries: {summaries}
"""
prompt = PromptTemplate(template=template, input_variables=["query", "summaries"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# NewsAPI Setup
newsapi = NewsApiClient(api_key=newsapi_key)

def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language="en", sort_by="relevancy")
    return articles["articles"]

def summarize_articles(articles):
    summaries = [article["description"] for article in articles if article.get("description")]
    return " ".join(summaries)

def get_summary(query):
    articles = get_news_articles(query)
    return summarize_articles(articles)
