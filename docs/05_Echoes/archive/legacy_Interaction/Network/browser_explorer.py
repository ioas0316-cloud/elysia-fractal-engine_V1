"""
Browser Explorer (브라우저 탐색기)
==================================

지휘자님의 Chrome 프로필을 사용하여 웹 탐색
- 로그인된 상태 유지 (YouTube 유료, Google 등)
- API 키 불필요
- 실제 브라우저와 동일
"""

import os
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logger = logging.getLogger("Elysia.BrowserExplorer")


class BrowserExplorer:
    """
    브라우저 탐색기
    
    지휘자님의 Chrome 프로필을 그대로 사용하여:
    - 로그인된 상태에서 검색
    - YouTube 프리미엄, Google 계정 등 활용
    - API 제한 없이 탐색
    """
    
    def __init__(self, use_profile: bool = True):
        """
        Args:
            use_profile: True면 지휘자님 Chrome 프로필 사용
        """
        self.driver = None
        self.use_profile = use_profile
        
        # Chrome 프로필 경로 (Windows 기본)
        self.profile_path = os.path.expanduser(
            r"~\AppData\Local\Google\Chrome\User Data"
        )
        
        logger.info("🌐 BrowserExplorer initialized")
    
    def start(self, headless: bool = True):
        """브라우저 시작"""
        options = Options()
        
        if headless:
            options.add_argument("--headless=new")
        
        if self.use_profile and os.path.exists(self.profile_path):
            # 지휘자님 Chrome 프로필 사용
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")
            logger.info(f"   Using Chrome profile: {self.profile_path}")
        
        # 기타 옵션
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("   ✅ Browser started")
            return True
        except Exception as e:
            logger.error(f"   ❌ Browser start failed: {e}")
            return False
    
    def stop(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("   Browser stopped")
    
    def google_search(self, query: str) -> Dict[str, Any]:
        """
        Google 검색
        
        Returns:
            검색 결과 (제목, 스니펫, URL)
        """
        if not self.driver:
            self.start()
        
        try:
            # Google 검색
            self.driver.get(f"https://www.google.com/search?q={query}")
            time.sleep(2)  # 로딩 대기
            
            results = []
            
            # 검색 결과 추출
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for i, result in enumerate(search_results[:5]):  # 상위 5개
                try:
                    title_elem = result.find_element(By.CSS_SELECTOR, "h3")
                    link_elem = result.find_element(By.CSS_SELECTOR, "a")
                    
                    # 스니펫 추출 시도
                    snippet = ""
                    try:
                        snippet_elem = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                        snippet = snippet_elem.text
                    except:
                        pass
                    
                    results.append({
                        "rank": i + 1,
                        "title": title_elem.text,
                        "url": link_elem.get_attribute("href"),
                        "snippet": snippet
                    })
                except:
                    continue
            
            return {
                "query": query,
                "results": results,
                "success": len(results) > 0
            }
            
        except Exception as e:
            logger.error(f"Google search failed: {e}")
            return {"query": query, "results": [], "success": False, "error": str(e)}
    
    def youtube_search(self, query: str) -> Dict[str, Any]:
        """
        YouTube 검색 (로그인된 상태로!)
        """
        if not self.driver:
            self.start()
        
        try:
            self.driver.get(f"https://www.youtube.com/results?search_query={query}")
            time.sleep(3)  # 로딩 대기
            
            results = []
            
            # 비디오 결과 추출
            videos = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
            
            for i, video in enumerate(videos[:5]):
                try:
                    title_elem = video.find_element(By.CSS_SELECTOR, "#video-title")
                    channel_elem = video.find_element(By.CSS_SELECTOR, "#channel-name")
                    
                    results.append({
                        "rank": i + 1,
                        "title": title_elem.text,
                        "url": title_elem.get_attribute("href"),
                        "channel": channel_elem.text
                    })
                except:
                    continue
            
            return {
                "query": query,
                "results": results,
                "success": len(results) > 0
            }
            
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            return {"query": query, "results": [], "success": False, "error": str(e)}


# =============================================================================
# 테스트
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🌐 Browser Explorer Test")
    print("   지휘자님 Chrome 프로필로 검색")
    print("=" * 60)
    
    explorer = BrowserExplorer(use_profile=False)  # 테스트는 새 프로필로
    
    if explorer.start(headless=True):
        print("\n📌 Google 검색 테스트")
        result = explorer.google_search("자유란 무엇인가")
        
        if result["success"]:
            for r in result["results"][:3]:
                print(f"   {r['rank']}. {r['title'][:40]}...")
        
        explorer.stop()
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
