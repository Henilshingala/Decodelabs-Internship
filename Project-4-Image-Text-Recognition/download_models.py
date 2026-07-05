import os
import urllib.request
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent / "models"
MODELS = {
    "MobileNetSSD_deploy.prototxt": {
        "url": "https://raw.githubusercontent.com/djmv/MobilNet_SSD_opencv/master/MobileNetSSD_deploy.prototxt",
        "min_size": 20000  # ~29KB
    },
    "MobileNetSSD_deploy.caffemodel": {
        "url": "https://github.com/djmv/MobilNet_SSD_opencv/raw/master/MobileNetSSD_deploy.caffemodel",
        "min_size": 20000000  # ~23MB
    }
}

def download_file(url: str, dest: Path, min_size: int = 0) -> bool:
    if dest.exists():
        if dest.stat().st_size >= min_size:
            logger.info(f"File already exists and passes size check: {dest.name}")
            return True
        else:
            logger.warning(f"File {dest.name} exists but is too small (incomplete download). Redownloading...")
            dest.unlink()
            
    logger.info(f"Downloading {dest.name} from {url}...")
    try:
        urllib.request.urlretrieve(url, str(dest))
        if dest.exists() and dest.stat().st_size >= min_size:
            logger.info(f"Successfully downloaded {dest.name} ({dest.stat().st_size / (1024*1024):.2f} MB)")
            return True
        else:
            logger.error(f"Downloaded {dest.name} but size {dest.stat().st_size} is smaller than expected {min_size}.")
            if dest.exists():
                dest.unlink()
            return False
    except Exception as e:
        logger.error(f"Failed to download {dest.name}: {e}")
        return False

def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    all_success = True
    for filename, info in MODELS.items():
        dest = MODELS_DIR / filename
        success = download_file(info["url"], dest, info["min_size"])
        if not success:
            all_success = False
            
    if all_success:
        logger.info("All model files are present and verified.")
    else:
        logger.error("Some model files failed to download.")
        
if __name__ == "__main__":
    main()
