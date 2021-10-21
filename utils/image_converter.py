import os, random
from PIL import Image


def pgm_to_jpg(src, dest, filename):
    _, extension = os.path.splitext(os.path.basename(src))
    if extension == ".pgm":
        new_file = "{}.jpg".format(filename)
        Image.open(src).resize((100, 100)).save(dest + new_file)


def atnt_face_converter(source_path, save_path):
    src = os.getcwd() + source_path
    for folder in os.listdir(src):
        dest = "{}/{}/".format(os.getcwd() + save_path, folder[1:])
        if not os.path.exists(dest):
            os.mkdir(dest)
        for file in os.listdir(src + "/" + folder):
            source_image_path = "{}/{}/{}".format(src, folder, file)
            # filename = "{}".format(folder + str(int(file.split(".")[0]) - 1))
            filename = file.split(".")[0]
            pgm_to_jpg(source_image_path, dest, filename)

# atnt_face_converter("/data/raw", "/data/preprocessed")

def create_negative(source_path, save_path):
    src = os.getcwd() + source_path
    dest = os.getcwd() + save_path
    filename = 1

    while filename <= 200:
        src_folder = 2
        while src_folder <= 40:
            number = random.randint(1, 10)
            src_file_path = "{}/{}/{}.jpg".format(src, src_folder, number)
            dest_file_path = "{}/{}.jpg".format(dest, filename)
            Image.open(src_file_path).save(dest_file_path)
            filename += 1
            src_folder += 1
            

# create_negative("/data/preprocessed", "/data/negative")

print(os.listdir(os.getcwd() + "/data/positive"))
