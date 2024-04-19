import os, shutil
from markdown_html import markdown_to_html

def main():
    copy_static_files("./static", "./public")
    generate_pages_recursively("./content", "./template.html", "./public")

def copy_static_files(src, dest):
    if dest == "./public":
        shutil.rmtree("./public")
        print("public directory reset")
    if not os.path.exists(dest):
        os.mkdir(dest)
    static_contents = os.listdir(src)
    for item in static_contents:
        if os.path.isfile(f"{src}/{item}"):
            # copy file into public
            print(f"Copying {src}/{item} into {dest}")
            shutil.copy(f"{src}/{item}", dest)
        else:
            new_src = f"{src}/{item}"
            new_dest = f"{dest}/{item}"
            copy_static_files(new_src, new_dest)

def extract_title(markdown):
    title_position = markdown.find("# ")
    if title_position == -1:
        raise Exception("All pages need a single h1 header")
    title = ""
    for i in range(title_position + 2, len(markdown)):
        if markdown[i] == "\n":
            break
        title += markdown[i]
    return title.strip()

def generate_page(from_path, template_path, dest_path):
    try:
        print(f"Generating page from {from_path} to {dest_path} using {template_path}. . .")
        with open(from_path, encoding="utf-8") as markdown_file:
            markdown = markdown_file.read()
        with open(template_path, encoding="utf-8") as template_file:
            template = template_file.read()
        title = extract_title(markdown)
        html = markdown_to_html(markdown)
        result = template.replace("{{ Title }}", title)
        result = result.replace("{{ Content }}", html)
        new_file = open(dest_path, "w")
        new_file.write(result)
    except Exception as e:
        print(e)

def generate_pages_recursively(src, template, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    path_items = os.listdir(src)
    for item in path_items:
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            new_file = item.rstrip(".md") + ".html"
            dest_path = os.path.join(dest, new_file)
            generate_page(item_path, template, dest_path)
        else:
            updated_src = item_path
            updated_dest = os.path.join(dest, item)
            generate_pages_recursively(updated_src, template, updated_dest)

if __name__ == "__main__":
    main()