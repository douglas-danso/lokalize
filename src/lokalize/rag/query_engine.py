"""
AWS Bedrock Knowledge Base integration for fashion cultural RAG
"""
import json
import logging
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)

class BedrockKnowledgeBase:
    """
    AWS Bedrock Knowledge Base client for fashion cultural localization
    """
    
    def __init__(self, 
                 region_name: str = "us-east-1",
                 knowledge_base_id: Optional[str] = None,
                 model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize Bedrock Knowledge Base client
        
        Args:
            region_name: AWS region
            knowledge_base_id: Bedrock Knowledge Base ID (if existing)
            model_id: Foundation model ID for generation
        """
        self.region_name = region_name
        self.knowledge_base_id = knowledge_base_id
        self.model_id = model_id
        
        try:
            self.bedrock_agent = boto3.client('bedrock-agent-runtime', region_name=region_name)
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region_name)
            logger.info(f"Initialized Bedrock clients for region: {region_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock clients: {e}")
            raise
    
    def query_knowledge_base(self, 
                           query: str, 
                           max_results: int = 5,
                           confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Query the knowledge base for relevant fashion cultural information
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            confidence_threshold: Minimum confidence score for results
            
        Returns:
            Dictionary containing query results and metadata
        """
        if not self.knowledge_base_id:
            raise ValueError("Knowledge Base ID not provided")
        
        try:
            response = self.bedrock_agent.retrieve(
                knowledgeBaseId=self.knowledge_base_id,
                retrievalQuery={
                    'text': query
                },
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': max_results,
                        'overrideSearchType': 'HYBRID'
                    }
                }
            )
            
            # Filter results by confidence threshold
            filtered_results = []
            for result in response.get('retrievalResults', []):
                score = result.get('score', 0)
                if score >= confidence_threshold:
                    filtered_results.append(result)
            
            logger.info(f"Retrieved {len(filtered_results)} results for query: {query[:50]}...")
            
            return {
                'query': query,
                'results': filtered_results,
                'total_results': len(filtered_results),
                'raw_response': response
            }
            
        except ClientError as e:
            logger.error(f"AWS ClientError querying knowledge base: {e}")
            raise
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            raise
    
    def generate_culturally_aware_response(self, 
                                         query: str, 
                                         context_docs: List[Dict],
                                         target_region: str = "Saudi Arabia") -> str:
        """
        Generate culturally aware fashion advice using retrieved context
        
        Args:
            query: User's fashion localization query
            context_docs: Retrieved documents from knowledge base
            target_region: Target cultural region
            
        Returns:
            Generated culturally aware response
        """
        # Prepare context from retrieved documents
        context_text = "\n\n".join([
            f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\n"
            f"Content: {doc.get('content', {}).get('text', '')}"
            for doc in context_docs
        ])
        
        # Create prompt for cultural fashion localization
        prompt = f"""
You are an expert in fashion marketing localization with deep knowledge of {target_region}'s cultural norms, values, and preferences.

Context Information:
{context_text}

User Query: {query}

Based on the provided context about {target_region}'s culture and fashion norms, provide specific, actionable advice for localizing fashion marketing. Consider:

1. Cultural sensitivities and values
2. Appropriate imagery and messaging
3. Color symbolism and preferences
4. Religious and social considerations
5. Local fashion trends and preferences
6. Marketing channels and approaches

Provide a comprehensive response that goes beyond translation to true cultural localization.

Response:"""

        try:
            # Call Bedrock for generation
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId=self.model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            generated_text = response_body.get('content', [{}])[0].get('text', '')
            
            logger.info(f"Generated response for query: {query[:50]}...")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def query_and_generate(self, 
                          query: str, 
                          target_region: str = "Saudi Arabia",
                          max_results: int = 5) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve relevant docs and generate response
        
        Args:
            query: User's fashion localization query
            target_region: Target cultural region
            max_results: Maximum number of documents to retrieve
            
        Returns:
            Dictionary with generated response and metadata
        """
        try:
            # Step 1: Retrieve relevant documents
            retrieval_results = self.query_knowledge_base(query, max_results)
            
            # Step 2: Generate culturally aware response
            response = self.generate_culturally_aware_response(
                query, 
                retrieval_results['results'], 
                target_region
            )
            
            return {
                'query': query,
                'target_region': target_region,
                'generated_response': response,
                'retrieved_docs': retrieval_results['results'],
                'num_docs_used': len(retrieval_results['results'])
            }
            
        except Exception as e:
            logger.error(f"Error in query_and_generate pipeline: {e}")
            raise

# Utility function for quick testing
def quick_fashion_query(query: str, 
                       knowledge_base_id: str,
                       region: str = "Saudi Arabia") -> str:
    """
    Quick function to query fashion cultural knowledge base
    
    Args:
        query: Fashion localization query
        knowledge_base_id: AWS Bedrock Knowledge Base ID
        region: Target cultural region
        
    Returns:
        Generated culturally aware response
    """
    kb = BedrockKnowledgeBase(knowledge_base_id=knowledge_base_id)
    result = kb.query_and_generate(query, region)
    return result['generated_response']

if __name__ == "__main__":
    # Example usage (requires actual Knowledge Base ID)
    logging.basicConfig(level=logging.INFO)
    
    # Example query
    sample_query = "How should I adapt a luxury handbag advertisement for Saudi Arabian market?"
    
    print(f"Sample query: {sample_query}")
    print("Note: Requires AWS credentials and Knowledge Base ID to run")
