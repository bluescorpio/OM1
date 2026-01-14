# 异常处理改进计划

## 发现的问题
1. 缺少超时处理
2. 异常信息不够详细
3. 缺少重试机制
4. 资源清理不完整

## 改进方案

### 1. 网络调用异常处理
```python
import asyncio
import logging
from typing import Optional, Type, Any
from functools import wraps

def with_retry(max_retries: int = 3, backoff_factor: float = 2.0):
    """
    装饰器：为网络调用添加重试机制
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** attempt
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        logging.error(f"All {max_retries} attempts failed. Last error: {e}")
                        raise
        return wrapper
    return decorator

def safe_operation(operation_name: str):
    """
    上下文管理器：安全执行操作，确保资源清理
    """
    class SafeOperation:
        def __enter__(self):
            logging.debug(f"Starting operation: {operation_name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                logging.error(f"Operation {operation_name} failed: {exc_val}")
            else:
                logging.debug(f"Operation {operation_name} completed successfully")
    
    return SafeOperation()
```

### 2. JSON解析安全处理
```python
import json
from typing import Any, Dict, Optional

def safe_json_loads(json_str: str, context: str = "unknown") -> Optional[Dict[str, Any]]:
    """
    安全JSON解析，包含详细错误信息
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error in {context}: {e}")
        logging.error(f"Invalid JSON content: {json_str[:200]}...")
        return None
    except Exception as e:
        logging.error(f"Unexpected error parsing JSON in {context}: {e}")
        return None

def safe_json_dumps(data: Any, context: str = "unknown") -> Optional[str]:
    """
    安全JSON序列化
    """
    try:
        return json.dumps(data)
    except (TypeError, ValueError) as e:
        logging.error(f"JSON serialization error in {context}: {e}")
        return None
```

### 3. 资源管理改进
```python
import atexit
import weakref
from typing import Set

class ResourceManager:
    """资源管理器，跟踪和清理资源"""
    
    def __init__(self):
        self._resources: Set[Any] = set()
        atexit.register(self.cleanup_all)
    
    def register_resource(self, resource: Any, cleanup_func: callable):
        """注册资源和清理函数"""
        weak_ref = weakref.ref(resource)
        self._resources.add((weak_ref, cleanup_func))
    
    def cleanup_resource(self, resource: Any):
        """清理特定资源"""
        for weak_ref, cleanup_func in self._resources:
            if weak_ref() is resource:
                try:
                    cleanup_func(resource)
                    self._resources.discard((weak_ref, cleanup_func))
                    break
                except Exception as e:
                    logging.error(f"Error cleaning up resource: {e}")
    
    def cleanup_all(self):
        """清理所有注册的资源"""
        for weak_ref, cleanup_func in list(self._resources):
            resource = weak_ref()
            if resource is not None:
                try:
                    cleanup_func(resource)
                except Exception as e:
                    logging.error(f"Error during cleanup: {e}")
        self._resources.clear()
```