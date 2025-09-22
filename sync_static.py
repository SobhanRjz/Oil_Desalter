#!/usr/bin/env python3
"""
Sync script to copy frontend files to static folder for GitHub Pages deployment.
Run this after making changes to HTML files in frontend/html/
"""

import shutil
import os
from pathlib import Path

def sync_static():
    """Sync frontend files to static folder"""
    frontend_dir = Path("frontend")
    static_dir = Path("static")

    # Ensure static directory exists
    static_dir.mkdir(exist_ok=True)

    # Copy HTML files
    html_src = frontend_dir / "html"
    if html_src.exists():
        for html_file in html_src.glob("*.html"):
            shutil.copy2(html_file, static_dir / html_file.name)
            print(f"Copied {html_file.name}")

    # Copy assets, css, js (these should already be there, but ensure they're up to date)
    for subdir in ["assets", "css", "js"]:
        src_dir = frontend_dir / subdir
        dst_dir = static_dir / subdir
        if src_dir.exists():
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"Updated {subdir}/")

    print("✅ Static files synced successfully!")
    print("You can now commit and push to deploy to GitHub Pages")

if __name__ == "__main__":
    sync_static()
