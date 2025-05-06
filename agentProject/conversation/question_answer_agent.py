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
            print("✅ Knowledge base loaded successfully.")
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
                 If the answer cannot be found in the document, respond with: 'I don't know the answer based on the PDF.""",
                name="PDF Knowledge Agent",
                role="Answer questions based on the content of the PDF.",
                instructions=[
                    "Only answer using content from the PDF.",
                    "If the answer isn't in the PDF, respond with: 'I don't know the answer based on the PDF.'"
                ],
                model=Groq(id="llama3-70b-8192"),  # Correct model ID for Groq
                # knowledge_base=knowledge_base,  # Attach the knowledge base here
                markdown=True,
                debug_mode=True,
                fallback_messages=["I don't know the answer based on the PDF."],
            )

            print("✅ Agent initialized successfully.")
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

            # with open(f"response-25-04-{number}.txt", "w") as file:
            #     file.write(f"Question: {question}\n")
            #     file.write(f"Answer: {answer}\n")
            #     # file.write(answer + "\n---\n")

            if "I don't know" in answer or not answer:
                print(f"🤷‍♂️ Question: {question}\n➡️ Fallback: I don't know the answer based on the PDF.\n")
                return "I don't know the answer based on the PDF."
            else:
                print(f"✅ Question: {question}\n➡️ Answer: {answer}\n")
                return answer
        except Exception as e:
            print(f"❌ Error processing question '{question}': {e}")
            return "Error processing the question."

# === MAIN ===
# if __name__ == "__main__":
#     knowledge_base = questionAnswer.load_knowledge_base()
#     agent = questionAnswer.initialize_agent(knowledge_base)

#     questions = [
#         "Give me The details of this Document.",
#         "Give me Reliance stock proce and besed on the pdf what is the best time to buy it?",
#         "Based on the pdf, what is the best time to buy a stock?",
#         "Based on the Pdf Give me summery of the document.",
#         "Give me Defanition Of the Cemicals How To make A Nacl.",
#         "Can you give me haxagonal Cube and its properties?",
#         "The normal boiling point of ethyl acetate is 77.06 0 C. A solution of 50 g of a nonvolatile solute in 150 g of ethyl acetate boils at 84.27 0 C. Evaluate the molar mass of solute if Kb for ethyl acetate is 2.77 0 C kg mol-1.",
#         "How vapour pressure lowering is related to a rise in boiling point of solution?",
#         "Give me the summery of the document.",
#     ]

#     for index, question in enumerate(questions):
#         questionAnswer.ask_question(agent, question, index)