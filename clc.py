import csv
from math import ceil
from datetime import datetime
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
    Row1: CLC Tagnames
    Row2: Actual Tagnames
    Row3: Tag descriptions
    Row4: Engineering units
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
    """
    This function generate temp files to handle sections of large CLC files.
    """
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
    """
    This function dump to dats from temp files to output CSV file.
    """

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
    """
    This function write the output CSV file. 
    The name of the CSV file will be the name attribute of CLC file not the CLC file name.
    """
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
    main function to to call other function.
    To covert a CLC file just pass the CLC file name to this function. 
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

def get_segment(row, section_count, tags_per_section):
    split = tags_per_section * 2
    start = 1
    end = split + 1
    segment = []
    while section_count > 0:
        segment.append([row[0]] + row[start:end])
        (start,end) = (end,end+split)
        section_count -=1
    return segment

def writetempcsv(filename, line):
    with open(filename, 'a', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(line)

def generate_data_files(data, section_count,tags_per_section):
    data_files = []
    for section in range(1, section_count + 1):
        filename = 'temp' + str(section) + '.csv'
        data_files.append(filename)
    for row in data:
        segment = get_segment(row, section_count, tags_per_section)
        for filename, line in zip(data_files, segment):
            writetempcsv(filename, line)
    return data_files

def get_section2(row1, row2, row3, row4):
    section2 = []
    for mdl_tag, dcs_tag, tag_descrip, eu in zip(row1[1:], row2[1:], row3[1:], row4[1:]):
        d = '~~~'
        if mdl_tag.lower() != "quality":
            section2.append(mdl_tag + d + dcs_tag + d + tag_descrip + d + eu)
    return section2

def get_timedelta(end, start):
    
    if len(start) > 17:
        if '/' in start:
            fmt = '%m/%d/%Y %H:%M:%S' #12/16/1997 12:19:00
        elif '-' in start:
            fmt = '%m-%d-%Y %H:%M:%S' #12-16-1997 12:19:00
    elif len(start) < 17:
        if '/' in start:
            fmt = '%m/%d/%Y %H:%M' #12/16/1997 12:19
        elif '-' in start:
            fmt = '%m-%d-%Y %H:%M' #12-16-1997 12:19
    else:
        print('Invalid timestamp')
    
    deltatime = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return int(deltatime.total_seconds())


def GetCSV_data(reader, csvfilename):
    filename = csvfilename.rsplit('.')[0]
    file_descrition = 'Converted from ' + csvfilename
    row1 = next(reader)
    tag_count = int((len(row1) - 1) / 2)
    tags_per_section = 8
    section_count = ceil(tag_count/tags_per_section)
    row2 = next(reader)
    row3 = next(reader)
    row4 = next(reader)
    section2 = get_section2(row1, row2, row3, row4)
    data = list(reader)
    start_time = data[0][0]
    second_sample = data[1][0]
    sample_period = get_timedelta(second_sample, start_time)
    sample_count = len(data)
    section1 = [filename, file_descrition, tag_count, tags_per_section, start_time, sample_period, sample_count]
    return (section1, section2, section_count, data)

def write_clc(section1, section2, datafiles):
    section_break = '============================================'
    with open(section1[0]+'.clc', 'w') as wf:
        for item in section1:
            wf.write("%s\n" % item)
        wf.write("%s\n" % section_break)
        for item in section2:
            wf.write("%s\n" % item)
        for datafile in datafiles:
            wf.write("%s\n" % section_break)
            with open(datafile, 'r') as rf:
                wf.write(rf.read())
        purgefiles(datafiles)

def convertcsv(file_2_convert):
    """
    main function to to call other function.
    To covert a CSV file just pass the CSV file name and type of file to this function. 
    """
    with open(file_2_convert, newline='') as rf:
        reader = csv.reader(rf)
        section1, section2, section_count, data = GetCSV_data(reader,file_2_convert)
        data_files = generate_data_files(data, section_count,section1[3])
        write_clc(section1, section2, data_files)
    print('File', file_2_convert, 'converted')