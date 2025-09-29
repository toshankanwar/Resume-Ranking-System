import redis
import json
import hashlib
from typing import Any, Optional, Dict
import pickle
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis-based caching system for resume processing results"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.redis_url = self.config.get('REDIS_URL', 'redis://localhost:6379/0')
        self.default_ttl = self.config.get('CACHE_DEFAULT_TIMEOUT', 3600)  # 1 hour
        self.prefix = self.config.get('CACHE_PREFIX', 'resume_ranking:')
        
        try:
            self.redis_client = redis.from_url(self.redis_url)
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Redis cache initialization failed: {e}")
            self.enabled = False
            self.redis_client = None
    
    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate a unique cache key from arguments"""
        # Create a string representation of all arguments
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        
        # Create hash of the key data
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{self.prefix}{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        
        try:
            full_key = f"{self.prefix}{key}" if not key.startswith(self.prefix) else key
            cached_data = self.redis_client.get(full_key)
            
            if cached_data:
                return pickle.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        if not self.enabled:
            return False
        
        try:
            full_key = f"{self.prefix}{key}" if not key.startswith(self.prefix) else key
            ttl = ttl or self.default_ttl
            
            serialized_data = pickle.dumps(value)
            self.redis_client.setex(full_key, ttl, serialized_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.enabled:
            return False
        
        try:
            full_key = f"{self.prefix}{key}" if not key.startswith(self.prefix) else key
            return bool(self.redis_client.delete(full_key))
            
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def cache_algorithm_result(self, algorithm_name: str, resume_text: str, 
                              job_description: str, result: Dict[str, Any], 
                              ttl: int = None) -> bool:
        """Cache algorithm processing result"""
        
        cache_key = self._generate_cache_key(
            'algorithm_result',
            algorithm_name,
            resume_text[:500],  # First 500 chars to avoid huge keys
            job_description[:500]
        )
        
        cache_data = {
            'result': result,
            'timestamp': datetime.utcnow().isoformat(),
            'algorithm': algorithm_name
        }
        
        return self.set(cache_key, cache_data, ttl or 1800)  # 30 minutes default
    
    def get_cached_algorithm_result(self, algorithm_name: str, resume_text: str, 
                                   job_description: str) -> Optional[Dict[str, Any]]:
        """Get cached algorithm result"""
        
        cache_key = self._generate_cache_key(
            'algorithm_result',
            algorithm_name,
            resume_text[:500],
            job_description[:500]
        )
        
        cached_data = self.get(cache_key)
        
        if cached_data:
            # Check if cache is still valid (additional check)
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.utcnow() - cache_time < timedelta(hours=1):
                return cached_data['result']
        
        return None
    
    def cache_file_text(self, file_hash: str, extracted_text: str, 
                       ttl: int = None) -> bool:
        """Cache extracted text from file"""
        
        cache_key = f"file_text:{file_hash}"
        
        cache_data = {
            'text': extracted_text,
            'timestamp': datetime.utcnow().isoformat(),
            'length': len(extracted_text)
        }
        
        return self.set(cache_key, cache_data, ttl or 86400)  # 24 hours default
    
    def get_cached_file_text(self, file_hash: str) -> Optional[str]:
        """Get cached file text"""
        
        cache_key = f"file_text:{file_hash}"
        cached_data = self.get(cache_key)
        
        if cached_data:
            return cached_data['text']
        
        return None
    
    def cache_model_embeddings(self, model_name: str, text_hash: str, 
                              embeddings: Any, ttl: int = None) -> bool:
        """Cache model embeddings"""
        
        cache_key = f"embeddings:{model_name}:{text_hash}"
        
        cache_data = {
            'embeddings': embeddings,
            'timestamp': datetime.utcnow().isoformat(),
            'model': model_name
        }
        
        return self.set(cache_key, cache_data, ttl or 7200)  # 2 hours default
    
    def get_cached_embeddings(self, model_name: str, text_hash: str) -> Optional[Any]:
        """Get cached embeddings"""
        
        cache_key = f"embeddings:{model_name}:{text_hash}"
        cached_data = self.get(cache_key)
        
        if cached_data:
            return cached_data['embeddings']
        
        return None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.enabled:
            return {'enabled': False}
        
        try:
            info = self.redis_client.info()
            keys = self.redis_client.keys(f"{self.prefix}*")
            
            return {
                'enabled': True,
                'total_keys': len(keys),
                'memory_used': info.get('used_memory_human', 'N/A'),
                'connected_clients': info.get('connected_clients', 0),
                'cache_hits': info.get('keyspace_hits', 0),
                'cache_misses': info.get('keyspace_misses', 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def clear_cache(self, pattern: str = None) -> int:
        """Clear cache entries"""
        if not self.enabled:
            return 0
        
        try:
            if pattern:
                keys = self.redis_client.keys(f"{self.prefix}{pattern}")
            else:
                keys = self.redis_client.keys(f"{self.prefix}*")
            
            if keys:
                return self.redis_client.delete(*keys)
            
            return 0
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return 0
