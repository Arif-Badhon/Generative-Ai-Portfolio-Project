import requests
import json
from typing import Dict

class OllamaLLM:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.model = model
        
    def generate(self, question: str, context: str) -> str:
        """Generate answer using RAG context"""
        prompt = f"""You are a helpful AI assistant. Use the following context to answer the question accurately and concisely.

Context:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the provided context
- If the answer is not in the context, say "I don't have enough information to answer that"
- Keep your answer clear and concise (max 3-5 sentences)
- Cite specific parts of the context when relevant

Answer:"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Error generating response")
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
