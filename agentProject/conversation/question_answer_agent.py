import os
from phi.agent import Agent
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.model.groq import Groq

# === Set Groq API Key ===
os.environ["GROQ_API_KEY"] = os.environ.get("groqApiKey")

# === Load PDF Knowledge Base ===
class questionAnswer():
    @staticmethod
    def load_knowledge_base(document_url):
        try:
            knowledge_base = PDFUrlKnowledgeBase(
                urls=[
                    document_url
                ],
            )
            knowledge_base.load(recreate=False)
            return knowledge_base
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            exit(1)

    # === Initialize Agent with Groq Free Model ===
    @staticmethod
    def initialize_agent(knowledge_base):
        try:
            agent = Agent(
                description="""You are an AI assistant that answers questions using the content from a
                 specific PDF document provided to you. Only respond with information that is directly available in the PDF. 
                 If the answer cannot be found in the document, respond with: 'I'm sorry, but I couldn't find the answer to your question in the provided PDF document.""",
                name="PDF Knowledge Agent",
                role="Answer questions based on the content of the PDF.",
                instructions=[
                    "Only answer using content from the PDF.",
                    "If the answer isn't in the PDF, respond with: 'I'm sorry, but I couldn't find the answer to your question in the provided PDF document.'"
                ],
                model=Groq(id="llama3-70b-8192"),  # Correct model ID for Groq
                # knowledge_base=knowledge_base,  # Attach the knowledge base here
                markdown=True,
                # debug_mode=True,
                fallback_messages=["I'm sorry, but I couldn't find the answer to your question in the provided PDF document."],
            )

            return agent
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            exit(1)

    # === Ask Question ===
    @staticmethod
    def ask_question(agent, question):
        try:
            response = agent.run(question)
            answer = response.content.strip()
            if "I'm sorry, but I couldn't find the answer to your question in the provided PDF document." in answer or not answer:
                return "I'm sorry, but I couldn't find the answer to your question in the provided PDF document. the answer based on the PDF."
            else:
                return answer
        except Exception as e:
            return "Error processing the question."

