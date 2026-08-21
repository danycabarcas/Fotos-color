import os
from PIL import Image

def optimize_images(input_dir, output_dir, max_size_mb=1.0, max_dim=1920, 
                    start_quality=85, watermark_path=None, watermark_position="bottom-right", 
                    watermark_opacity=0.5, progress_callback=None, log_callback=None):
    
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if log_callback: log_callback(f"Created output directory: {output_dir}")

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total_files = len(files)
    
    if total_files == 0:
        if log_callback: log_callback("No images found in the input directory.")
        if progress_callback: progress_callback(1.0)
        return

    if log_callback: log_callback(f"Starting optimization for {total_files} images...")
    
    # Load watermark if provided
    watermark = None
    if watermark_path and os.path.exists(watermark_path):
        try:
            watermark = Image.open(watermark_path).convert("RGBA")
        except Exception as e:
            if log_callback: log_callback(f"Error loading watermark: {e}")

    for i, filename in enumerate(files, 1):
        file_path = os.path.join(input_dir, filename)
        name, _ = os.path.splitext(filename)
        output_filename = name + ".jpeg"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Exif rotation handling
                try:
                    from PIL import ExifTags
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    exif = img._getexif()
                    if exif is not None and orientation in exif:
                        if exif[orientation] == 3:
                            img = img.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            img = img.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            img = img.rotate(90, expand=True)
                except Exception:
                    pass
                
                # Resize
                width, height = img.size
                if width > max_dim or height > max_dim:
                    if width > height:
                        new_width = max_dim
                        new_height = int(height * (max_dim / width))
                    else:
                        new_height = max_dim
                        new_width = int(width * (max_dim / height))
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Apply watermark
                if watermark:
                    wm_width = int(img.width * 0.2) # Watermark takes 20% of image width
                    wm_ratio = wm_width / watermark.width
                    wm_height = int(watermark.height * wm_ratio)
                    wm_resized = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
                    
                    # Apply opacity
                    if watermark_opacity < 1.0:
                        alpha = wm_resized.split()[3]
                        alpha = alpha.point(lambda p: int(p * watermark_opacity))
                        wm_resized.putalpha(alpha)
                    
                    # Position
                    if watermark_position == "bottom-right":
                        pos = (img.width - wm_width - 20, img.height - wm_height - 20)
                    elif watermark_position == "bottom-left":
                        pos = (20, img.height - wm_height - 20)
                    elif watermark_position == "top-right":
                        pos = (img.width - wm_width - 20, 20)
                    elif watermark_position == "top-left":
                        pos = (20, 20)
                    elif watermark_position == "center":
                        pos = ((img.width - wm_width) // 2, (img.height - wm_height) // 2)
                    else:
                        pos = (img.width - wm_width - 20, img.height - wm_height - 20)
                    
                    img_rgba = img.convert('RGBA')
                    img_rgba.paste(wm_resized, pos, wm_resized)
                    img = img_rgba.convert('RGB')

                # Save with quality
                quality = int(start_quality)
                img.save(output_path, "JPEG", optimize=True, quality=quality)
                
                while os.path.getsize(output_path) > max_size_bytes and quality > 10:
                    quality -= 5
                    img.save(output_path, "JPEG", optimize=True, quality=quality)
            
            final_size_kb = os.path.getsize(output_path) / 1024
            if log_callback: log_callback(f"[{i}/{total_files}] Optimized: {filename} -> {final_size_kb:.2f} KB (Q: {quality})")
            
        except Exception as e:
            if log_callback: log_callback(f"[{i}/{total_files}] Error processing {filename}: {e}")
            
        if progress_callback:
            progress_callback(i / total_files)

    if log_callback: log_callback("All images processed successfully!")
    if progress_callback: progress_callback(1.0)

