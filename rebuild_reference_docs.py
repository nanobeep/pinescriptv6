import os
import re

def main():
    """
    Parses the Pine Script reference source and distributes documentation
    into categorized markdown files in 'reference/'.
    """
    source_candidates = [
        "pinescriptv6_complete_reference.md",
        "pinescriptv6reference.md",
    ]
    source_file = next((p for p in source_candidates if os.path.exists(p)), None)

    if not source_file:
        print("Error: No source reference file found. Expected one of:", source_candidates)
        return

    base_output_dir = "reference"
    functions_output_dir = os.path.join(base_output_dir, "functions")
    
    # Ensure output directories exist
    if not os.path.exists(functions_output_dir):
        os.makedirs(functions_output_dir)

    # 1. Define Standard Sections (Simple 1-to-1 mapping)
    #    Maps the Header found in the source file to the output filename.
    standard_sections = {
        "# Variables": "variables.md",
        "# Constants": "constants.md",
        "# Keywords": "keywords.md",
        "# Types": "types.md",
        "# Operators": "operators.md",
        "# Annotations": "annotations.md"
    }

    # 2. Define Function Categories (for the # Functions section)
    #    Maps namespaces/prefixes to specific function files.
    function_categories = {
        "collections.md": ["array", "matrix", "map"],
        "drawing.md": ["box", "line", "label", "polyline", "table", "linefill", 
                       "plot", "bgcolor", "fill", "hline", "barcolor"],
        "request.md": ["request"],
        "strategy.md": ["strategy"],
        "ta.md": ["ta"]
    }
    
    # Initialize buffers
    # Standard buffers
    buffers = {filename: [] for filename in standard_sections.values()}
    
    # Function buffers
    function_buffers = {
        "collections.md": [],
        "drawing.md": [],
        "request.md": [],
        "strategy.md": [],
        "ta.md": [],
        "general.md": []
    }

    current_section = None
    current_function_category = "general.md" # Default for functions

    try:
        with open(source_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
        return

    print(f"Parsing '{source_file}'...")

    for line in lines:
        stripped_line = line.strip()

        # 1. Check for Top-Level Sections
        if line.startswith("# ") and not line.startswith("## "):
            # Identify which section we are entering
            found_section = False
            
            # Check against standard sections
            for header, filename in standard_sections.items():
                if stripped_line.startswith(header): # Use startswith to handle trailing spaces
                    current_section = filename
                    found_section = True
                    # Add the header to the file?
                    # The previous script didn't, but usually it's good practice.
                    # However, looking at the previous script, it filtered strictly.
                    # Let's include the header in the standard files for clarity.
                    buffers[filename].append(line)
                    break
            
            # Check if it's the Functions section
            if not found_section and stripped_line == "# Functions":
                current_section = "FUNCTIONS_MODE"
                found_section = True
            
            # If it's a known section, we are done with this line
            if found_section:
                continue
            # If it's an unknown top-level section (e.g. title), ignore or handle appropriately.
            # The first line is "# Pine Script® language reference manual", we can probably ignore it or put it in a README?
            # For now, if we are not in a known section, we ignore.
            if not current_section:
                continue

        # 2. Process Content based on Current Section
        if current_section == "FUNCTIONS_MODE":
            # -- Function Categorization Logic --
            
            # Detect new function definition to switch category
            if line.startswith("## "):
                # Extract function name: "## ta.rsi()" -> "ta.rsi"
                # Remove '## ' and parameters
                func_name_chunk = line.strip()[3:].split('(')[0] 
                # Remove generic type like array.new<type>
                func_name = func_name_chunk.split('<')[0]
                
                # Determine Category
                found_cat = "general.md"
                for cat, prefixes in function_categories.items():
                    for prefix in prefixes:
                        if func_name == prefix or func_name.startswith(prefix + "."):
                            found_cat = cat
                            break
                    if found_cat != "general.md":
                        break
                current_function_category = found_cat
            
            # Append line to the active function buffer
            if current_function_category:
                function_buffers[current_function_category].append(line)

        elif current_section in buffers:
            # -- Standard Section Logic --
            # Just append to the mapped file
            buffers[current_section].append(line)

    # 3. Write All Files
    
    # Write Standard Sections
    for filename, content in buffers.items():
        path = os.path.join(base_output_dir, filename)
        if content:
            print(f"Writing {len(content)} lines to {path}")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(content)
        else:
            print(f"Warning: No content found for {filename}")

    # Write Function Sections
    for filename, content in function_buffers.items():
        path = os.path.join(functions_output_dir, filename)
        if content:
            print(f"Writing {len(content)} lines to {path}")
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(content)
        else:
            print(f"Warning: No content found for {filename}")

    print("Rebuild complete.")

if __name__ == "__main__":
    main()
