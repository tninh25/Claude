# utils/conversation_id.py

import time

def generate_time_based_conversation_suffix(window_seconds: int = 10) -> str:
    """
    Sinh suffix cho conversation_id theo block thời gian
    Mặc định: 5 phút = 300s
    """
    time_bucket = int(time.time() // window_seconds)
    return str(time_bucket)

if __name__ == '__main__':
    print(generate_time_based_conversation_suffix())