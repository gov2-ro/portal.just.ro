import os
import gzip
import shutil


rootdir = 'data/cached-responses/xml'
outputdir = 'data/cached-responses/xmlgz'


def compress_xml_files(root_dir, output_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            print(filename)
            if filename.endswith(".xml"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "rb") as f_in:
                    with gzip.open(os.path.join(output_dir, filename + ".gz"), "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

compress_xml_files(rootdir, outputdir)
print('done')