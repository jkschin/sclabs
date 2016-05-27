import numpy as np
import lmdb
import os
import imghdr
from collections import defaultdict

class PrepareDataset:
    def __init__(self, directory, auto_remove):
        self.directory = directory
        self.sub_directories = self.get_sub_directories_from_main_directory(self.directory)
        self.data_statistics = defaultdict(str)
        self.auto_remove = auto_remove

    def __str__(self):
        return ("Directory: " + str(self.directory) + "\n" +
                "Sub-Directories: " + str(self.sub_directories) + "\n" +
                "Data Statistics: " + str(self.format_defaultdict(self.data_statistics)) + "\n" +
                "Auto Remove: " + str(self.auto_remove) + "\n"
                )

    def is_directory(self, path):
        return os.path.isdir(path)

    def format_defaultdict(self, defaultdict):
        output = []
        for key in defaultdict.keys():
            output.append(str(key))
            output.append(str(defaultdict[key]))
        return " ".join(output)

    def check_directory_only_contains_images(self, directory):
        print "Crawling %s" %(directory)
        counter = defaultdict(int)
        for image_name in os.listdir(directory):
            image_path = os.path.join(directory, image_name)
            file_type = imghdr.what(image_path)
            if file_type == None:
                if auto_remove:
                    os.remove(image_path)
                    print "%s is not a valid image. Removed." %(image_path)
                else:
                    print "%s is not a valid image. Remove?" %(image_path)
                    answer = str(raw_input("[y/n]?\n"))
                    if answer=="y":
                        os.remove(image_path)
                        print "%s removed." %(image_path)
                    else:
                        print "%s not removed." %(image_path)
            else:
                counter[file_type] += 1
        self.data_statistics[directory] = counter
        print "PASS ... %s directory only contains images." %(directory), self.format_defaultdict(counter)

    def get_sub_directories_from_main_directory(self, directory):
        sub_directories = []
        for sub_directory in os.listdir(directory):
            path = os.path.join(directory, sub_directory)
            if self.is_directory(path):
                sub_directories.append(sub_directory)
        sub_directories = sorted(sub_directories)
        return sub_directories

    def images_directory_check(self):
        print "Directories to crawl: ", self.sub_directories
        [self.check_directory_only_contains_images(os.path.join(self.directory,sub_directory)) for sub_directory in self.sub_directories]
        print "Images directory check completed. %s and the sub-directories are valid." %(self.directory)

# '''
# Writes out the hash map of words to indexes
# hare 1
# espresso 2
# etc.
# '''
# def create_mapping(directory):
#     mapping = open("mapping.txt", "w")
#     sub_directories = get_sub_directories_from_main_directory(directory)
#     label = 0
#     for sub_directory in sub_directories:
#         string_out = str(sub_directory) + " " + str(label) + "\n"
#         mapping.write(string_out)
#         label += 1
#     print "Mapping created."

# def create_lmdb(directory):
#     print "Preparing Data"
#     global auto_remove
#     auto_remove = input("Auto remove invalid files? (Type 'True' or 'False')\n")
#     images_directory_check(directory)
#     create_mapping(directory)

# if __name__ == "__main__":
#     create_lmdb("toy_dataset")

