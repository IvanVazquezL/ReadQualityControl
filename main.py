import math


def print_data_from_file(file_name):
    reads_data = dict()

    with open(file_name, 'r') as my_file:  # Open the file in read mode using a context manager
        reads_count = 0  # Initialize a counter variable to keep track of the number of lines printed
        is_read_length_line = False

        for line in my_file:  # Iterate over each line in the file
            if line.startswith('@SRR'):
                reads_count += 1
                is_read_length_line = True
            elif is_read_length_line:
                # print("Sequence:", repr(line))
                # print("Length:", len(line))
                clean_line = line.replace("\n", "")
                if len(clean_line) in reads_data:  # Check if the length of the line is already a key in the dictionary
                    reads_data[len(clean_line)] += 1  # If the key exists, increment its value by 1
                else:
                    reads_data[
                        len(clean_line)] = 1  # If the key doesn't exist, add it to the dictionary with a value of 1
                is_read_length_line = False

    print_data(reads_data, reads_count)


def print_data(data, reads_count):
    print(f"Reads in the file = {reads_count}:")

    sorted_reads_data = dict(sorted(data.items()))
    sum_length = 0
    for key, value in sorted_reads_data.items():
        sum_length += key * value
        print(f"\twith length {key} = {value}")

    average = round(sum_length / reads_count)
    print(f"Reads sequence average length = {average}")


def main():
    file_name = input()
    print_data_from_file(file_name)


if __name__ == '__main__':
    main()
