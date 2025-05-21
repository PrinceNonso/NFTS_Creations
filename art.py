import os
import random
from PIL import Image
import json

# Configuration
OUTPUT_DIR = "output"
IMAGE_DIR = f"{OUTPUT_DIR}/images"
METADATA_DIR = f"{OUTPUT_DIR}/metadata"
NUM_NFTS = 520
LAYER_DIRS = ["background", "Fur", "eyes", "mouth", "Cloth", "earring", "hat"]

def setup_folders():
    """Ensure all required folders exist with at least one image"""
    # Create output directories
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)
    
    # Create layer directories and verify contents
    for layer in LAYER_DIRS:
        layer_path = os.path.join("layers", layer)
        os.makedirs(layer_path, exist_ok=True)
        
        # Check if folder has images
        if not any(f.endswith(('.png', '.jpg', '.jpeg')) for f in os.listdir(layer_path)):
            print(f"⚠️ No images found in {layer_path} - add some PNG/JPG files")
            # Create placeholder if you want (remove in production)
            Image.new('RGBA', (1000, 1000), (0, 0, 0, 0)).save(f"{layer_path}/placeholder.png")

def load_layers():
    """Load all layer images with error handling"""
    layers = {}
    for layer in LAYER_DIRS:
        layer_path = os.path.join("layers", layer)
        try:
            layers[layer] = [f for f in os.listdir(layer_path) 
                            if f.endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Loaded {len(layers[layer])} images from {layer_path}")
        except Exception as e:
            print(f"❌ Error loading {layer_path}: {str(e)}")
            layers[layer] = []
    return layers

def generate_nft(nft_id, layers, generated_combinations):
    """Generate one NFT with uniqueness check"""
    # Randomly select one trait per layer (skip empty layers)
    combination = []
    for layer in LAYER_DIRS:
        if not layers[layer]:
            continue  # Skip empty layers
        trait = random.choice(layers[layer])
        combination.append((layer, trait))
    
    # Check for uniqueness
    combination_key = tuple(combination)
    if combination_key in generated_combinations:
        return None
    generated_combinations.add(combination_key)
    
    # Create composite image
    base_image = None
    for layer, trait in combination:
        trait_path = os.path.join("layers", layer, trait)
        try:
            img = Image.open(trait_path).convert("RGBA")
            if base_image is None:
                base_image = img
                reference_size = img.size
            else:
                if img.size != reference_size:
                    img = img.resize(reference_size, Image.LANCZOS)
                base_image = Image.alpha_composite(base_image, img)
        except Exception as e:
            print(f"❌ Error processing {trait_path}: {str(e)}")
            return None
    
    # Save image
    image_path = os.path.join(IMAGE_DIR, f"{nft_id}.png")
    base_image.save(image_path, "PNG")
    
    # Create metadata
    metadata = {
        "name": f"NFT #{nft_id}",
        "description": "Unique auto-generated NFT",
        "image": f"ipfs://bafybeie4quiuijoxfxrunqy2ltamw5bhoynjuolnq25fcg6scdflfx5soi/{nft_id}.png",
        "attributes": [
            {"trait_type": layer, "value": os.path.splitext(trait)[0]}
            for layer, trait in combination
        ]
    }
    
    # Save metadata
    metadata_path = os.path.join(METADATA_DIR, f"{nft_id}.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
    
    return combination

def main():
    print("🚀 Starting NFT Generator")
    print(f"Working directory: {os.getcwd()}")
    
    # Setup folders and verify structure
    setup_folders()
    
    # Load layer assets
    layers = load_layers()
    
    # Generate NFTs
    count = 0
    nft_id = 1
    generated_combinations = set()
    
    while count < NUM_NFTS:
        result = generate_nft(nft_id, layers, generated_combinations)
        if result:
            print(f"✅ Generated NFT #{nft_id}")
            count += 1
        nft_id += 1
        
        # Safety check to prevent infinite loops
        if nft_id > NUM_NFTS * 10:  # 10x attempts
            print("⚠️ Warning: Having trouble finding unique combinations")
            break
    
    print(f"\n🎉 Successfully generated {count} unique NFTs!")
    print(f"Images saved to: {os.path.abspath(IMAGE_DIR)}")
    print(f"Metadata saved to: {os.path.abspath(METADATA_DIR)}")

if __name__ == "__main__":
    main()