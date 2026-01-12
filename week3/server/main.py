#!/usr/bin/env python3
"""
TMDB Movie MCP Server
영화 정보를 검색하는 MCP 서버
"""

import sys
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# MCP 서버 초기화
mcp = FastMCP("TMDB Movie Server")

# TMDB API 설정
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# 로깅은 stderr로!
def log(message: str):
    sys.stderr.write(f"[MCP Server] {message}\n")
    sys.stderr.flush()

# ===== 도구 1: 영화 검색 =====
class SearchMovieInput(BaseModel):
    query: str = Field(description="검색할 영화 제목")
    year: int | None = Field(None, description="개봉 연도 (선택)")

@mcp.tool()
async def search_movie(params: SearchMovieInput) -> dict:
    """영화를 제목으로 검색합니다."""
    try:
        log(f"영화 검색 시작: {params.query}")
        
        # API 호출
        async with httpx.AsyncClient() as client:
            url = f"{TMDB_BASE_URL}/search/movie"
            api_params = {
                "api_key": TMDB_API_KEY,
                "query": params.query,
                "language": "ko-KR"
            }
            if params.year:
                api_params["year"] = params.year
            
            response = await client.get(url, params=api_params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # 결과 정리
        movies = data.get("results", [])[:5]  # 상위 5개만
        
        log(f"검색 완료: {len(movies)}개 결과")
        
        return {
            "movies": [
                {
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "release_date": m.get("release_date"),
                    "overview": m.get("overview", "")[:200] + "..." if len(m.get("overview", "")) > 200 else m.get("overview", ""),
                    "vote_average": m.get("vote_average")
                }
                for m in movies
            ],
            "total": len(movies)
        }
        
    except httpx.HTTPStatusError as e:
        log(f"API 에러: {e.response.status_code}")
        return {"error": f"API 오류: {e.response.status_code}"}
    except Exception as e:
        log(f"예상치 못한 에러: {str(e)}")
        return {"error": "검색 중 오류 발생"}

# ===== 도구 2: 영화 상세 정보 =====
class MovieDetailsInput(BaseModel):
    movie_id: int = Field(description="TMDB 영화 ID")

@mcp.tool()
async def get_movie_details(params: MovieDetailsInput) -> dict:
    """영화의 상세 정보를 가져옵니다."""
    try:
        log(f"영화 상세 정보 조회: ID {params.movie_id}")
        
        async with httpx.AsyncClient() as client:
            url = f"{TMDB_BASE_URL}/movie/{params.movie_id}"
            api_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR"
            }
            
            response = await client.get(url, params=api_params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        log("상세 정보 조회 완료")
        
        return {
            "id": data.get("id"),
            "title": data.get("title"),
            "original_title": data.get("original_title"),
            "release_date": data.get("release_date"),
            "runtime": data.get("runtime"),
            "genres": [g["name"] for g in data.get("genres", [])],
            "overview": data.get("overview"),
            "vote_average": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "budget": data.get("budget"),
            "revenue": data.get("revenue")
        }
        
    except httpx.HTTPStatusError as e:
        log(f"API 에러: {e.response.status_code}")
        return {"error": f"API 오류: {e.response.status_code}"}
    except Exception as e:
        log(f"예상치 못한 에러: {str(e)}")
        return {"error": "조회 중 오류 발생"}

# ===== 서버 실행 =====
if __name__ == "__main__":
    log("TMDB MCP 서버 시작")
    mcp.run(transport="stdio")