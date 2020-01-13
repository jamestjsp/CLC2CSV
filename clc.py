import csv
from math import ceil
import os


def purgefiles(temp_files):
    """
    Helper function to remove temp files from folder by passing a list of files
    """
    for temp_file in temp_files:
        os.remove(temp_file)


def GetFileMetaData(reader):
    """
    This funtion return a tuple of meta data in the following order
    1. clc_filename
    2. clc_description
    3. tag_count
    4. tags_per_section
    5. start_time
    6. sample_period
    7. sample_count
    8. tag_dat_sec_count
    """
    clc_filename = next(reader)[0].strip()
    clc_description = next(reader)[0]
    tag_count = int(next(reader)[0])
    tags_per_section = int(next(reader)[0])
    start_time = next(reader)[0]
    sample_period = int(next(reader)[0])
    sample_count = int(next(reader)[0])
    tag_dat_sec_count = ceil(tag_count/tags_per_section)
    next(reader)
    return(clc_filename, clc_description, tag_count, tags_per_section, start_time, sample_period, sample_count, tag_dat_sec_count)


def CreateCSVHeader(reader, tag_count):
    """
    This function return a tuple of list used of CSV header.
    """
    model_tags = ["Time", ]
    Collect_tags = ["", ]
    Tag_descriptions = ["", ]
    Engineering_units = ["", ]

    while tag_count > 0:
        line = next(reader)[0]
        tag_atributes = line.split("~~~")
        model_tags.append(tag_atributes[0])
        model_tags.append("Quality")
        Collect_tags.append(tag_atributes[1])
        Collect_tags.append('')
        Tag_descriptions.append(tag_atributes[2])
        Tag_descriptions.append('')
        Engineering_units.append(tag_atributes[3])
        Engineering_units.append('')
        tag_count -= 1
    return(model_tags, Collect_tags, Tag_descriptions, Engineering_units)


def GenerateTempFile(reader, sample_count, tag_dat_sec_count):
    temp_files = []
    tf_count = 0
    temp_tag_sec_cunt = tag_dat_sec_count

    while temp_tag_sec_cunt > 0:
        tf_count += 1
        temp_count = sample_count
        next(reader)
        temp_files.append('tempfile'+str(tf_count)+'.csv')
        with open('tempfile'+str(tf_count)+'.csv', 'w', newline='') as tf:
            tf_writer = csv.writer(tf)
            while temp_count > 0:
                tf_writer.writerow(next(reader))
                temp_count -= 1
        temp_tag_sec_cunt -= 1
    return(temp_files)


def DumpData(temp_files, writer, sample_count):

    fs = []
    for temp_file in temp_files:
        fs.append(open(temp_file, newline=''))

    csv_objects = []
    for f in fs:
        csv_objects.append(csv.reader(f))

    temp_count = sample_count
    while temp_count > 0:
        temp_line = None

        for index, csv_object in enumerate(csv_objects):

            if index == 0:
                temp_line = next(csv_object)

            else:
                temp_line = temp_line + next(csv_object)[1:]

        writer.writerow(temp_line)
        temp_count -= 1

    for f in fs:
        f.close()


def WriteCSVFile(clc_filename, sample_count, csv_header, temp_files):
    model_tags = csv_header[0]
    Collect_tags = csv_header[1]
    Tag_descriptions = csv_header[2]
    Engineering_units = csv_header[3]
    with open(clc_filename+'.csv', 'w', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(model_tags)
        writer.writerow(Collect_tags)
        writer.writerow(Tag_descriptions)
        writer.writerow(Engineering_units)
        DumpData(temp_files, writer, sample_count)
    purgefiles(temp_files)


def convertclc(file_2_convert):
    """
    function to read CSV file in a context manger 
    """
    with open(file_2_convert, newline='') as rf:
        reader = csv.reader(rf)
        metadata = GetFileMetaData(reader)
        clc_filename = metadata[0]
        tag_count = metadata[2]
        sample_count = metadata[6]
        tag_dat_sec_count = metadata[7]
        csv_header = CreateCSVHeader(reader, tag_count)
        temp_files = GenerateTempFile(reader, sample_count, tag_dat_sec_count)
        WriteCSVFile(clc_filename, sample_count, csv_header, temp_files)
    print('File', file_2_convert, 'converted')
