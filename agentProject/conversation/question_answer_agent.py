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
               description="""You are an AI assistant that answers questions **strictly** using the content from a 
                        specific PDF document provided to you. Do not use external knowledge, do not infer or guess answers, and 
                        do not use the internet or any pre-existing world knowledge. If the answer cannot be found explicitly in 
                        the PDF, respond with: 'I'm sorry, but I couldn't find the answer to your question in the provided PDF document.'""",

                    name="PDF-Only QA Agent",
                    role="Answer user questions using only the content of a specific PDF file.",
    
                    instructions=[
                        "Only use the PDF content to answer questions.",
                        "Do not use external knowledge, AI inference, or assumptions.",
                        "Do not perform internet searches or use general world knowledge.",
                        "If the answer is not clearly in the PDF, respond with: 'I'm sorry, but I couldn't find the answer to your question in the provided PDF document.'",
                        "Do not hallucinate or fabricate answers.",
                        "If the question is unrelated to the PDF, use the fallback message."
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
                return "I'm sorry, but I couldn't find the answer to your question in the provided PDF document."
            else:
                return answer
        except Exception as e:
            return "Error processing the question."

