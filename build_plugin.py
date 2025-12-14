
import os
import re
import ast
import zipfile

def get_plugin_info(init_path):
    """
    Extracts version and name from __init__.py.
    """
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex for version = (x, y, z)
    version_match = re.search(r"version\s*=\s*(\([0-9,\s]+\))", content)
    if not version_match:
        raise ValueError("Could not find 'version' tuple in __init__.py")
    
    current_version_str = version_match.group(1)
    current_version = ast.literal_eval(current_version_str)
    
    # regex for name 
    # Try to find a simple string name if possible, otherwise callback to "EbookTranslator"
    name_match = re.search(r"identifier\s*=\s*['\"]([^'\"]+)['\"]", content)
    plugin_name = name_match.group(1) if name_match else "Ebook-Translator-Calibre-Plugin"
    
    # normalize name for file
    plugin_name = plugin_name.replace(' ', '_')
    
    return content, current_version, plugin_name, version_match.span(1)

def increment_version(version_tuple):
    """
    Increments the patch version (last element).
    """
    new_version = list(version_tuple)
    new_version[-1] += 1
    return tuple(new_version)

def update_init_file(init_path, content, span, new_version):
    """
    Writes the new version back to __init__.py.
    """
    start, end = span
    new_content = content[:start] + str(new_version) + content[end:]
    
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def create_zip(source_dir, output_filename, exclude_patterns):
    """
    Zips the directory with exclusions.
    """
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip exclusions
            dirs[:] = [d for d in dirs if d not in exclude_patterns and not d.startswith('.')]
            
            for file in files:
                if file == os.path.basename(output_filename):
                    continue
                if file in exclude_patterns or file.endswith('.pyc') or file.startswith('.'):
                    continue
                if file.endswith('.zip'): 
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

import sys

def main():
    # Use the script's location as the root directory anchor
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Root directory: {root_dir}")
    sys.stdout.flush()
    
    init_path = os.path.join(root_dir, '__init__.py')
    
    if not os.path.exists(init_path):
        print(f"Error: {init_path} not found.")
        sys.stdout.flush()
        return

    try:
        content, old_version, plugin_name, version_span = get_plugin_info(init_path)
        
        # Check for --no-bump flag
        no_bump = '--no-bump' in sys.argv
        
        # Check for --version flag to override
        override_version_str = None
        for i, arg in enumerate(sys.argv):
             if arg == '--version' and i + 1 < len(sys.argv):
                 override_version_str = sys.argv[i+1]
                 break

        if override_version_str:
             print(f"Build started with explicit version: {override_version_str}")
             # Convert string "x.y.z" to tuple (x, y, z)
             new_version = tuple(map(int, override_version_str.split('.')))
             
             # We must update __init__.py with this version so the file inside the zip is correct
             update_init_file(init_path, content, version_span, new_version)
             print(f"Updated __init__.py to explicit version: {new_version}")
             
        elif no_bump:
            print(f"Build started with --no-bump. Using current version: {old_version}")
            new_version = old_version
        else:
            new_version = increment_version(old_version)
            print(f"Old Version: {old_version}")
            print(f"New Version: {new_version}")
            update_init_file(init_path, content, version_span, new_version)
            print("Updated __init__.py")
        sys.stdout.flush()
        
        # Create build directory
        build_dir = os.path.join(root_dir, 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
            print(f"Created build directory: {build_dir}")

        # Format version string (e.g., 2.4.3)
        version_str = ".".join(map(str, new_version))
        # Name format: {identifier}_{version}.zip
        zip_name = f"{plugin_name}_{version_str}.zip"
        zip_path = os.path.join(build_dir, zip_name)
        
        exclusions = {
            '__pycache__', '.git', '.github', 'tests', '.gitignore', 
            'build_plugin.py', '.vscode', '.idea', 'build'
        }
        
        print(f"Creating package: {zip_path}...")
        create_zip(root_dir, zip_path, exclusions)
        print("Done!")
        
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
