if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import os
import inspect
from letterboxdpy import user, movie, films, members, search

def get_defined_functions(module):
    """Returns a list of function names defined in the given module."""
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and inspect.getmodule(obj) == module:
            functions.append(name)
    return functions

def get_existing_md_files(directory):
    """Returns a list of .md files in the given directory without extension."""
    md_files = [f[:-3] for f in os.listdir(directory) if f.endswith('.md')]
    return md_files

def check_missing_md_files(functions, md_files):
    """Compares functions and .md files, returning functions without corresponding .md files."""
    missing_md = [func for func in functions if func not in md_files]
    return missing_md

def create_md_file_for_missing_function(func_name, module, directory):
    """Creates a .md file for a missing function with its signature."""
    file_path = os.path.join(directory, f"{func_name}.md")
    func = getattr(module, func_name)

    signature = str(inspect.signature(func))
    docstring = inspect.getdoc(func) or "No documentation provided."
    
    with open(file_path, 'w') as file:
        file.write(f'<h2 id="{func_name}">{func_name}{signature}</h2>\n\n')
        file.write(f'**Documentation:**\n\n{docstring}\n\n')
        file.write(f'[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+{func_name})\n')

def check_modules_for_missing_md(modules):
    """Checks each module for missing .md files and prints the results."""
    base_directory = "."
    for module_name, module in modules.items():
        print(f"{module_name}:")
        function_names = get_defined_functions(module)
        md_directory = os.path.join(base_directory, module_name, 'funcs')
        
        if not os.path.exists(md_directory):
            print(f"Directory {md_directory} does not exist. Creating...")
            os.makedirs(md_directory, exist_ok=True)
        
        md_files = get_existing_md_files(md_directory)
        missing_md_files = check_missing_md_files(function_names, md_files)
        
        for func in missing_md_files:
            create_md_file_for_missing_function(func, module, md_directory)
            print(f"✗ {func}.md missing and created.")
        
        for func in function_names:
            if func in md_files:
                print(f"✓ {func}.md exists")
        
        if not missing_md_files:
            print("All functions have corresponding .md files.")
        print()

if __name__ == "__main__":
    modules = {
        'user': user,
        'movie': movie,
        'films': films,
        'members': members,
        'search': search
    }
    check_modules_for_missing_md(modules)
