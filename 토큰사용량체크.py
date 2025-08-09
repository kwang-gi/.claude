import json
import os
from pathlib import Path

def check_claude_usage():
    """Claude Code 토큰 사용량 체크"""
    
    projects_dir = Path("C:/Users/b/.claude/projects")
    total_input = 0
    total_output = 0
    total_cache_creation = 0
    total_cache_read = 0
    session_count = 0
    
    print("🔍 Claude Code 토큰 사용량 분석 중...")
    print("=" * 50)
    
    for project_path in projects_dir.glob("*/"):
        project_name = project_path.name.replace("--", "/")
        print(f"\n📁 프로젝트: {project_name}")
        
        for jsonl_file in project_path.glob("*.jsonl"):
            session_count += 1
            session_input = 0
            session_output = 0
            session_cache_creation = 0
            session_cache_read = 0
            
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            if 'message' in data and 'usage' in data['message']:
                                usage = data['message']['usage']
                                session_input += usage.get('input_tokens', 0)
                                session_output += usage.get('output_tokens', 0)
                                session_cache_creation += usage.get('cache_creation_input_tokens', 0)
                                session_cache_read += usage.get('cache_read_input_tokens', 0)
                        except json.JSONDecodeError:
                            continue
                            
            except Exception as e:
                print(f"   ❌ 파일 읽기 오류: {e}")
                continue
            
            if session_input > 0 or session_output > 0:
                print(f"   📄 {jsonl_file.name[:8]}...")
                print(f"      입력: {session_input:,} 토큰")
                print(f"      출력: {session_output:,} 토큰")
                if session_cache_creation > 0:
                    print(f"      캐시생성: {session_cache_creation:,} 토큰")
                if session_cache_read > 0:
                    print(f"      캐시읽기: {session_cache_read:,} 토큰")
            
            total_input += session_input
            total_output += session_output
            total_cache_creation += session_cache_creation
            total_cache_read += session_cache_read
    
    print("\n" + "=" * 50)
    print("📊 전체 사용량 요약")
    print("=" * 50)
    print(f"총 세션 수: {session_count}")
    print(f"총 입력 토큰: {total_input:,}")
    print(f"총 출력 토큰: {total_output:,}")
    print(f"총 캐시생성 토큰: {total_cache_creation:,}")
    print(f"총 캐시읽기 토큰: {total_cache_read:,}")
    print(f"전체 토큰 합계: {total_input + total_output + total_cache_creation + total_cache_read:,}")
    
    # 대략적인 비용 계산 (Sonnet 4 기준)
    # 입력: $3/M토큰, 출력: $15/M토큰 (대략)
    input_cost = (total_input + total_cache_creation + total_cache_read) / 1000000 * 3
    output_cost = total_output / 1000000 * 15
    total_cost = input_cost + output_cost
    
    print(f"\n💰 예상 비용 (대략적)")
    print(f"입력 비용: ${input_cost:.2f}")
    print(f"출력 비용: ${output_cost:.2f}")
    print(f"총 비용: ${total_cost:.2f}")

if __name__ == "__main__":
    check_claude_usage()