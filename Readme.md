# Subtitle Time Changer For srt Files

With this script you can change the time for a subtitle file of the .srt format.

## Running

The script takes two parameters.
The first <file_name> is the path to the subtitle file.
The second <time_to_change> is a string in the format "HH:MM:SS,MSx3", (MSx3: three digits for milliseconds).
This is added to all times in the subtitle file.

If you add a "-" infront of the time, it will add a negative time.\
Hence will substract time.
Be aware not to substract more than the first subtitle, as this is not taken care of with the script.

```Bash
python3 main.py file_name time_to_change
```