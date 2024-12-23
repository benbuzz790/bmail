#start.py
from bots.dev import project_tree
import os
import sys

def cleanup_directory(script_path, extensions=('.txt', '.bot', '.py', '.md'), dry_run=True, recursive=True):
    """
    Deletes specific file types and empty directories in the script directory and its subdirectories,
    except the script itself.
    
    Args:
        script_path: Path to the current script
        extensions: Tuple of file extensions to delete (including the dot)
        dry_run: If True, only prints what would be deleted without actually deleting
        recursive: If True, also process subdirectories
    
    Returns:
        tuple: (list of deleted files, list of deleted directories)
    """
    base_directory = os.path.dirname(os.path.abspath(script_path))
    script_name = os.path.basename(script_path)
    
    deleted_files = []
    deleted_dirs = []
    
    print(f"Cleaning directory: {base_directory}")
    print(f"Looking for files with extensions: {', '.join(extensions)}")
    print(f"Preserving script: {script_name}")
    print(f"Recursive mode: {'enabled' if recursive else 'disabled'}")
    
    def process_directory(directory):
        """Returns True if directory is empty after processing"""
        is_empty = True
        
        # Use list to avoid modification during iteration
        for entry in list(os.scandir(directory)):
            if entry.is_file():
                # Skip the script itself
                allow_list = ['example.py']
                if entry.name == script_name and entry.path == os.path.join(base_directory, script_name) or (entry.name in allow_list):
                    is_empty = False
                    continue
                    
                # Delete matching files
                if entry.name.lower().endswith(extensions):
                    if dry_run:
                        print(f"Would delete file: {entry.path}")
                    else:
                        try:
                            os.remove(entry.path)
                            deleted_files.append(entry.path)
                            print(f"Deleted file: {entry.path}")
                        except Exception as e:
                            print(f"Error deleting file {entry.path}: {e}")
                            is_empty = False
                else:
                    is_empty = False
            
            elif entry.is_dir() and recursive:
                # Process subdirectory and check if it became empty
                subdir_empty = process_directory(entry.path)
                if subdir_empty:
                    if dry_run:
                        print(f"Would delete directory: {entry.path}")
                    else:
                        try:
                            os.rmdir(entry.path)
                            deleted_dirs.append(entry.path)
                            print(f"Deleted directory: {entry.path}")
                        except Exception as e:
                            print(f"Error deleting directory {entry.path}: {e}")
                            is_empty = False
                else:
                    is_empty = False
        
        return is_empty
    
    # Start the cleanup process
    process_directory(base_directory)
    
    return deleted_files, deleted_dirs

if __name__ == "__main__":
    # Add command line arguments for recursive mode
    recursive = True  # Default to recursive
    if len(sys.argv) > 1 and sys.argv[1].lower() in ('--no-recursive', '-nr'):
        recursive = False
    
    # First run in dry_run mode to show what would be deleted
    print("DRY RUN - No files or directories will be deleted:")
    deleted_files, deleted_dirs = cleanup_directory(__file__, 
                                                  extensions=('.txt', '.bot', '.py'), 
                                                  dry_run=True, 
                                                  recursive=recursive)
    
    # Ask for confirmation before actual deletion
    response = input("\nDo you want to proceed with deletion? (yes/no): ")
    if response.lower() == 'yes':
        print("\nDeleting files and directories:")
        deleted_files, deleted_dirs = cleanup_directory(__file__, 
                                                      extensions=('.txt', '.bot', '.py', '.md'), 
                                                      dry_run=False, 
                                                      recursive=recursive)
        print(f"\nSuccessfully deleted {len(deleted_files)} files and {len(deleted_dirs)} directories")
    else:
        print("Operation cancelled")
    
    project_tree.main()