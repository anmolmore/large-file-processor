import multiprocessing as mp
import os
import time

import db_processor


def serial_ingestion(file_name):
    """
    Read file line by line and insert into db
    :param file_name:
    :return:
    """
    start_time = time.time()
    results = []
    with open(file_name, 'r') as f:
        for line in f:
            results.append(process_item(line))
    print("--- %s seconds ---" % (time.time() - start_time))


def parallel_ingestion(file_name):
    """
    Read file in chunks and insert in DB
    :param file_name: Name of file to be ingested
    :return:
    """
    # Check max available CPU in current system
    cpu_count = mp.cpu_count()

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count

    # Arguments for each chunk (eg. [('input.txt', 0, 32), ('input.txt', 32, 64)])
    chunk_args = []
    with open(file_name, 'r') as f:
        def is_start_of_line(position):
            if position == 0:
                return True
            # Check whether the previous character is EOL
            f.seek(position - 1)
            return f.read(1) == '\n'

        def get_next_line_position(position):
            # Read the current line till the end
            f.seek(position)
            f.readline()
            # Return a position after reading the line
            return f.tell()

        chunk_start = 0
        # Iterate over all chunks and construct arguments for `process_chunk`
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            # Make sure the chunk ends at the beginning of the next line
            while not is_start_of_line(chunk_end):
                chunk_end -= 1

            # Handle the case when a line is too long to fit the chunk size
            if chunk_start == chunk_end:
                chunk_end = get_next_line_position(chunk_end)

            # Save `process_chunk` arguments
            args = (file_name, chunk_start, chunk_end)
            chunk_args.append(args)

            # Move to the next chunk
            chunk_start = chunk_end

    with mp.Pool(cpu_count) as p:
        # Run chunks in parallel
        # print(chunk_args)
        chunk_results = p.starmap(process_chunk, chunk_args)

    results = []
    # Combine chunk results into `results`
    for chunk_result in chunk_results:
        for result in chunk_result:
            results.append(result)
    return results


def process_chunk(file_name, chunk_start, chunk_end):
    """
    Process given chunk of file
    :param file_name: name of file to process
    :param chunk_start: starting line to read from
    :param chunk_end: ending line number
    :return:
    """
    chunk_results = []
    with open(file_name, 'r') as f:
        # Moving stream position to `chunk_start`
        f.seek(chunk_start)

        # Read and process lines until `chunk_end`
        for line in f:
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            chunk_results.append(process_item(line))
    return chunk_results


def process_item(line):
    """
    insert record in DB
    :param line:
    :return:
    """
    items = line.split(',')
    if len(items) > 2:
        db_processor.insert_catalog((items[1], items[0], items[2]))
    else:
        db_processor.log_error(line)


if __name__ == "__main__":
    # file structure name, sku, description

    # start_time = time.time()
    # serial_ingestion('Zluri_Assignment_Dataset')
    # print("Serial process --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    parallel_ingestion('Zluri_Assignment_Dataset')
    print("--- DB insert with parallel processing completed in %s seconds ---" % (time.time() - start_time))

    # print(db_processor.get_count_by_name())
