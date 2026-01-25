import os
import shutil

PRESERVE_FILES = {
    # Backend Core
    r"backend\app.py",
    r"backend\.env",
    r"backend\requirements.txt",
    r"backend\routes\base.py",
    r"backend\routes\chat.py",
    r"backend\routes\notes.py",
    r"backend\services\ai_service.py",
    r"backend\utils\response.py",
    r"backend\test_chat.py",
    # Frontend Core
    r"frontend\index.html",
    r"frontend\script.js",
    r"frontend\style.css",
    # Project Root
    r"launch_noteship.bat",
    r"README.md",
}

PRESERVE_DIRS = {
    r"backend",
    r"backend\routes",
    r"backend\services",
    r"backend\utils",
    r"frontend",
    r".venv",
    r".git",
    r".vscode", # User option override: keep it
    
}

DELETE_FILES = [
    "NOTESHIP_FIX_REPORT.md",
    "diagnose_noteship.py",
    "diagnose_remaining.py",
    "full_codebase.md",
    "noteship_file_list.txt",
    "noteship_file_list",
    "tools.yaml",
    "run_backend_diagnostic.py",
    r"backend\verification.txt",
    r"backend\verify_api.py",
    r"backend\verify_fix_agent.py",
    r"backend\verify_length.py",
    r"backend\.env.example",
    "all_files.txt",
    "diagnostic_report.md", # Artifacts are stored in brain, this might be a local copy? Just in case.
]

ROOT_DIR = os.getcwd()

def normalize_path(path):
    return os.path.normpath(os.path.join(ROOT_DIR, path))

def is_preserved(path):
    rel_path = os.path.relpath(path, ROOT_DIR)
    
    # Check exact file matches
    if rel_path in PRESERVE_FILES:
        return True
    
    # Check if inside preserved directories (but we still want to clean garbage inside them if not essential)
    # The requirement is: "If a file is not in the list above -> classify it and delete unless it is essential."
    # But effectively we are deleting specific lists + patterns.
    
    # We always preserve .venv and .git contents implicitly
    if rel_path.startswith(".venv") or rel_path.startswith(".git") or rel_path.startswith(".vscode"):
        return True

    return False

def cleanup():
    print(f"Starting cleanup in: {ROOT_DIR}")
    
    deleted_count = 0

    # 1. Delete Specific Files
    for filename in DELETE_FILES:
        full_path = normalize_path(filename)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"[DELETED] {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR] Could not delete {filename}: {e}")
    
    # 2. Recursive Scan for Patterns (pycache, pyc, empty dirs)
    for root, dirs, files in os.walk(ROOT_DIR, topdown=False):
        # Skip .venv and .git for traversal cleanup if we want to be super safe, 
        # though topdown=False means we process children first.
        # We need to filter dirs to avoid walking into .venv
        rel_root = os.path.relpath(root, ROOT_DIR)
        if rel_root.startswith(".venv") or rel_root.startswith(".git") or rel_root.startswith(".vscode"):
             continue

        # Delete Garbage Files
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".pyc") or file == ".DS_Store" or file == "Thumbs.db":
                 try:
                    os.remove(file_path)
                    print(f"[DELETED artifact] {os.path.relpath(file_path, ROOT_DIR)}")
                    deleted_count +=1
                 except Exception as e:
                    print(f"[ERROR] {e}")

        # Delete Garbage Directories
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"[DELETED dir] {os.path.relpath(pycache_path, ROOT_DIR)}")
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR] {e}")

    # 3. Remove Empty Directories (careful not to remove core structure)
    # We walk again bottom-up
    for root, dirs, files in os.walk(ROOT_DIR, topdown=False):
        rel_root = os.path.relpath(root, ROOT_DIR)
        if rel_root == ".": continue
        if rel_root.startswith(".venv") or rel_root.startswith(".git") or rel_root.startswith(".vscode"): continue
        
        # Don't delete preserved struct dirs even if empty (unlikely given app.py etc)
        if rel_root in PRESERVE_DIRS:
            continue

        if not os.listdir(root): # Is empty
            try:
                os.rmdir(root)
                print(f"[DELETED empty dir] {rel_root}")
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR] {e}")

    print(f"Cleanup complete. Removed {deleted_count} items.")

if __name__ == "__main__":
    cleanup()
