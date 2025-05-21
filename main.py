import os
import json
import shutil
from dotenv import load_dotenv

load_dotenv()

# Configuration
IMAGE_FOLDER = "images"
METADATA_FOLDER = "metadata"
BASE_IPFS_IMAGE_URL = os.getenv("BASE_IPFS_IMAGE_URL")
COLLECTION_NAME = "Collection Name"
EXTERNAL_URL = "https://yourwebsite.com"
ROYALTY_PERCENTAGE = 7.5  # Royalty percentage (e.g., 7.5%)

# Ensure folders exist
os.makedirs(METADATA_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = (".jpeg", ".jpg", ".png", ".gif", ".mp4", ".webm")

def generate_metadata(token_id, filename):
    """Generate OpenSea-compatible metadata with rarity traits"""
    # Example trait generator - replace with your actual trait logic
    background = get_random_trait("Background", ["Default", "Stormy", "Dojo", "Lightning Storm"])
    eyes = get_random_trait("Eyes", ["Normal", "Electric Yellow", "Glowing Gold", "Thunder God Red"])
    
    return {
        # Core OpenSea fields
        "name": f"{COLLECTION_NAME} #{token_id}",
        "description": f"A unique {COLLECTION_NAME} NFT featuring Zenitsu. {get_flavor_text(background, eyes)}",
        "image": f"{BASE_IPFS_IMAGE_URL}/{filename}",
        "external_url": EXTERNAL_URL,
        "animation_url": get_animation_url(filename),  # For animated NFTs
        
        # Seller fees (royalties)
        "seller_fee_basis_points": int(ROYALTY_PERCENTAGE * 100),  # 7.5% = 750
        "fee_recipient": "0xYOUR_WALLET_ADDRESS",  # Your royalty wallet
        
        # OpenSea-specific display
        "background_color": "FFFFFF",  # White background
        "youtube_url": "https://youtube.com/yourchannel",  # Optional
        
        # Attributes with rarity
        "attributes": [
            {"trait_type": "Background", "value": background},
            {"trait_type": "Eyes", "value": eyes},
            {"trait_type": "Rarity", "value": calculate_rarity(background, eyes)},
            # Add more traits as needed
        ],
        
        # Collection metadata (optional but recommended)
        "collection": {
            "name": COLLECTION_NAME,
            "family": "Demon Slayer"  # Your project family
        }
    }

# Helper functions (implement your logic here)
def get_random_trait(trait_type, options):
    """Mock function - replace with your actual weighted randomness"""
    import random
    return random.choice(options)

def calculate_rarity(*traits):
    """Determine rarity based on traits"""
    if "Thunder God Red" in traits:
        return "Legendary"
    elif "Glowing Gold" in traits:
        return "Rare"
    else:
        return "Common"

def get_flavor_text(background, eyes):
    """Generate dynamic description based on traits"""
    if eyes == "Thunder God Red":
        return "This Legendary Zenitsu possesses the ultimate Thunder God form."
    return "A powerful Demon Slayer from the Hidden Thunder Village."

def get_animation_url(filename):
    """Optional: Point to animated version if exists"""
    base_name = os.path.splitext(filename)[0]
    for ext in [".mp4", ".gif", ".webm"]:
        if os.path.exists(f"{IMAGE_FOLDER}/{base_name}{ext}"):
            return f"{BASE_IPFS_IMAGE_URL}/{base_name}{ext}"
    return None

# Main execution
if __name__ == "__main__":
    # Rename and process images
    image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(ALLOWED_EXTENSIONS)])
    
    for new_index, old_name in enumerate(image_files):
        ext = os.path.splitext(old_name)[1].lower()
        new_name = f"{new_index}{ext}"
        
        # Rename file
        src = os.path.join(IMAGE_FOLDER, old_name)
        dst = os.path.join(IMAGE_FOLDER, new_name)
        shutil.move(src, dst)
        
        # Generate metadata
        metadata = generate_metadata(new_index, new_name)
        with open(f"{METADATA_FOLDER}/{new_index}.json", "w") as f:
            json.dump(metadata, f, indent=2)
    
    print(f"Success! Generated {len(image_files)} metadata files with OpenSea standards.")