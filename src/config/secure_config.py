import os
import logging
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SecureConfig:
    """
    安全配置管理类，支持从环境变量安全读取敏感信息。
    """
    
    @staticmethod
    def get_api_key(service_name: str = "openmind") -> Optional[str]:
        """
        安全获取API密钥
        
        优先级：
        1. 环境变量 OM_API_KEY
        2. 环境变量 {SERVICE_NAME}_API_KEY  
        3. 环境变量 OPENAI_API_KEY (对于OpenAI兼容服务)
        4. 配置文件中的测试密钥（仅限开发环境）
        
        Parameters
        ----------
        service_name : str
            服务名称，用于构建环境变量名
            
        Returns
        -------
        Optional[str]
            API密钥，如果未找到则返回None
        """
        # 首先检查通用OpenMind API密钥
        api_key = os.getenv("OM_API_KEY")
        if api_key:
            return api_key
            
        # 检查服务特定密钥
        service_env_key = os.getenv(f"{service_name.upper()}_API_KEY")
        if service_env_key:
            return service_env_key
            
        # 对于OpenAI兼容服务，检查OpenAI密钥
        if "openai" in service_name.lower():
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                return openai_key
        
        # 最后，仅在开发环境使用测试密钥
        is_dev = os.getenv("ENVIRONMENT", "production").lower() in ["dev", "development", "test"]
        if is_dev:
            return "openmind_free"  # 仅限开发和测试
            
        logging.error(f"API key not found for service: {service_name}")
        return None
    
    @staticmethod
    def validate_api_key(api_key: str, service_name: str) -> bool:
        """
        验证API密钥的有效性
        
        Parameters
        ----------
        api_key : str
            要验证的API密钥
        service_name : str  
            服务名称
            
        Returns
        -------
        bool
            密钥是否有效
        """
        if not api_key:
            return False
            
        # 检查是否使用了测试密钥（生产环境不允许）
        is_production = os.getenv("ENVIRONMENT", "production").lower() == "production"
        is_test_key = api_key in ["openmind_free", "test_key", "demo_key", "example"]
        
        if is_production and is_test_key:
            logging.error(f"Production environment using test API key for {service_name}")
            return False
            
        # 基本格式检查
        if len(api_key) < 10:
            logging.error(f"API key too short for {service_name}")
            return False
            
        return True
    
    @staticmethod
    def get_config_value(key: str, default: str = "", required: bool = True) -> str:
        """
        安全获取配置值
        
        Parameters
        ----------
        key : str
            配置键名
        default : str
            默认值
        required : bool
            是否必需
            
        Returns
        -------
        str
            配置值
        """
        value = os.getenv(key.upper(), default)
        if required and not value:
            logging.error(f"Required configuration value missing: {key}")
            raise ValueError(f"Required configuration value missing: {key}")
        
        return value