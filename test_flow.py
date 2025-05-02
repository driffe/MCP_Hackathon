import requests
import base64

# 테스트 서버 URL
BASE_URL = "http://localhost:5000"

def create_dummy_audio():
    """더미 오디오 데이터 생성 (base64 인코딩된 더미 데이터)"""
    dummy_audio = "dummy_audio_data_for_testing"
    return base64.b64encode(dummy_audio.encode()).decode()

def test_analysis_and_notification():
    """감정 분석 및 이메일 알림 테스트"""
    print("\n=== 감정 분석 및 이메일 알림 테스트 ===")
    
    # 테스트 데이터 준비
    audio_data = create_dummy_audio()
    recipient_email = "test@example.com"  # 실제 이메일 주소로 변경 필요
    
    # API 요청 데이터
    payload = {
        "audio_data": audio_data,
        "recipient_email": recipient_email
    }
    
    # API 호출
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload
    )
    
    # 결과 출력
    print(f"응답 상태: {response.status_code}")
    print(f"응답 내용: {response.json()}")

if __name__ == "__main__":
    test_analysis_and_notification() 