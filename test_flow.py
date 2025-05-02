import requests
import base64

# test server URL
BASE_URL = "http://localhost:5000"

def create_dummy_audio():
    """create dummy audio data (base64 encoded dummy data)"""
    dummy_audio = "dummy_audio_data_for_testing"
    return base64.b64encode(dummy_audio.encode()).decode()

def test_analysis_and_notification():
    """emotion analysis and email notification test"""
    print("\n=== emotion analysis and email notification test ===")
    
    # prepare test data
    audio_data = create_dummy_audio()
    recipient_email = "syoh2k@gmail.com"  # email address for testing
    
    # API request data
    payload = {
        "audio_data": audio_data,
        "recipient_email": recipient_email
    }
    
    # API call
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload
    )
    
    # print result
    print(f"response status: {response.status_code}")
    print(f"response content: {response.json()}")

if __name__ == "__main__":
    test_analysis_and_notification() 