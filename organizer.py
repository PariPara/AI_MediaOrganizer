import os
import shutil
import cv2
import fitz
import ollama
import argparse
import csv
import re
from datetime import datetime
from pydantic import BaseModel, Field
from PIL import Image

# 1. Improved Schema with constraints
class FileAnalysis(BaseModel):
    # Constraint: Ask for a short name, max 40 chars
    suggested_filename: str = Field(..., max_length=40)
    # Ensure category is descriptive (not just "folder")
    category: str = Field(..., description="A one-word category like Finance, Gaming, Art, etc.")

def get_ai_analysis(file_path, model_name):
    temp_image = "temp_fast_preview.jpg"
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        # --- VIDEO EXTRACTION ---
        if ext in ['.mp4', '.mov', '.avi']:
            cap = cv2.VideoCapture(file_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                success, frame = cap.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                cv2.imwrite(temp_image, frame)
            cap.release()
        
        # --- PDF EXTRACTION ---
        elif ext == '.pdf':
            doc = fitz.open(file_path)
            pix = doc.load_page(0).get_pixmap()
            pix.save(temp_image)
            doc.close()
            
        # --- IMAGE EXTRACTION (with RGBA fix) ---
        else:
            with Image.open(file_path) as img:
                img = img.convert("RGBA")
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                bg.thumbnail((768, 768))
                bg.save(temp_image, "JPEG")

        # --- AI CALL ---
        response = ollama.chat(
            model=model_name,
            format=FileAnalysis.model_json_schema(),
            messages=[{
                'role': 'user', 
                'content': "Analyze this file. Give me a 2-3 word descriptive filename and a broad category.",
                'images': [temp_image]
            }]
        )
        return FileAnalysis.model_validate_json(response['message']['content'])
    finally:
        if os.path.exists(temp_image): os.remove(temp_image)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Source folder")
    parser.add_argument("--live", action="store_true", help="Execute changes")
    parser.add_argument("--folder", action="store_true", help="Organize into category folders")
    parser.add_argument("--model", default="moondream", help="Ollama model")
    args = parser.parse_args()

    dir_path = os.path.abspath(os.path.expanduser(args.directory))
    backup_dir = os.path.join(dir_path, "original_backups")
    
    if args.live and not os.path.exists(backup_dir): os.makedirs(backup_dir)

    valid_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.mp4', '.mov')
    
    print(f"--- Running {'LIVE' if args.live else 'DRY RUN'} ---")

    for filename in os.listdir(dir_path):
        if filename.startswith('.') or filename in ["original_backups", "rename_log.csv"]:
            continue
        
        if filename.lower().endswith(valid_exts):
            old_path = os.path.join(dir_path, filename)
            
            try:
                analysis = get_ai_analysis(old_path, args.model)
                
                # SANITIZE FILENAME
                clean_name = analysis.suggested_filename.strip().lower().replace(" ", "_")
                clean_name = re.sub(r'[^\w\-]', '', clean_name) # Remove special chars like ? or :
                clean_name = clean_name[:40] # Force 40 character limit
                
                ext = os.path.splitext(filename)[1]
                new_filename = f"{clean_name}{ext}"
                
                # CATEGORY LOGIC
                category = analysis.category.strip().capitalize()
                # Safety: If AI just says "Folder" or "None", put it in "Uncategorized"
                if category.lower() in ["folder", "none", "file"]:
                    category = "Uncategorized"

                if args.folder:
                    target_dir = os.path.join(dir_path, category)
                else:
                    target_dir = dir_path

                if args.live:
                    if args.folder: os.makedirs(target_dir, exist_ok=True)
                    shutil.copy2(old_path, os.path.join(backup_dir, filename))
                    shutil.move(old_path, os.path.join(target_dir, new_filename))
                    print(f"[OK] {filename} -> {category if args.folder else ''}/{new_filename}")
                else:
                    print(f"[DRY] {filename} -> {category if args.folder else 'ROOT'}/{new_filename}")

            except Exception as e:
                print(f"[ERR] {filename}: {e}")

if __name__ == "__main__":
    main()
