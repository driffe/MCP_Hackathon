import base64
import requests
import json
from datetime import datetime, timedelta
import time

# 테스트 서버 URL
BASE_URL = "http://localhost:5000"

# 요청 헤더
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def wait_for_server():
    """서버가 준비될 때까지 대기"""
    max_retries = 5
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 404:  # Flask 기본 404 응답은 서버가 실행 중임을 의미
                print("Server is ready")
                return True
        except requests.exceptions.RequestException:
            print(f"Waiting for server... (attempt {i+1}/{max_retries})")
            time.sleep(retry_delay)
    
    raise Exception("Server is not responding")

def create_test_user():
    """테스트용 사용자 데이터 생성"""
    user_data = {
        "user_id": "test_user_1",
        "name": "KIM",
        "age": 65,
        "vapi_config": {
            "emotion_detection": True,
            "language": "ko",
            "sensitivity": 0.8
        },
        "routine_config": {
            "check_interval_hours": 3,
            "max_silence_hours": 6,
            "medication_times": ["09:00", "21:00"]
        },
        "alert_config": {
            "primary_contact": "01012345678",
            "secondary_contact": "01087654321",
            "welfare_center": "02-1234-5678",
            "preferred_language": "ko"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/register",
        headers=HEADERS,
        json=user_data,
        timeout=10
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    result = response.json()
    print("User registration result:", result)
    if result["status"] == "success":
        return result["data"]
    else:
        raise Exception(f"User registration failed: {result['message']}")

def create_test_audio():
    """테스트용 더미 오디오 데이터 생성"""
    # 1초 길이의 무음 WAV 파일 (16kHz, 16bit)
    dummy_audio = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
    return base64.b64encode(dummy_audio).decode('utf-8')

def test_emotion_analysis(user_id):
    """감정 분석 테스트"""
    audio_data = create_test_audio()
    
    response = requests.post(
        f"{BASE_URL}/analyze_emotion/{user_id}",
        headers=HEADERS,
        json={"audio_data": audio_data},
        timeout=10
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    result = response.json()
    print("Emotion analysis result:", result)
    if result["status"] == "success":
        return result["data"]
    else:
        raise Exception(f"Emotion analysis failed: {result['message']}")

def test_routine_check(user_id):
    """일상 패턴 확인 테스트"""
    response = requests.get(
        f"{BASE_URL}/check_routine/{user_id}",
        headers=HEADERS,
        timeout=10
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    result = response.json()
    print("Daily pattern check result:", result)
    if result["status"] == "success":
        return result["data"]
    else:
        raise Exception(f"Daily pattern check failed: {result['message']}")

def test_alert_system():
    """알림 시스템 테스트"""
    alert_data = {
        "type": "emotional",
        "severity": "high",
        "message": "Emergency: Emotional state is unstable. Please check.",
        "context": {
            "emotion": "sad",
            "severity": 8.5,
            "timestamp": datetime.now().isoformat()
        },
        "recipients": ["01012345678", "01087654321"]
    }
    
    response = requests.post(
        f"{BASE_URL}/send_alert",
        headers=HEADERS,
        json=alert_data,
        timeout=10
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    result = response.json()
    print("Alert sending result:", result)
    if result["status"] == "success":
        return result["data"]
    else:
        raise Exception(f"Alert sending failed: {result['message']}")

def run_all_tests():
    """모든 테스트 실행"""
    print("=== Test start ===")
    
    # 서버가 준비될 때까지 대기
    wait_for_server()
    
    try:
        # 1. 사용자 등록
        user_result = create_test_user()
        user_id = user_result.get("user_id")
        
        if not user_id:
            print("User registration failed")
            return
        
        # 2. 감정 분석
        test_emotion_analysis(user_id)
        
        # 3. 일상 패턴 확인
        test_routine_check(user_id)
        
        # 4. 알림 시스템
        test_alert_system()
        
        print("=== Test completed ===")
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    run_all_tests() 