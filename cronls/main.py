#/usr/bin/env python3
'''
Main program to use it in the command line interpreter.
'''

from pathlib import Path
from collections import namedtuple
import argparse

CRON_SCHEDULED = [Path(path) for path in ["/etc/cron.daily",
                                          "/etc/cron.hourly",
                                          "/etc/cron.weekly",
                                          "/etc/cron.monthly"]]

CRON_PATHS = [Path(path) for path in ["/etc/cron.d",
                                      "/var/spool/cron/crontabs",
                                      "/etc/anacrontab"]]

CRON_FILES = [Path(file) for file in ["/etc/crontab"]]

Cronfile = namedtuple("Cronfile", ["name", "path", "content"])


def cron_scanner():
    """Scan paths and files and return lists of "cronfiles" items."""
    path_results = [Cronfile(
                      name=file.name,
                      path=str(file.resolve()),
                      content=file.read_text()
                  )
               for cronfile in CRON_PATHS for file in cronfile.glob('[!.]*')
               if cronfile.is_dir()]

    file_results = [Cronfile(
                      name=file.name,
                      path=str(file.resolve()),
                      content=file.read_text()
                  ) for file in CRON_FILES if file.is_file()]

    return path_results + file_results


def arg_parser():
    """Parse args."""
    parser = argparse.ArgumentParser(
                        description="""Check all cron entries in the system""")
    parser.add_argument("-c", "--show-comments", dest="show_comments",
                        action='store_true',
                        help='''Print commented lines (disable by default)''')

    parser.add_argument("-s", "--show-scheduled", dest="show_scheduled",
                        action='store_true',
                        help='''Print lines of standard scheduled crontabs
                                (daily, monthly, etc...)''')
    return parser.parse_args()

    pass


def main():
    """Command line app."""
    args = arg_parser()
    if args.show_scheduled:
        global CRON_PATHS
        global CRON_SCHEDULED
        CRON_PATHS += CRON_SCHEDULED
    cron_files = cron_scanner()
    for file in cron_files:
        print("Filename: {}".format(file.name))
        print("Location: {}".format(file.path))
        print("Content:")
        if args.show_comments:
            for line in file.content.splitlines():
                print("\t{}".format(line))
        else:
            for line in file.content.splitlines():
                if not line.startswith("#"):
                    print("\t{}".format(line))
        print("\n")


if __name__ == "__main__":
    main()
