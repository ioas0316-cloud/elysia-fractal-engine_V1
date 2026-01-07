"""
Naver Search Connector (네이버 검색 커넥터)
==========================================

네이버 오픈 API를 사용한 검색
- 무료 (하루 25,000건)
- 한글 검색에 최적화
- API 키 필요: https://developers.naver.com/

설정 방법:
1. https://developers.naver.com/ 접속
2. 애플리케이션 등록
3. 검색 API 선택
4. Client ID와 Client Secret을 환경변수에 저장:
   - NAVER_CLIENT_ID
   - NAVER_CLIENT_SECRET
"""

import os
import urllib.request
import urllib.parse
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("Elysia.NaverConnector")


class NaverSearchConnector:
    """
    네이버 검색 API 커넥터
    
    지원 검색 유형:
    - 블로그
    - 뉴스
    - 웹문서
    - 백과사전
    - 지식iN
    """
    
    def __init__(self):
        self.client_id = os.getenv('NAVER_CLIENT_ID')
        self.client_secret = os.getenv('NAVER_CLIENT_SECRET')
        
        self.base_url = "https://openapi.naver.com/v1/search"
        
        self.available = bool(self.client_id and self.client_secret)
        
        if self.available:
            logger.info("✅ Naver API connected")
        else:
            logger.warning("⚠️ Naver API keys not found. Set NAVER_CLIENT_ID and NAVER_CLIENT_SECRET")
    
    def _request(self, endpoint: str, query: str, display: int = 5) -> Optional[Dict]:
        """API 요청"""
        if not self.available:
            return None
        
        try:
            encoded = urllib.parse.quote(query)
            url = f"{self.base_url}/{endpoint}?query={encoded}&display={display}"
            
            req = urllib.request.Request(url)
            req.add_header("X-Naver-Client-Id", self.client_id)
            req.add_header("X-Naver-Client-Secret", self.client_secret)
            
            response = urllib.request.urlopen(req, timeout=10)
            return json.loads(response.read().decode())
            
        except Exception as e:
            logger.error(f"Naver API error: {e}")
            return None
    
    def search_encyclopedia(self, query: str, display: int = 3) -> Dict[str, Any]:
        """
        백과사전 검색 (가장 신뢰도 높음)
        """
        result = self._request("encyc", query, display)
        
        if result and result.get("items"):
            items = result["items"]
            return {
                "query": query,
                "source": "naver_encyclopedia",
                "success": True,
                "results": [
                    {
                        "title": self._clean_html(item.get("title", "")),
                        "description": self._clean_html(item.get("description", "")),
                        "link": item.get("link", "")
                    }
                    for item in items
                ]
            }
        
        return {"query": query, "source": "naver_encyclopedia", "success": False, "results": []}
    
    def search_kin(self, query: str, display: int = 3) -> Dict[str, Any]:
        """
        지식iN 검색
        """
        result = self._request("kin", query, display)
        
        if result and result.get("items"):
            items = result["items"]
            return {
                "query": query,
                "source": "naver_kin",
                "success": True,
                "results": [
                    {
                        "title": self._clean_html(item.get("title", "")),
                        "description": self._clean_html(item.get("description", "")),
                        "link": item.get("link", "")
                    }
                    for item in items
                ]
            }
        
        return {"query": query, "source": "naver_kin", "success": False, "results": []}
    
    def search_webkr(self, query: str, display: int = 5) -> Dict[str, Any]:
        """
        웹문서 검색 (일반 검색)
        """
        result = self._request("webkr", query, display)
        
        if result and result.get("items"):
            items = result["items"]
            return {
                "query": query,
                "source": "naver_web",
                "success": True,
                "results": [
                    {
                        "title": self._clean_html(item.get("title", "")),
                        "description": self._clean_html(item.get("description", "")),
                        "link": item.get("link", "")
                    }
                    for item in items
                ]
            }
        
        return {"query": query, "source": "naver_web", "success": False, "results": []}
    
    def search_best(self, query: str) -> Dict[str, Any]:
        """
        최적 검색 - 백과사전 우선, 없으면 지식iN
        """
        # 1. 백과사전 시도
        result = self.search_encyclopedia(query)
        if result["success"] and result["results"]:
            return result
        
        # 2. 지식iN 시도
        result = self.search_kin(query)
        if result["success"] and result["results"]:
            return result
        
        # 3. 웹문서 시도
        return self.search_webkr(query)
    
    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        import re
        clean = re.sub(r'<[^>]+>', '', text)
        return clean.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')


# =============================================================================
# 테스트
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🔍 Naver Search Connector Test")
    print("=" * 60)
    
    naver = NaverSearchConnector()
    
    if naver.available:
        result = naver.search_best("자유란 무엇인가")
        
        if result["success"]:
            print(f"\n✅ Source: {result['source']}")
            for r in result["results"][:2]:
                print(f"   📖 {r['title']}")
                print(f"      {r['description'][:80]}...")
        else:
            print("❌ No results")
    else:
        print("\n⚠️ Naver API not configured")
        print("   Set environment variables:")
        print("   - NAVER_CLIENT_ID")
        print("   - NAVER_CLIENT_SECRET")
        print("\n   Get keys at: https://developers.naver.com/")
    
    print("\n" + "=" * 60)
