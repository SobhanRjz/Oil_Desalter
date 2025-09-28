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

    # Copy HTML files and fix static paths
    html_src = frontend_dir / "html"
    if html_src.exists():
        for html_file in html_src.glob("*.html"):
            # Read and fix paths in HTML files
            content = html_file.read_text(encoding='utf-8')
            # Fix both ./static/ and /static/ paths to relative paths
            content = content.replace('./static/', './')
            content = content.replace('/static/', './')
            
            # Write corrected content to static directory
            output_file = static_dir / html_file.name
            output_file.write_text(content, encoding='utf-8')
            print(f"Copied and fixed paths in {html_file.name}")

    # Copy assets, css, js (these should already be there, but ensure they're up to date)
    for subdir in ["assets", "css"]:
        src_dir = frontend_dir / subdir
        dst_dir = static_dir / subdir
        if src_dir.exists():
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"Updated {subdir}/")
    
    # Copy JS files and fix navigation paths
    js_src = frontend_dir / "js"
    js_dst = static_dir / "js"
    if js_src.exists():
        if js_dst.exists():
            shutil.rmtree(js_dst)
        js_dst.mkdir(exist_ok=True)
        
        for js_file in js_src.glob("*.js"):
            # Read and fix navigation paths in JS files
            content = js_file.read_text(encoding='utf-8')
            # Fix navigation paths for GitHub Pages
            content = content.replace("window.location.href = '/login'", "window.location.href = './login.html'")
            content = content.replace("window.location.href = '/input'", "window.location.href = './input-page.html'")
            content = content.replace("window.location.href = '/results'", "window.location.href = './result.html'")
            
            # Write corrected content to static directory
            output_file = js_dst / js_file.name
            output_file.write_text(content, encoding='utf-8')
            print(f"Copied and fixed navigation in {js_file.name}")
        print(f"Updated js/")

    print("✅ Static files synced successfully!")
    print("You can now commit and push to deploy to GitHub Pages")

if __name__ == "__main__":
    sync_static()
