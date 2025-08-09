import json
import os
from pathlib import Path

def check_claude_usage():
    """Claude Code Token Usage Checker"""
    
    projects_dir = Path("C:/Users/b/.claude/projects")
    total_input = 0
    total_output = 0
    total_cache_creation = 0
    total_cache_read = 0
    session_count = 0
    
    print("Claude Code Token Usage Analysis")
    print("=" * 50)
    
    for project_path in projects_dir.glob("*/"):
        project_name = project_path.name.replace("--", "/")
        print(f"\nProject: {project_name}")
        
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
                print(f"   Error reading file: {e}")
                continue
            
            if session_input > 0 or session_output > 0:
                print(f"   Session {jsonl_file.name[:8]}...")
                print(f"      Input: {session_input:,} tokens")
                print(f"      Output: {session_output:,} tokens")
                if session_cache_creation > 0:
                    print(f"      Cache Creation: {session_cache_creation:,} tokens")
                if session_cache_read > 0:
                    print(f"      Cache Read: {session_cache_read:,} tokens")
            
            total_input += session_input
            total_output += session_output
            total_cache_creation += session_cache_creation
            total_cache_read += session_cache_read
    
    print("\n" + "=" * 50)
    print("TOTAL USAGE SUMMARY")
    print("=" * 50)
    print(f"Total Sessions: {session_count}")
    print(f"Total Input Tokens: {total_input:,}")
    print(f"Total Output Tokens: {total_output:,}")
    print(f"Total Cache Creation Tokens: {total_cache_creation:,}")
    print(f"Total Cache Read Tokens: {total_cache_read:,}")
    print(f"GRAND TOTAL: {total_input + total_output + total_cache_creation + total_cache_read:,} tokens")
    
    # Approximate cost calculation (Sonnet 4 pricing)
    input_cost = (total_input + total_cache_creation + total_cache_read) / 1000000 * 3
    output_cost = total_output / 1000000 * 15
    total_cost = input_cost + output_cost
    
    print(f"\nESTIMATED COST (Approximate)")
    print(f"Input Cost: ${input_cost:.2f}")
    print(f"Output Cost: ${output_cost:.2f}")
    print(f"Total Cost: ${total_cost:.2f}")

if __name__ == "__main__":
    check_claude_usage()