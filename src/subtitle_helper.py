import srt
import datetime
import os

class SubtitleHelper:
    filename = ""
    subtitle_queue = []
    included_indexes = []
    include_all = True

    def __init__(self, filename):
        self.filename = filename

        try:
            with open(filename, "r", encoding = 'utf8') as f:
                contents = srt.parse(f.read())

                if os.path.isfile("include.txt"):
                    print(f"An include.txt file has been detected. Do you want to include only the indexes in this file?")
                    if input() == "y":
                        self.include_all = False
                        with open("include.txt", "r") as include_file:
                            for line in include_file:
                                self.included_indexes.append(int(line))

                # Build a queue of subtitles in a dictionary with string and time. Time is in milliseconds always so convert the timedelta to milliseconds
                for item in contents:
                    if self.include_all:
                        self.subtitle_queue.append({
                            "content": item.content,
                            "start_time": item.start.total_seconds() * 1000,
                        })
                    else:
                        if item.index in self.included_indexes:
                            self.subtitle_queue.append({
                            "content": item.content,
                            "start_time": item.start.total_seconds() * 1000,
                        })

        except Exception as e:
            print(f"Error: Could not open file {filename}")
            print(e)
            exit(1)

    def __iter__(self):
        return self

    def __next__(self):
        next_subtitle = self.get_next_subtitle()
        
        if next_subtitle is None:
            raise StopIteration
        return next_subtitle

    def get_strings(self):
        strings = []

        for item in self.subtitle_queue:
            strings.append(item["content"])

        return strings

    def get_next_subtitle(self):
        if len(self.subtitle_queue) > 0:
            return self.subtitle_queue.pop(0)
        else:
            return None
