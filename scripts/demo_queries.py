import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000"

def query_rag(question: str, top_k: int = 5) -> Dict:
    """Query the RAG system"""
    response = requests.post(
        f"{BASE_URL}/query",
        json={"question": question, "top_k": top_k}
    )
    return response.json()

def print_result(question: str, result: Dict):
    """Pretty print query results"""
    print("\n" + "="*80)
    print(f"❓ QUESTION: {question}")
    print("="*80)
    print(f"\n💡 ANSWER:\n{result['answer']}\n")
    print(f"📚 SOURCES ({result['context_used']} chunks used):")
    for idx, source in enumerate(result['sources'], 1):
        print(f"  {idx}. {source['source']} (chunk {source['chunk_index']}, score: {source['score']:.3f})")
    print("="*80)

def main():
    """Run demo queries"""
    demo_queries = [
        "What is deep learning and how does it work?",
        "Explain the RAG process in simple terms",
        "What are the benefits of using RAG systems?",
        "What is supervised learning?",
        "How does reinforcement learning work?",
    ]
    
    print("\n🚀 RAG SYSTEM DEMO")
    print("="*80)
    
    # Check health first
    health = requests.get(f"{BASE_URL}/health").json()
    print(f"\n✅ System Status: {health['status']}")
    print(f"   Ollama: {'✓' if health['ollama_connected'] else '✗'}")
    print(f"   Qdrant: {'✓' if health['qdrant_connected'] else '✗'}")
    
    # Run queries
    for question in demo_queries:
        try:
            result = query_rag(question)
            print_result(question, result)
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n✨ Demo complete!")

if __name__ == "__main__":
    main()
