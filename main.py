from collections import Counter
import math


def get_data_from_file(file_name):
    data = dict()
    data['reads_data'] = dict()

    with open(file_name, 'r') as my_file:  # Open the file in read mode using a context manager
        reads_count = 0
        is_read_length_line = False
        sum_average = 0

        for line in my_file:  # Iterate over each line in the file
            if line.startswith('@SRR'):
                reads_count += 1
                is_read_length_line = True
            elif is_read_length_line:
                clean_line = line.replace("\n", "")
                if len(clean_line) in data['reads_data']:
                    data['reads_data'][len(clean_line)] += 1
                else:
                    data['reads_data'][len(clean_line)] = 1
                is_read_length_line = False

                char_count = Counter(line)
                sum_average += round((char_count['G'] + char_count['C']) / len(clean_line),4)

    data['reads_count'] = reads_count
    data['gc_average'] = round((sum_average / reads_count) * 100,2)
    return data


def print_data(data):
    print(f"Reads in the file = {data['reads_count']}:")

    sorted_reads_data = dict(sorted(data['reads_data'].items()))
    sum_length = 0
    for key, value in sorted_reads_data.items():
        sum_length += key * value

    average = round(sum_length / data['reads_count'])
    print(f"Reads sequence average length = {average}")

    print(f"\nGC content average = {data['gc_average']}%")


def main():
    file_name = input()
    data = get_data_from_file(file_name)
    print_data(data)


if __name__ == '__main__':
    main()
