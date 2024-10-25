import os
import sys

def create_markdown_from_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        return

    folder_name = os.path.basename(folder_path)
    markdown_dir = "./docs/Functions"
    markdown_file = f"{markdown_dir}/{folder_name}.md"
    yml_file = "mkdocs.yml"
    yml_entry = f"    - Functions/{folder_name}.md\n"

    # Ensure the directory exists
    if not os.path.exists(markdown_dir):
        os.makedirs(markdown_dir)
        print(f"Directory '{markdown_dir}' created.")

    try:
        with open(markdown_file, 'w') as md_file:
            md_file.write(f"# {folder_name}\n\n")
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    md_file.write(f"- {file_path}\n")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        return

    print(f"Markdown file '{markdown_file}' created successfully.")

    # Check if entry is already in mkdocs.yml
    try:
        with open(yml_file, 'r') as yml:
            if yml_entry in yml.readlines():
                print(f"Entry 'Functions/{folder_name}.md' already exists in '{yml_file}'.")
                return
    except IOError as e:
        print(f"An error occurred while reading '{yml_file}': {e}")
        return

    # Append the entry to mkdocs.yml if it does not already exist
    try:
        with open(yml_file, 'a') as yml:
            yml.write(yml_entry)
        print(f"Added 'Functions/{folder_name}.md' to '{yml_file}' under Functions section.")
    except IOError as e:
        print(f"An error occurred while updating '{yml_file}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python function_to_docs.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        create_markdown_from_folder(folder_path)
