import pytest
from unittest.mock import patch
from config.secure_config import SecureConfig

class TestSecureConfig:
    """Test secure configuration management"""
    
    def test_missing_api_key(self):
        """Test behavior when no API key is available"""
        with patch.dict(os.environ, {}, clear=True):
            key = SecureConfig.get_api_key()
            assert key is None
    
    def test_environment_variable_priority(self):
        """Test that OM_API_KEY has highest priority"""
        with patch.dict(os.environ, {
            "OM_API_KEY": "priority_key",
            "OPENAI_API_KEY": "lower_priority_key"
        }, clear=True):
            key = SecureConfig.get_api_key()
            assert key == "priority_key"
    
    def test_service_specific_key(self):
        """Test service-specific API key loading"""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "openai_specific_key"
        }, clear=True):
            key = SecureConfig.get_api_key("openai")
            assert key == "openai_specific_key"
    
    def test_development_test_key_allowed(self):
        """Test that test keys are allowed in development"""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "development"
        }, clear=True):
            key = SecureConfig.get_api_key()
            assert key == "openmind_free"  # test key allowed in dev
    
    def test_production_test_key_blocked(self):
        """Test that test keys are blocked in production"""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "OM_API_KEY": "openmind_free"
        }, clear=True):
            key = SecureConfig.get_api_key()
            assert key is None  # test key blocked in prod
    
    def test_valid_production_key(self):
        """Test that valid production keys are allowed"""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "production",
            "OM_API_KEY": "real_secure_key_123456789"
        }, clear=True):
            key = SecureConfig.get_api_key()
            assert key == "real_secure_key_123456789"
    
    def test_key_validation_length(self):
        """Test API key length validation"""
        # Short key should fail
        assert not SecureConfig.validate_api_key("short", "test")
        
        # Valid key should pass
        assert SecureConfig.validate_api_key("real_secure_key_123456789", "production")
    
    def test_key_validation_test_keys(self):
        """Test that test keys fail in production"""
        test_keys = ["openmind_free", "test_key", "demo_key", "example"]
        
        for test_key in test_keys:
            assert not SecureConfig.validate_api_key(test_key, "production")