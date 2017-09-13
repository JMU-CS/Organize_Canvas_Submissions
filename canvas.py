"""Organize files submitted via Canvas into directories."""

import names
import glob
import os
import sys


def main(path):
    """Organize downloads from canvas into folders by usernames."""
    files = glob.glob(path + "/*")
    for name in sorted(files):
        # format: path/student_number_number_filename
        u0 = name.rfind('/')            # get idx where canvasname starts
        u1 = name.find('_', u0 + 1)     # get idx where number1 starts
        u2 = name.find('_', u1 + 1)     # get idx where number2 starts
        u3 = name.find('_', u2 + 1)     # get idx where filename starts
        student = name[u0 + 1:u1]

        # special case: late submission
        if "_late" in name:         # usual format is:
                                    # path/student_late_number_number_filename
            late = "_LATE"
            u3 = name.find('_', u3 + 1)
            if name.count('_') == 3:    # this is some weird case
                                        # where number2 is missing
                u3 = name.find('_', u2 + 1)
        else:
            late = ""
            if name.count('_') == 2:    # this is some weird case
                                        # where number2 is missing
                u3 = name.find('_', u1 + 1)

        filename = name[u3 + 1:]
        # special case: re-submission, remove the dash
        u4 = filename.rfind('-')
        if u4 > -1:
            u5 = filename.rfind('.')
            num = filename[u4 + 1:u5]
            if len(num) == 1 and num.isdigit():
                filename = filename[:u4] + filename[u5:]

        # created dir if needed, move/rename the file
        eid = names.IDS[student]
        dname = path + '/' + eid + late
        if not os.path.exists(dname):
            os.mkdir(dname)
        os.rename(name, dname + '/' + filename)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Usage: python canvas.py PATH"
