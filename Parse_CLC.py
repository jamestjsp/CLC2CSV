import csv
with open('Sample.clc', newline='') as rf:
    reader = csv.reader(rf)
    clc_filename = next(reader)[0].strip()
    clc_description = next(reader)[0]
    tag_count = int(next(reader)[0])
    tags_per_section = int(next(reader)[0])
    start_time = next(reader)[0]
    sample_period = int(next(reader)[0])
    sample_count = int(next(reader)[0])
    next(reader)
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

    with open(clc_filename+'.csv', 'w', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(model_tags)
        writer.writerow(Collect_tags)
        writer.writerow(Tag_descriptions)
        writer.writerow(Engineering_units)
        temp_files = []
        tf_count = 0

        while tags_per_section > 0:
            tf_count += 1
            temp_count = sample_count
            next(reader)
            temp_files.append('tempfile'+str(tf_count)+'.csv')

            with open('tempfile'+str(tf_count)+'.csv', 'w', newline='') as tf:
                tf_writer = csv.writer(tf)

                while temp_count > 0:
                    tf_writer.writerow(next(reader))
                    temp_count -= 1

            tags_per_section -= 1
        fs = []
        for temp_file in temp_files:
            fs.append(open(temp_file, newline=''))
        csv_objects = []
        for f in fs:
            csv_objects.append(csv.reader(f))
        while True:
            temp_line = None

            for index, csv_object in enumerate(csv_objects):
                if index == 0:
                    temp_line = next(csv_object)
                else:
                    temp_line = temp_line + next(csv_object)[1:]

            writer.writerow(temp_line)

        for f in fs:
            f.close()
