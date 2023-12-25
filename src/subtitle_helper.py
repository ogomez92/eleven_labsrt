import srt

class SubtitleHelper:
    filename = ""
    contents = ""

    def __init__(self, filename):
        self.filename = filename

        try:
            with open(filename, "r", encoding = 'utf8') as f:
                self.contents = srt.parse(f.read())

        except Exception as e:
            print(f"Error: Could not open file {filename}")
            print(e)
            exit(1)

    def get_strings(self):
        strings = []

        for item in self.contents:
            strings.append(item.content)

        return strings
    