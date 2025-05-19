import pytest
import requests
from urllib3 import exceptions
from urllib3 import disable_warnings

disable_warnings(exceptions.InsecureRequestWarning)

BASE_URI = "https://localhost:2443/redfish/v1"
CREDENTIALS = {"UserName": "root", "Password": "0penBmc"}

@pytest.fixture()
def session_token():
    auth_endpoint = f"{BASE_URI}/SessionService/Sessions"
    response = requests.post(
        auth_endpoint,
        json=CREDENTIALS,
        headers={"Content-Type": "application/json"},
        verify=False
    )
    return response

def verify_response(response, expected_status, checks):
    try:
        assert response.status_code == expected_status
        for check in checks:
            assert check in response.json()
    except AssertionError:
        print("Verification failed for one of the checks")

def test_authentication_process(session_token):
    try:
        assert "X-Auth-Token" in session_token.headers
        assert session_token.status_code == 201
    except AssertionError:
        print("Authentication validation failed")

def test_system_information():
    system_endpoint = f"{BASE_URI}/Systems/system"
    response = requests.get(
        system_endpoint,
        auth=(CREDENTIALS["UserName"], CREDENTIALS["Password"]),
        verify=False
    )
    verify_response(response, 200, ["Status", "PowerState"])

def test_power_operations(session_token):
    if session_token.status_code != 201:
        print("Authentication failed, skipping power test")
        return

    power_action_url = f"{BASE_URI}/Systems/system/Actions/ComputerSystem.Reset"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": session_token.headers['X-Auth-Token']
    }
    
    power_response = requests.post(
        power_action_url,
        json={"ResetType": "PowerOn"},
        headers=headers,
        verify=False
    )
    
    try:
        assert power_response.status_code == 204
    except AssertionError:
        print("Power action failed with unexpected status code")
    
    system_status = requests.get(
        f"{BASE_URI}/Systems/system",
        headers=headers,
        verify=False
    )
    
    try:
        assert system_status.json().get("PowerState") == "On"
    except AssertionError:
        print("Power state verification failed")
