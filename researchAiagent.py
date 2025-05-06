from phi.agent import Agent
from phi.model.groq import Groq
# from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
import os
# from dotenv import load_dotenv
# load_dotenv()
os.environ['GROQ_API_KEY']="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"
# agent = Agent(
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[ Newspaper4k()],
#     description="You are a senior NYT researcher writing an article on a topic.",
#     instructions=[
#         "For a given topic, search for the top 5 links.",
#         "Then read each URL and extract the article text, if a URL isn't available, ignore it.",
#         "Analyse and prepare an NYT worthy article based on the information.",
#     ],
#     markdown=True,
#     show_tool_calls=True,
#     add_datetime_to_instructions=True,
#     # debug_mode=True,
# )
# agent.print_response("Simulation theory", stream=True)

from phi.agent import Agent
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
knowledge_base = PDFUrlKnowledgeBase(
    # Read PDF from this URL
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    # Store embeddings in the `ai.recipes` table
    vector_db=PgVector(table_name="recipes", db_url=db_url, search_type=SearchType.hybrid),
)
# Load the knowledge base: Comment after first run
knowledge_base.load(upsert=True)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    # Enable RAG by adding references from AgentKnowledge to the user prompt.
    add_context=True,
    # Set as False because Agents default to `search_knowledge=True`
    search_knowledge=False,
    markdown=True,
    # debug_mode=True,
)
agent.print_response("How do I make chicken and galangal in coconut milk soup")
#  Print the response from the agent
