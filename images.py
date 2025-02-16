import os
import re
import shutil
import filecmp

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\curra\OneDrive\Documents\My Website\Curran Hill\content\posts"
attachments_dir = r"C:\Users\curra\OneDrive\Documents\Obsidian Vault\Attachments"
static_images_dir = r"C:\Users\curra\OneDrive\Documents\My Website\Curran Hill\static\images"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"Processing file: {filepath}")
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        print(f"Found images: {images}")
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"![[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            image_destination = os.path.join(static_images_dir, image)
            if os.path.exists(image_source):
                print(f"Copying {image_source} to {image_destination}")
                shutil.copy(image_source, image_destination)
                if os.path.exists(image_destination):
                    print(f"Successfully copied {image_source} to {image_destination}")
                    # Verify file integrity
                    if filecmp.cmp(image_source, image_destination, shallow=False):
                        print(f"File integrity verified for {image_source}")
                    else:
                        print(f"File integrity check failed for {image_source}")
                else:
                    print(f"Failed to copy {image_source} to {image_destination}")
            else:
                print(f"Image not found: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")