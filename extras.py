def fix_file(source_file, destination_file):
    start_delimiter = '::'
    end_delimiter = ';;'
    start, end = None, None
    with open(source_file) as fr:
        with open(destination_file, 'w') as fw:
            for line in fr:
                if not start:
                    start = line.rfind(start_delimiter)
                end = line.rfind(end_delimiter)
                if end != -1:



