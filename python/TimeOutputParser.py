import re
import os


class TimeOutputParser(object):
    def __init__(self, output_path):
        self.output_path = output_path
        self.REAL_LABEL = "real_time"
        self.SYS_LABEL = "sys_time"
        self.USER_LABEL = "user_time"
        self.timeOutputRegex = """real (?P<%s>[.0-9eE]+)
user (?P<%s>[.0-9eE]+)
sys (?P<%s>[.0-9eE]+)""" % (
            self.REAL_LABEL,
            self.USER_LABEL,
            self.SYS_LABEL,
        )

    def get_dict(self):
        """
        @return
        None if failed to get the last result of time command.
        """
        if not os.path.exists(self.output_path):
            return None
        with open(self.output_path) as f_to:
            timeOutput = f_to.read()
            p = re.compile(self.timeOutputRegex)
            m = p.search(timeOutput)
            return {
                self.REAL_LABEL: float(m.group(self.REAL_LABEL)),
                self.USER_LABEL: float(m.group(self.USER_LABEL)),
                self.SYS_LABEL: float(m.group(self.SYS_LABEL)),
            }
