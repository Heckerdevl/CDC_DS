import os
import math
import requests
import pandas as pd
from tqdm import tqdm
from PIL import Image
from io import BytesIO

class ImageryHarvester:
    def __init__(self, output_dir="raw_satellite_tiles", zoom=19):
        self.output_dir = output_dir
        self.zoom = zoom
        self.base_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _lat_lon_to_tile(self, lat, lon):
        """Converts geographic coordinates to Slippy Map tile indices."""
        lat_rad = math.radians(lat)
        n = 2.0 ** self.zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return x, y

    def download_single_tile(self, lat, lon, filename):
        """Fetches a single tile from the ESRI World Imagery server."""
        x, y = self._lat_lon_to_tile(lat, lon)
        tile_url = f"{self.base_url}/{self.zoom}/{y}/{x}"
        save_path = os.path.join(self.output_dir, filename)

        # Skip if already downloaded (Caching)
        if os.path.exists(save_path):
            return True

        headers = {'User-Agent': 'GeospatialResearchBot/1.1'}
        
        try:
            response = requests.get(tile_url, headers=headers, timeout=12)
            if response.status_code == 200:
                with Image.open(BytesIO(response.content)) as img:
                    img.convert("RGB").save(save_path, "JPEG", quality=95)
                return True
        except Exception as e:
            # Silent failure for cleaner tqdm output
            return False
        return False

def run_harvest():
    # Load your dataset
    dataset_path = "train(1)(train(1)).csv"
    df = pd.read_csv(dataset_path)

    # Initialize Harvester
    harvester = ImageryHarvester(output_dir="property_visuals")

    print(f"🌍 Starting High-Res Imagery Harvest for {len(df)} properties...")
    
    success_count = 0
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Harvesting Tiles"):
        # Dynamic filename generation
        file_name = f"tile_id_{idx}.jpg"
        
        status = harvester.download_single_tile(row['lat'], row['long'], file_name)
        if status:
            success_count += 1

    print(f"\n✅ Harvest Complete! {success_count} images stored in {harvester.output_dir}.")

if __name__ == "__main__":
    run_harvest()