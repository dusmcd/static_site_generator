import os, shutil
from markdown_html import markdown_to_html

def main():
    copy_static_files("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

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
        print("Invalid markdown")
        print(e)

if __name__ == "__main__":
    main()