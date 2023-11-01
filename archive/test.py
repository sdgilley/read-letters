# testing snippets here
img_path = "C:\\Git\\read-letters-data\\letters"
print("START")
import os
# find the file names from the local repo.
for path,dirs,files in os.walk(img_path):
    for file in files: 
        # read_image_path = os.path.join(path,file)
        parts = file.split('.')
        print(parts)
        fn = parts[0]
        write_fn = os.path.join(path,f"{fn}.txt")
        print(write_fn)