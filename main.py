import sys


def read_data(file: str):
    file_reader = open(file)
    line_count = 0
    subtitles = []
    subtitles_dict = {}
    subtitle_number = 0
    subtitle_time = ""
    for line in file_reader:
        line = line.split("\n")[0]
        if not line:
            subtitles_dict[subtitle_number] = {"time": subtitle_time, "subtitles": subtitles}
            line_count = -1
            subtitles = []
        elif line_count == 0:
            subtitle_number = line
        elif line_count == 1:
            subtitle_time = line
        else:
            subtitle_element = line
            subtitles.append(subtitle_element)
        line_count += 1

    return subtitles_dict


def add_time(time_string: str, adding_time: str):
    time_split_by_milli = time_string.split(",")
    adding_time_split_by_milli = adding_time.split(",")

    milli_seconds = int(time_split_by_milli[1])
    adding_milli_seconds = int(adding_time_split_by_milli[1])

    split_time = time_split_by_milli[0].split(":")
    split_adding_time = adding_time_split_by_milli[0].split(":")

    seconds = int(split_time[2])
    minutes = int(split_time[1])
    hours = int(split_time[0])

    adding_seconds = int(split_adding_time[2])
    adding_minutes = int(split_adding_time[1])
    adding_hours = int(split_adding_time[0])

    new_milli_seconds = calcualte_new_time(milli_seconds, adding_milli_seconds, 1000, False, False)
    new_seconds = calcualte_new_time(seconds, adding_seconds, 60, new_milli_seconds['overflow'],
                                     new_milli_seconds['underflow'])
    new_minutes = calcualte_new_time(minutes, adding_minutes, 60, new_seconds['overflow'], new_seconds['underflow'])
    new_hours = calcualte_new_time(hours, adding_hours, 60, new_minutes['overflow'], new_minutes['underflow'])

    new_milli_seconds_str = attach_pre_zero(str(new_milli_seconds['time']), 3)
    new_seconds_str = attach_pre_zero(str(new_seconds['time']), 2)
    new_minutes_str = attach_pre_zero(str(new_minutes['time']), 2)
    new_hours_str = attach_pre_zero(str(new_hours['time']), 2)

    return new_hours_str + ":" + new_minutes_str + ":" + new_seconds_str + "," + new_milli_seconds_str


def calcualte_new_time(old_time: int, adding_time: int, max_value: int, prev_overflow: bool, prev_underflow: bool):
    overflow = False
    underflow = False

    if prev_overflow:
        adding_time += 1
    elif prev_underflow:
        adding_time -= 1

    new_time = old_time + adding_time
    if new_time > max_value:
        overflow = True
        new_time -= max_value
    elif new_time < 0:
        underflow = True
        new_time = max_value + new_time

    return {'time': new_time, 'overflow': overflow, 'underflow': underflow}


def attach_pre_zero(time_string: str, length_to_be: int):
    while len(time_string) < length_to_be:
        time_string = "0" + time_string
    return time_string


def add_time_to_dict(subtitle_dict: dict, time_to_add: str):
    for entry_number, entry in subtitle_dict.items():
        subtitle_time = entry["time"].split(" --> ")
        start_time = subtitle_time[0]
        end_time = subtitle_time[1]
        new_start_time = add_time(start_time, time_to_add)
        new_end_time = add_time(end_time, time_to_add)
        entry["time"] = new_start_time + " --> " + new_end_time

    return subtitle_dict


def write_dict(subtitle_dict: dict, file: str):
    file_to_write = open(file, "w+")
    for elem, entry in subtitle_dict.items():
        file_to_write.write(elem + "\n")
        file_to_write.write(entry["time"] + "\n")
        for subtitle in entry["subtitles"]:
            file_to_write.write(subtitle + "\n")
        file_to_write.write("\n")


def print_dict(data_dict: dict):
    for subtitle_number, subtitles in data_dict.items():
        print(subtitle_number, end="")
        print(": ", end="")
        print(subtitles)


def negative_time(time_string: str):
    split_by_milli = time_string.split(",")
    new_milli = str(-1 * int(split_by_milli[1]))

    split_time = split_by_milli[0].split(":")
    new_hours = str(-1 * int(split_time[0]))
    new_minutes = str(-1 * int(split_time[1]))
    new_seconds = str(-1 * int(split_time[2]))

    return new_hours + ":" + new_minutes + ":" + new_seconds + "," + new_milli


def main():
    if len(sys.argv) > 3 or len(sys.argv) == 1:
        print("Check the Readme for how to run the file.")
        return
    else:
        file = sys.argv[1]
        time = sys.argv[2]
        if time[:1] == "-":
            time = negative_time(time[1:])
        subtitles_dict = read_data(file)
        subtitles_dict = add_time_to_dict(subtitles_dict, time)
        write_dict(subtitles_dict, file + ".new")
        print("New subtitle file written.")


if __name__ == '__main__':
    main()
