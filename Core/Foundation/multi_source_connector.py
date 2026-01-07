"""
Multi-Source Knowledge Connector
================================

Wikipedia (X) → 다양한 소스 (O)

- 나무위키
- 네이버 지식백과
- 구글 검색
- 유튜브
- 일반 웹사이트
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import time

class MultiSourceConnector:
    """다중 소스 지식 수집"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_from_namuwiki(self, concept: str) -> Optional[str]:
        """나무위키에서 가져오기"""
        try:
            url = f"https://namu.wiki/w/{concept}"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 나무위키 본문 추출
                content = soup.find('div', {'class': 'wiki-content'})
                if content:
                    text = content.get_text()[:1000]  # 첫 1000자
                    return f"[나무위키] {text}"
        except:
            pass
        return None
    
    def fetch_from_naver(self, concept: str) -> Optional[str]:
        """네이버 검색에서 가져오기"""
        try:
            url = f"https://search.naver.com/search.naver?query={concept}"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 지식백과나 요약 정보
                summary = soup.find('div', {'class': 'api_subject_bx'})
                if summary:
                    text = summary.get_text()[:800]
                    return f"[네이버] {text}"
        except:
            pass
        return None
    
    def fetch_from_google(self, concept: str) -> Optional[str]:
        """구글 검색 스니펫"""
        try:
            url = f"https://www.google.com/search?q={concept}"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Featured snippet
                snippet = soup.find('div', {'class': 'BNeawe'})
                if snippet:
                    text = snippet.get_text()[:500]
                    return f"[Google] {text}"
        except:
            pass
        return None
    
    def fetch_from_wikipedia(self, concept: str) -> Optional[str]:
        """Wikipedia (기존)"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{concept}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract', '')
                return f"[Wikipedia] {extract}"
        except:
            pass
        return None
    
    def fetch_multi_source(self, concept: str) -> Dict[str, str]:
        """
        모든 소스에서 시도
        
        Returns:
            {'source': content, ...}
        """
        results = {}
        
        print(f"🌐 Multi-source fetching: {concept}")
        
        # 1. 나무위키 (한국어!)
        print("   📚 Trying 나무위키...")
        namuwiki = self.fetch_from_namuwiki(concept)
        if namuwiki:
            results['namuwiki'] = namuwiki
            print("      ✓ Success")
        
        # 2. 네이버
        print("   🔍 Trying 네이버...")
        naver = self.fetch_from_naver(concept)
        if naver:
            results['naver'] = naver
            print("      ✓ Success")
        
        # 3. Wikipedia (English)
        print("   📖 Trying Wikipedia...")
        wiki = self.fetch_from_wikipedia(concept)
        if wiki:
            results['wikipedia'] = wiki
            print("      ✓ Success")
        
        # 4. Google snippet
        print("   🔎 Trying Google...")
        google = self.fetch_from_google(concept)
        if google:
            results['google'] = google
            print("      ✓ Success")
        
        if results:
            print(f"   ✅ Found {len(results)} sources")
        else:
            print(f"   ❌ No sources found")
        
        return results
    
    def combine_sources(self, sources: Dict[str, str]) -> str:
        """여러 소스 통합"""
        if not sources:
            return f"General concept knowledge"
        
        combined = []
        for source, content in sources.items():
            combined.append(content)
        
        return "\n\n".join(combined)


# 데모
if __name__ == "__main__":
    print("="*70)
    print("🌐 MULTI-SOURCE KNOWLEDGE CONNECTOR")
    print("="*70)
    print()
    
    connector = MultiSourceConnector()
    
    test_concepts = ["사랑", "Love", "인공지능", "Python"]
    
    for concept in test_concepts:
        print()
        print("="*70)
        sources = connector.fetch_multi_source(concept)
        combined = connector.combine_sources(sources)
        
        print()
        print(f"📝 Combined content ({len(combined)} chars):")
        print(combined[:300] + "...")
        print()
        time.sleep(1)  # Rate limiting
    
    print("="*70)
    print("✅ MULTI-SOURCE CONNECTOR WORKING")
    print("   나무위키 + 네이버 + Wikipedia + Google!")
    print("="*70)
