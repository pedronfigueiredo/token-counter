#!/usr/bin/env python3
import os

def prepare_repository():
    """
    Walks through a repository at `repo_path`, creating (or overwriting)
    a text file at `output_file` that contains the paths and contents of
    all included files (excluding binary files, images, and .git).
    """

    # Hardcoded repository path
    repo_path = "/app/metamask-extension"
    
    # Check if the repository exists; if not, print a message and exit.
    if not os.path.isdir(repo_path):
        print(f"Repository not found: {repo_path}")
        return
    
    # Hardcoded output file name
    output_file = "context.txt"

    # Set of directories to exclude from processing
    excluded_dirs = {'.git', 'node_modules', 'coverage', '.nyc_output', 'storybook-build', 'dist', '.yarn', 'mock-cdn'}

    # Set of files to exclude from processing
    excluded_files = {'.DS_Store'}
    
    # Image extensions to skip
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.tiff', '.webm', '.wasm', '.zip', '.ttf', '.eot', '.woff', '.woff2'}

    # Size limit to skip very large files (e.g., 100 MB)
    size_limit_bytes = 100 * 1024 * 1024

    # Remove the file if it exists (to fully clear before rewriting)
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w', encoding='utf-8') as out:
        for root, dirs, files in os.walk(repo_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file_name in files:
                # Basic exclusions by file name
                if file_name in excluded_files:
                    continue

                # Exclude images by checking the file extension
                ext = os.path.splitext(file_name)[1].lower()
                if ext in image_extensions:
                    continue

                file_path = os.path.join(root, file_name)
                
                # Skip files that exceed the size limit
                if os.path.getsize(file_path) > size_limit_bytes:
                    continue

                # Attempt to read the file as text; skip if it fails
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                except Exception:
                    continue

                out.write(f"===== FILE: {os.path.relpath(file_path, repo_path)} =====\n")
                out.write(file_content)
                out.write("\n\n")

    print(f"Repository prepared. Output written to: {output_file}")


def main():
    prepare_repository()

if __name__ == "__main__":
    main() 