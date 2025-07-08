import gdown
import os

# Make sure the target directory exists
os.makedirs("player_detection_model/models", exist_ok=True)

# Replace with your actual Google Drive file ID
file_id = "1PKG4i0UX-jigDAJ5kEZEd3GiqDXuLHhp"

# Output file path
output_path = "player_detection_model/models/best.pt"

# Google Drive direct download URL
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file
print(f"Downloading best.pt model to {output_path}...")
gdown.download(url, output_path, quiet=False)
print("Download complete.")
