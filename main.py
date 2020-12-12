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
    adding_time_split_by_milli = adding_time.split(",")
    time_split_by_milli = time_string.split(",")
    adding_milli_seconds = int(adding_time_split_by_milli[1])
    time_milli_seconds = int(time_split_by_milli[1])
    milli_seconds_overflow = False
    milli_seconds_underflow = False
    new_milli_seconds = adding_milli_seconds + time_milli_seconds
    if new_milli_seconds >= 1000:
        milli_seconds_overflow = True
        new_milli_seconds = new_milli_seconds - 1000
    if new_milli_seconds < 0:
        milli_seconds_underflow = True
        new_milli_seconds = 1000 + new_milli_seconds

    split_time = time_split_by_milli[0].split(":")
    split_adding_time = adding_time_split_by_milli[0].split(":")

    seconds = int(split_time[2])
    minutes = int(split_time[1])
    hours = int(split_time[0])

    adding_seconds = int(split_adding_time[2])
    if milli_seconds_overflow:
        adding_seconds += 1
    if milli_seconds_underflow:
        adding_seconds -= 1
    adding_minute = int(split_adding_time[1])
    adding_hour = int(split_adding_time[0])

    new_seconds = seconds + adding_seconds
    seconds_overflow = False
    seconds_underflow = False
    if new_seconds >= 60:
        seconds_overflow = True
        new_seconds -= 60
    elif new_seconds < 0:
        seconds_underflow = True
        new_seconds = 60 + new_seconds

    new_minutes = minutes + adding_minute
    if seconds_overflow:
        new_minutes += 1
    if seconds_underflow:
        new_minutes -= 1
    minute_overflow = False
    minute_underflow = False
    if new_minutes >= 60:
        minute_overflow = True
        new_minutes -= 60
    if new_minutes < 0:
        minute_underflow = True
        new_minutes = 60 + new_minutes

    new_hours = hours + adding_hour
    if minute_overflow:
        new_hours += 1
    if minute_underflow:
        new_hours -= 1

    if len(str(new_hours)) < 2:
        new_hours = "0" + str(new_hours)
    else:
        new_hours = str(new_hours)

    if len(str(new_minutes)) < 2:
        new_minutes = "0" + str(new_minutes)
    else:
        new_minutes = str(new_minutes)

    if len(str(new_seconds)) < 2:
        new_seconds = "0" + str(new_seconds)
    else:
        new_seconds = str(new_seconds)

    if len(str(new_milli_seconds)) < 3:
        if len(str(new_milli_seconds)) == 1:
            new_milli_seconds = "00" + str(new_milli_seconds)
        else:
            new_milli_seconds = "0" + str(new_milli_seconds)
    else:
        new_milli_seconds = str(new_milli_seconds)

    return new_hours + ":" + new_minutes + ":" + new_seconds + "," + new_milli_seconds


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
