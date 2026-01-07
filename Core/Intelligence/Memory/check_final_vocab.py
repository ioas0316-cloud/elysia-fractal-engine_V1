import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector
    
    print("📊 Checking Vocabulary Size...")
    w = WebKnowledgeConnector()
    
    # Check if comm_enhancer exists and has metrics
    if hasattr(w, 'comm_enhancer'):
        m = w.comm_enhancer.get_communication_metrics()
        vocab_size = m.get('vocabulary_size', 0)
        print(f"✅ Final Vocabulary Count: {vocab_size:,} words")
        
        # Also check Internal Universe concepts if possible
        if hasattr(w, 'connector') and hasattr(w.connector, 'universe'):
            concepts = len(w.connector.universe.concepts)
            print(f"✅ Internal Universe Concepts: {concepts:,}")
            
    else:
        print("⚠️ No CommunicationEnhancer found on WebKnowledgeConnector instance.")
        print("   (Note: In-memory learning might not have persisted to disk if not saved)")

except Exception as e:
    print(f"❌ Error checking vocabulary: {e}")
