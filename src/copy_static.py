import os
import shutil


def copy_static():
    def cp_recur(src, dest):
        if os.path.isfile(src):
            print(f'copying "{src}" to "{dest}"')
            shutil.copy(src, dest)
            return

        print(f"creating directory {dest}")
        os.mkdir(dest)

        for entry in os.listdir(src):
            cp_recur(os.path.join(src, entry), os.path.join(dest, entry))

    if not os.path.exists("static/"):
        raise Exception('directory "static/" does not exist')

    if os.path.exists("public/"):
        print('deleting "public/"')
        shutil.rmtree("public/")

    cp_recur("static/", "public/")
