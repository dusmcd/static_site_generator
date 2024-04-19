import os, shutil

def main():
    copy_static_files("./static", "./public")

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


if __name__ == "__main__":
    main()