import os
import time
from datetime import datetime, timedelta
import requests

# URLs for TLE data
TLE_URLS = {
    "cosmos_1408": "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-1408-debris&FORMAT=tle",
    "fengyun_1c": "https://celestrak.org/NORAD/elements/gp.php?GROUP=fengyun-1c-debris&FORMAT=tle",
    "iridium_33": "https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium-33-debris&FORMAT=tle",
    "cosmos_2251": "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-2251-debris&FORMAT=tle",
    "active_satellites": "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
}

# Directory to save TLE files
SAVE_DIR = "tle_data"

# Create the save directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Duration for data collection (in hours)
HOURS_TO_COLLECT = 10 * 24  # 10 days

# Function to download a TLE file
def download_tle(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "w") as file:
                file.write(response.text)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download {url} - HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Main function to automate hourly downloads
def download_tle_hourly():
    end_time = datetime.now() + timedelta(hours=HOURS_TO_COLLECT)
    while datetime.now() < end_time:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        for name, url in TLE_URLS.items():
            filename = f"{name}_{timestamp}.txt"
            save_path = os.path.join(SAVE_DIR, filename)
            download_tle(url, save_path)

        print("Waiting for the next hour...")
        time.sleep(3600)  # Wait for one hour

if __name__ == "__main__":
    download_tle_hourly()