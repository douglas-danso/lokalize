"""
Main RAG orchestrator for fashion cultural localization
Combines web scraping with AWS Bedrock Knowledge Base
"""
import logging
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .web_scraper import FashionCulturalScraper, get_saudi_fashion_cultural_data
from .query_engine import BedrockKnowledgeBase

logger = logging.getLogger(__name__)

@dataclass
class LocalizationRequest:
    """Request for fashion localization advice"""
    query: str
    target_region: str = "Saudi Arabia"
    brand_context: Optional[str] = None
    product_type: Optional[str] = None
    campaign_type: Optional[str] = None

@dataclass
class LocalizationResponse:
    """Response with localization advice"""
    query: str
    target_region: str
    advice: str
    cultural_insights: List[str]
    recommendations: List[str]
    sources_used: int
    confidence_score: float

class FashionLocalizationRAG:
    """
    Main RAG system for fashion cultural localization
    """
    
    def __init__(self, 
                 knowledge_base_id: Optional[str] = None,
                 aws_region: str = "us-east-1",
                 model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Fashion Localization RAG system
        
        Args:
            knowledge_base_id: AWS Bedrock Knowledge Base ID
            aws_region: AWS region for Bedrock
            model_id: Foundation model ID
        """
        self.knowledge_base_id = knowledge_base_id
        self.aws_region = aws_region
        self.model_id = model_id
        
        # Initialize components
        self.scraper = FashionCulturalScraper(chunk_size=800, chunk_overlap=100)
        
        if knowledge_base_id:
            self.query_engine = BedrockKnowledgeBase(
                region_name=aws_region,
                knowledge_base_id=knowledge_base_id,
                model_id=model_id
            )
        else:
            self.query_engine = None
            logger.warning("No Knowledge Base ID provided. Some features will be limited.")
    
    def update_knowledge_base(self, urls: List[str]) -> Dict[str, Any]:
        """
        Scrape new URLs and update the knowledge base
        
        Args:
            urls: List of URLs to scrape and add to knowledge base
            
        Returns:
            Dictionary with update results
        """
        try:
            # Scrape and chunk documents
            documents = self.scraper.scrape_and_chunk(urls)
            
            if not documents:
                return {"status": "failed", "message": "No documents scraped"}
            
            logger.info(f"Scraped {len(documents)} document chunks from {len(urls)} URLs")
            
            # Note: In a real implementation, you'd sync these to Bedrock Knowledge Base
            # For hackathon, we'll return the documents for manual upload
            return {
                "status": "success",
                "documents_scraped": len(documents),
                "urls_processed": len(urls),
                "documents": documents,
                "message": "Documents ready for Knowledge Base upload"
            }
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_localization_advice(self, request: LocalizationRequest) -> LocalizationResponse:
        """
        Get culturally aware fashion localization advice
        
        Args:
            request: Localization request with query and context
            
        Returns:
            Structured localization response
        """
        if not self.query_engine:
            return LocalizationResponse(
                query=request.query,
                target_region=request.target_region,
                advice="Knowledge Base not configured. Please provide Knowledge Base ID.",
                cultural_insights=[],
                recommendations=[],
                sources_used=0,
                confidence_score=0.0
            )
        
        try:
            # Enhance query with context
            enhanced_query = self._enhance_query(request)
            
            # Query knowledge base and generate response
            result = self.query_engine.query_and_generate(
                enhanced_query, 
                request.target_region
            )
            
            # Parse and structure the response
            return self._parse_response(request, result)
            
        except Exception as e:
            logger.error(f"Error getting localization advice: {e}")
            return LocalizationResponse(
                query=request.query,
                target_region=request.target_region,
                advice=f"Error generating advice: {str(e)}",
                cultural_insights=[],
                recommendations=[],
                sources_used=0,
                confidence_score=0.0
            )
    
    def _enhance_query(self, request: LocalizationRequest) -> str:
        """Enhance query with additional context"""
        enhanced_parts = [request.query]
        
        if request.brand_context:
            enhanced_parts.append(f"Brand context: {request.brand_context}")
        
        if request.product_type:
            enhanced_parts.append(f"Product type: {request.product_type}")
        
        if request.campaign_type:
            enhanced_parts.append(f"Campaign type: {request.campaign_type}")
        
        enhanced_parts.append(f"Target region: {request.target_region}")
        
        return " | ".join(enhanced_parts)
    
    def _parse_response(self, request: LocalizationRequest, result: Dict[str, Any]) -> LocalizationResponse:
        """Parse and structure the generated response"""
        advice = result.get('generated_response', '')
        
        # Extract insights and recommendations (simple parsing for hackathon)
        cultural_insights = []
        recommendations = []
        
        if "cultural" in advice.lower():
            cultural_insights.append("Cultural considerations identified in response")
        
        if "recommend" in advice.lower():
            recommendations.append("Specific recommendations provided")
        
        return LocalizationResponse(
            query=request.query,
            target_region=request.target_region,
            advice=advice,
            cultural_insights=cultural_insights,
            recommendations=recommendations,
            sources_used=result.get('num_docs_used', 0),
            confidence_score=0.8  # Placeholder for hackathon
        )

# Convenience functions for quick testing
def quick_localization_advice(query: str, 
                            knowledge_base_id: str,
                            target_region: str = "Saudi Arabia") -> str:
    """
    Quick function to get localization advice
    
    Args:
        query: Fashion localization query
        knowledge_base_id: AWS Bedrock Knowledge Base ID
        target_region: Target cultural region
        
    Returns:
        Localization advice
    """
    rag = FashionLocalizationRAG(knowledge_base_id=knowledge_base_id)
    request = LocalizationRequest(query=query, target_region=target_region)
    response = rag.get_localization_advice(request)
    return response.advice

def setup_demo_knowledge_base() -> List[Dict]:
    """
    Setup demo knowledge base with Saudi fashion cultural data
    
    Returns:
        List of scraped documents ready for upload to Bedrock
    """
    rag = FashionLocalizationRAG()
    from .web_scraper import SAUDI_FASHION_URLS
    
    result = rag.update_knowledge_base(SAUDI_FASHION_URLS)
    return result.get('documents', [])

if __name__ == "__main__":
    # Demo setup
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Fashion Localization RAG Demo")
    print("1. Setting up demo knowledge base...")
    
    docs = setup_demo_knowledge_base()
    print(f"✅ Scraped {len(docs)} document chunks")
    
    if docs:
        print(f"📄 Sample content preview:")
        print(f"{docs[0].page_content[:200]}...")
    
    print("\n2. Example localization query:")
    sample_query = "How should luxury fashion brands adapt their marketing for Saudi Arabian consumers?"
    print(f"Query: {sample_query}")
    print("Note: Requires AWS Bedrock Knowledge Base setup to generate full response")
