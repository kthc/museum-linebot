import os
import glob, shutil

print(os.path.dirname(__file__))

app_root_dir_path = os.path.dirname(__file__)
venv = os.path.join(app_root_dir_path, 'venv')
root_dir_path, app_root_dir = os.path.split(app_root_dir_path)
dest_dir = os.path.join(root_dir_path, f'{app_root_dir}_pack')
print(root_dir_path)
print(app_root_dir)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

to_exclude = [venv]

#ignores excluded directories and .exe files
def get_ignored(path, filenames):
    ret = []
    for filename in filenames:
        if os.path.join(path, filename) in to_exclude:
            ret.append(filename)
    return ret

shutil.copytree(app_root_dir_path , dest_dir ,ignore=get_ignored, dirs_exist_ok=True)