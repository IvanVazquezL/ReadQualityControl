from collections import Counter
import gzip


def get_data_from_file(file_name):
    data = dict()
    repeats = dict()
    data['reads_data'] = dict()
    data['repeats_number'] = 0
    data['reads_with_n'] = 0

    with gzip.open(file_name, 'rt') as my_file:  # Open the file in read mode using a context manager
        reads_count = 0
        is_read_length_line = False
        sum_average = 0
        sum_average_ns = 0
        read_start = 0
        counter = 0

        for line in my_file:  # Iterate over each line in the file
            if read_start == counter:
                reads_count += 1
                is_read_length_line = True
                read_start += 4
            elif is_read_length_line:
                if line not in repeats:
                    repeats[line] = 0
                else:
                    data['repeats_number'] += 1

                clean_line = line.replace("\n", "")
                if len(clean_line) in data['reads_data']:
                    data['reads_data'][len(clean_line)] += 1
                else:
                    data['reads_data'][len(clean_line)] = 1
                is_read_length_line = False

                char_count = Counter(line)
                sum_average += round((char_count['G'] + char_count['C']) / len(clean_line), 5)
                sum_average_ns += round(char_count['N'] / len(clean_line), 5)
                data['reads_with_n'] += 1 if char_count['N'] > 0 else 0

            counter += 1

    data['reads_count'] = reads_count
    data['gc_average'] = 0 if reads_count == 0 else round((sum_average / reads_count) * 100, 2)
    data['ns_average'] = 0 if reads_count == 0 else round((sum_average_ns / reads_count) * 100, 2)
    return data


def print_data(data):
    print(f"Reads in the file = {data['reads_count']}:")

    sorted_reads_data = dict(sorted(data['reads_data'].items()))
    sum_length = 0
    for key, value in sorted_reads_data.items():
        sum_length += key * value

    average = 0 if data['reads_count'] == 0 else round(sum_length / data['reads_count'])
    print(f"Reads sequence average length = {average}")

    print(f"\nRepeats = {data['repeats_number']}")
    print(f"Reads with Ns = {data['reads_with_n']}")

    print(f"\nGC content average = {data['gc_average']}%")
    print(f"Ns per read sequence = {data['ns_average']}%")


def main():
    best_data = dict()

    for i in range(3):
        file_name = input()
        data = get_data_from_file(file_name)

        if i == 0:
            best_data = data
        elif (data['reads_with_n'] <= best_data['reads_with_n'] and
              data['repeats_number'] <= best_data['repeats_number']):
            best_data = data

    print_data(best_data)


if __name__ == '__main__':
    main()
