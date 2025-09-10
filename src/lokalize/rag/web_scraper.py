"""
Web scraper for fashion cultural content using LangChain WebBaseLoader
"""
import logging
from typing import List, Optional
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)

class FashionCulturalScraper:
    """Scraper for fashion and cultural content from web sources"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def scrape_urls(self, urls: List[str]) -> List[Document]:
        """
        Scrape content from list of URLs
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of Document objects with scraped content
        """
        try:
            loader = WebBaseLoader(urls)
            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} documents from {len(urls)} URLs")
            return documents
        except Exception as e:
            logger.error(f"Error scraping URLs: {e}")
            return []
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better RAG performance
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        try:
            chunked_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunked_docs)} chunks")
            return chunked_docs
        except Exception as e:
            logger.error(f"Error chunking documents: {e}")
            return documents
    
    def scrape_and_chunk(self, urls: List[str]) -> List[Document]:
        """
        Complete pipeline: scrape URLs and chunk the content
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of chunked documents ready for embedding
        """
        documents = self.scrape_urls(urls)
        if not documents:
            return []
        
        return self.chunk_documents(documents)

# Predefined URLs for Saudi Arabian fashion and cultural content
SAUDI_FASHION_URLS = [
    "https://www.arabia-interculture.com/en/social-etiquette-and-cultural-norms-in-saudi-arabia/",
    "https://thinknest.biz/future/saudi-fashion-modesty-tradition/",
    "https://www.arabianbusiness.com/lifestyle/fashion/saudi-arabia-fashion-industry-growth",
    "https://www.vogue.com/article/saudi-arabia-fashion-week-riyadh",
    "https://www.harpersbazaar.com/culture/features/a41968619/saudi-arabia-fashion-scene/",
    "https://www.businessoffashion.com/articles/markets/saudi-arabia-fashion-market-opportunity/",
    "https://fashionunited.com/news/fashion/saudi-arabia-s-fashion-industry-is-booming/",
    "https://www.middleeasteye.net/discover/saudi-arabia-fashion-industry-women-designers-growth"
]

def get_saudi_fashion_cultural_data() -> List[Document]:
    """
    Quick function to get Saudi fashion cultural data for hackathon demo
    
    Returns:
        List of chunked documents with Saudi fashion cultural content
    """
    scraper = FashionCulturalScraper(chunk_size=800, chunk_overlap=100)
    return scraper.scrape_and_chunk(SAUDI_FASHION_URLS)

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    docs = get_saudi_fashion_cultural_data()
    print(f"Scraped and chunked {len(docs)} documents")
    if docs:
        print(f"Sample content: {docs[0].page_content[:300]}...")
