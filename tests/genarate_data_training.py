import os 
import argparse
from tqdm import tqdm

def read_folder(folder_path):
    """Scan folder and return list of image paths"""
    image_list = []
    
    # Count total files first
    total_files = sum([len(files) for _, _, files in os.walk(folder_path)])
    
    with tqdm(total=total_files, desc="Scanning images") as pbar:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    image_list.append(os.path.join(root, file))
                pbar.update(1)
    
    return image_list

def generate_label_file(image_list, output_label_file):
    """Generate PaddleOCR label file from images with corresponding .txt files"""
    
    successful = 0
    skipped = 0
    
    with open(output_label_file, "w", encoding='utf-8') as f:
        for image_path in tqdm(image_list, desc="Generating labels"):
            if not os.path.exists(image_path):
                skipped += 1
                continue

            # Get corresponding label file path
            if image_path.endswith('.jpg'):
                label_path = image_path.replace(".jpg", ".txt")
            elif image_path.endswith('.png'):
                label_path = image_path.replace(".png", ".txt")
            else:
                skipped += 1
                continue
                
            # Check if label file exists
            if not os.path.exists(label_path):
                skipped += 1
                continue  

            # Read label text
            try:
                with open(label_path, "r", encoding='utf-8') as lf:
                    label = lf.read().strip()
                
                if image_path.startswith("/mnt/d/ThucTap/OCR_Labs/Datasets/"):
                    image_path = image_path.replace("/mnt/d/ThucTap/OCR_Labs/Datasets/", "./")
                # PaddleOCR format: image_path<TAB>text
                item = f'{image_path}\t{label}\n'  
                f.write(item)
                successful += 1
                
            except Exception as e:
                print(f"\n⚠️ Error reading {label_path}: {e}")
                skipped += 1
    
    return successful, skipped

def main():
    parser = argparse.ArgumentParser(
        description='Generate PaddleOCR training label file from images and text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Example usage:
    python genarate_data_training.py -i ./images -l train_label.txt
    
    Expected structure:
    images/
        ├── img_001.jpg
        ├── img_001.txt  (contains: "xin chào")
        ├── img_002.png
        └── img_002.txt  (contains: "bệnh nhân")
            
    Output format (train_label.txt):
    images/img_001.jpg	xin chào
    images/img_002.png	bệnh nhân
    """
    )
    
    parser.add_argument('-i', '--image_dir', type=str, required=True, 
                        help='Path to image directory')
    parser.add_argument('-l', '--label_file', type=str, required=True, 
                        help='Path to output label file')

    args = parser.parse_args()
    
    image_dir = args.image_dir
    label_file = args.label_file

    # Validate input directory
    if not os.path.exists(image_dir):
        print(f"❌ Error: Directory not found: {image_dir}")
        return
    
    print("="*60)
    print("PADDLEOCR LABEL FILE GENERATOR")
    print("="*60)
    
    print(f"\n📂 Scanning images in: {image_dir}")
    image_list = read_folder(image_dir)
    print(f"✅ Found {len(image_list)} images")
    
    if len(image_list) == 0:
        print("⚠️ No images found. Exiting.")
        return
    
    print(f"\n📝 Generating label file: {label_file}")
    successful, skipped = generate_label_file(image_list, label_file)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Successfully processed: {successful}")
    print(f"⚠️ Skipped: {skipped}")
    print(f"💾 Output file: {label_file}")
    print("\n✅ Done!")

if __name__ == '__main__':
    main()