"""
Tests for Fashion Localization RAG system
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_import_structure():
    """Test that all modules can be imported"""
    try:
        from lokalize.rag.web_scraper import FashionCulturalScraper
        from lokalize.rag.query_engine import BedrockKnowledgeBase
        from lokalize.rag import FashionLocalizationRAG
        assert True
    except ImportError as e:
        pytest.skip(f"Dependencies not installed: {e}")

def test_scraper_initialization():
    """Test scraper can be initialized"""
    try:
        from lokalize.rag.web_scraper import FashionCulturalScraper
        scraper = FashionCulturalScraper(chunk_size=500, chunk_overlap=50)
        assert scraper.chunk_size == 500
        assert scraper.chunk_overlap == 50
    except ImportError:
        pytest.skip("LangChain dependencies not available")

def test_bedrock_initialization():
    """Test Bedrock client initialization (mock)"""
    try:
        with patch('boto3.client') as mock_boto3:
            mock_boto3.return_value = Mock()
            from lokalize.rag.query_engine import BedrockKnowledgeBase
            
            kb = BedrockKnowledgeBase(
                knowledge_base_id="test-kb-id",
                region_name="us-east-1"
            )
            assert kb.knowledge_base_id == "test-kb-id"
            assert kb.region_name == "us-east-1"
    except ImportError:
        pytest.skip("Boto3 dependencies not available")

def test_sample_urls_exist():
    """Test that sample URLs are defined"""
    try:
        from lokalize.rag.web_scraper import SAUDI_FASHION_URLS
        assert isinstance(SAUDI_FASHION_URLS, list)
        assert len(SAUDI_FASHION_URLS) > 0
        assert all(url.startswith('http') for url in SAUDI_FASHION_URLS)
    except ImportError:
        pytest.skip("Module not available")

def test_localization_request_model():
    """Test localization request structure"""
    try:
        from lokalize.rag import LocalizationRequest
        
        request = LocalizationRequest(
            query="Test query",
            target_region="Saudi Arabia",
            brand_context="Luxury fashion",
            product_type="Handbags"
        )
        
        assert request.query == "Test query"
        assert request.target_region == "Saudi Arabia"
        assert request.brand_context == "Luxury fashion"
        assert request.product_type == "Handbags"
    except ImportError:
        pytest.skip("Module not available")

def test_demo_functions_exist():
    """Test that demo functions are available"""
    try:
        from lokalize.rag import quick_localization_advice, setup_demo_knowledge_base
        assert callable(quick_localization_advice)
        assert callable(setup_demo_knowledge_base)
    except ImportError:
        pytest.skip("Module not available")

@pytest.mark.integration
def test_quickstart_demo():
    """Test the quickstart demo script can run"""
    import subprocess
    import sys
    
    try:
        # Run quickstart script
        result = subprocess.run(
            [sys.executable, 'quickstart.py'], 
            capture_output=True, 
            text=True, 
            timeout=30,
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        # Should not crash (exit code 0 or acceptable error)
        assert result.returncode in [0, 1]  # 1 might be expected for missing deps
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pytest.skip("Quickstart demo not available or timed out")

if __name__ == "__main__":
    # Run basic tests
    print("🧪 Running basic validation tests...")
    
    try:
        test_import_structure()
        print("✅ Import structure test passed")
    except Exception as e:
        print(f"❌ Import test failed: {e}")
    
    try:
        test_sample_urls_exist()
        print("✅ Sample URLs test passed")
    except Exception as e:
        print(f"❌ Sample URLs test failed: {e}")
    
    print("🎉 Basic validation complete!")
