#!/usr/bin/env python3
"""
MCP 서버 테스트 스크립트
로컬에서 도구들이 제대로 작동하는지 확인
"""

import asyncio
import sys
import os
import httpx
from dotenv import load_dotenv

# 상위 디렉토리에서 .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

async def test_search_movie():
    """영화 검색 테스트"""
    print("=" * 60)
    print("테스트 1: 영화 검색")
    print("=" * 60)
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{TMDB_BASE_URL}/search/movie"
            api_params = {
                "api_key": TMDB_API_KEY,
                "query": "인터스텔라",
                "language": "ko-KR"
            }
            
            response = await client.get(url, params=api_params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        movies = data.get("results", [])[:5]
        
        print(f"\n✓ 검색 성공: {len(movies)}개 결과")
        for i, m in enumerate(movies, 1):
            print(f"\n{i}. {m.get('title')} ({m.get('release_date', 'N/A')})")
            print(f"   평점: {m.get('vote_average', 'N/A')}/10")
            print(f"   줄거리: {m.get('overview', '')[:100]}...")
        
        return {"success": True, "count": len(movies)}
        
    except Exception as e:
        print(f"\n❌ 검색 실패: {e}")
        return {"success": False, "error": str(e)}

async def test_get_movie_details():
    """영화 상세 정보 테스트"""
    print("\n" + "=" * 60)
    print("테스트 2: 영화 상세 정보 조회")
    print("=" * 60)
    
    try:
        # 인터스텔라의 TMDB ID
        movie_id = 157336
        
        async with httpx.AsyncClient() as client:
            url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            api_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR"
            }
            
            response = await client.get(url, params=api_params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        print(f"\n✓ 상세 정보 조회 성공")
        print(f"\n제목: {data.get('title')}")
        print(f"원제: {data.get('original_title')}")
        print(f"개봉일: {data.get('release_date')}")
        print(f"상영시간: {data.get('runtime')}분")
        print(f"장르: {', '.join([g['name'] for g in data.get('genres', [])])}")
        print(f"평점: {data.get('vote_average')}/10 ({data.get('vote_count')}명 평가)")
        print(f"\n줄거리:\n{data.get('overview', 'N/A')}")
        
        return {"success": True, "data": data}
        
    except Exception as e:
        print(f"\n❌ 조회 실패: {e}")
        return {"success": False, "error": str(e)}

async def main():
    """모든 테스트 실행"""
    print("\n[MCP 서버 로컬 테스트 시작]\n")
    
    # TMDB API 키 확인
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        print("❌ 오류: TMDB_API_KEY 환경 변수가 설정되지 않았습니다!")
        print("   .env 파일에 TMDB_API_KEY=your_api_key 를 추가하세요.")
        sys.exit(1)
    
    print(f"✓ TMDB API 키 확인됨: {api_key[:10]}...\n")
    
    try:
        # 테스트 실행
        await test_search_movie()
        await test_get_movie_details()
        
        print("=" * 60)
        print("✅ 모든 테스트 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
