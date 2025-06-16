import os
import shutil
import frontmatter

# Directories are set relative to the root of the repository
# 'private_vault' is where the GitHub Action will clone your private notes
# 'content' is the standard Quartz content folder
SOURCE_DIR = 'private_vault'
DEST_DIR = 'content'

def sync_notes():
    """
    Copies published markdown files and all other assets from the
    source directory to the destination directory.
    """
    # Ensure the destination directory exists and is empty
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

    print(f"Starting sync from '{SOURCE_DIR}' to '{DEST_DIR}'...")

    # Walk through the source directory
    for root, _, files in os.walk(SOURCE_DIR):
        # Exclude git history from the sync
        if '.git' in root:
            continue

        # Determine the corresponding destination directory
        relative_path = os.path.relpath(root, SOURCE_DIR)
        dest_root = os.path.join(DEST_DIR, relative_path)

        # Create destination subdirectories if they don't exist
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)

        for file in files:
            source_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_root, file)

            if file.endswith('.md'):
                try:
                    with open(source_file_path, 'r', encoding='utf-8') as f:
                        # Load the file's front matter
                        post = frontmatter.load(f)
                        # Check for 'publish: true'
                        if post.get('publish') is True:
                            shutil.copy2(source_file_path, dest_file_path)
                            print(f"Copied published note: {relative_path}/{file}")
                        else:
                            print(f"Skipped private note: {relative_path}/{file}")
                except Exception as e:
                    print(f"Could not process {source_file_path}: {e}")
            else:
                # Copy all non-markdown files (e.g., images, PDFs)
                shutil.copy2(source_file_path, dest_file_path)
                print(f"Copied asset: {relative_path}/{file}")

    print("Sync complete. Only published notes and assets have been copied.")

if __name__ == "__main__":
    sync_notes()
