import requests
from django.conf import settings


def control_barrier(jetson_ip: str, camera_ip: str, command: str = "open") -> str:
    """
    Sends an open/close command to the Jetson for a specific camera.

    Args:
        jetson_ip (str): IP of the Jetson (parking area IP).
        camera_ip (str): IP of the ESP device.
        command (str): "open" or "close".

    Returns:
        str: Response from Jetson or error.
    """
    try:
        response = requests.post(
            url=f"http://{jetson_ip}/barrier/control/",
            headers={
                "Authorization": f"Bearer {settings.BARRIER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "ip": camera_ip,
                "command": command
            },
            timeout=3
        )
        response.raise_for_status()
        return response.json().get("device_response", "success")
    except requests.exceptions.RequestException as e:
        return f"Barrier control error: {e}"
