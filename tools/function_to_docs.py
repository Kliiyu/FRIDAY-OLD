import os
import sys

def create_markdown_from_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        return

    folder_name = os.path.basename(folder_path)
    markdown_dir = "./docs/Functions"
    markdown_file = f"{markdown_dir}/{folder_name}.md"

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

    print(f"Markdown file '{markdown_file}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python function_to_docs.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        create_markdown_from_folder(folder_path)
