import time
import pychromecast

# Configuration
DEVICE_IP = "192.168.0.203"  # Your Chromecast's IP
TARGET_DEVICE_NAME = 'Master Bedroom TV'  # Your Target Device's Name
MAX_VOLUME = 0.61  # Maximum allowed volume (0.0 - 1.0)
SAFE_VOLUME = 0.6  # Volume to set when it's too high
CHECK_INTERVAL = 2  # Time (seconds) between checks

def get_chromecasts():
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Master Bedroom TV"])
    for cast in chromecasts:
        if cast.name == TARGET_DEVICE_NAME:
            cast.wait()
            print(cast.status.volume_level)
            browser.stop_discovery()
            print(f"Connected to Chromecast: {cast.name}")
            return cast
    browser.stop_discovery()


def monitor_volume():
    """Monitors and adjusts volume if it exceeds the allowed level."""
    cast = get_chromecasts()

    if not cast:
        print("Could not connect to Chromecast. Exiting.")
        return

    while True:
        try:
            current_volume = cast.status.volume_level  # Get volume level

            print(f"Current volume: {current_volume * 100:.0f}%")

            if current_volume > MAX_VOLUME:
                print(f"Volume too high! Lowering to {SAFE_VOLUME * 100:.0f}%")
                cast.set_volume(SAFE_VOLUME)

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Error during volume check: {e}")
            time.sleep(300)  # Wait and retry if there's an error


if __name__ == "__main__":
    monitor_volume()
