# Reference Documentation Rebuilder

This tool automates the process of "chunking" the massive `pinescriptv6reference.md` file into smaller, categorized markdown files located in `reference/functions/`. This structure is optimized for RAG (Retrieval Augmented Generation) and LLM context windows.

## Files

*   **Script:** `rebuild_reference_docs.py`
*   **Source:** `pinescriptv6reference.md` (Must exist in the project root)
*   **Target:** `reference/functions/*.md`

## Logic

The script parses `pinescriptv6reference.md` and splits it into categorized markdown files based on top-level sections (`# Section`) and function namespaces.

### Standard Sections
These sections are mapped 1-to-1 from the source file to a target file in `reference/`:

*   `# Variables` -> `reference/variables.md`
*   `# Constants` -> `reference/constants.md`
*   `# Keywords` -> `reference/keywords.md`
*   `# Types` -> `reference/types.md`
*   `# Operators` -> `reference/operators.md`
*   `# Annotations` -> `reference/annotations.md`

### Function Categories
The `# Functions` section is further processed and distributed into `reference/functions/` based on namespace prefixes:

| Category File | Namespaces / Prefixes |
| :--- | :--- |
| `collections.md` | `array.*`, `matrix.*`, `map.*` |
| `drawing.md` | `box.*`, `line.*`, `label.*`, `polyline.*`, `table.*`, `linefill.*`, `plot*`, `bgcolor`, `fill`, `hline`, `barcolor` |
| `request.md` | `request.*` |
| `strategy.md` | `strategy.*` |
| `ta.md` | `ta.*` |
| `general.md` | All other functions (e.g., `math.*`, `str.*`, `time`, `input.*`) |

## Usage

1.  Ensure you are in the root directory of the repository.
2.  Ensure `pinescriptv6reference.md` is present.
3.  Run the script using Python 3:

```bash
python3 rebuild_reference_docs.py
```

## Output

The script will overwrite the files in `reference/` and `reference/functions/` with the freshly parsed content. It will print a summary of lines written to each file.
