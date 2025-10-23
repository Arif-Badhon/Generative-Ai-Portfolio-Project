from langchain_ollama import ChatOllama
try:
    from langchain.prompts import PromptTemplate
except ImportError:
    from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

class OllamaLLM:
    def __init__(self, base_url: str, model: str):
        self.llm = ChatOllama(
            base_url=base_url,
            model=model,
            temperature=0.2,  # Lower for more factual responses
        )
        
        # RAG-specific prompt template
        self.prompt_template = PromptTemplate(
            template="""You are a helpful AI assistant. Use the following context to answer the question accurately and concisely.

Context:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the provided context
- If the answer is not in the context, say "I don't have enough information to answer that"
- Keep your answer clear and concise (max 3-5 sentences)
- Cite specific parts of the context when relevant

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def generate(self, question: str, context: str) -> str:
        """Generate answer using RAG context"""
        return self.chain.invoke({
            "question": question,
            "context": context
        })

async def generate_stream(self, question: str, context: str):
    """Stream LLM responses"""
    async for chunk in self.chain.astream({
        "question": question,
        "context": context
    }):
        yield chunk

from langchain.memory import ConversationBufferMemory

class ConversationalRAG:
    def __init__(self, rag_chain):
        self.rag_chain = rag_chain
        self.memory = ConversationBufferMemory()
