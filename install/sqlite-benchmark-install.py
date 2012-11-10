#!/usr/bin/env python

import os
sqlite_benchmark_dir = os.path.dirname(
    os.path.abspath(os.readlink(__file__))) + "/.."

import commands
import re
import shutil


## Config
dirs_to_ignore = [".git", "install"]
template_files = [
    "python/Config.py",
    "python/SQL.py",
    "make/Makefile",
]
script_to_update_dirs = ["python", "make"]


def create_dirs():
    # find directories
    dir_list = []
    for (search_path, dirs, files) in os.walk(sqlite_benchmark_dir):
        if search_path == sqlite_benchmark_dir:
            continue
        rel_search_path = search_path.replace(sqlite_benchmark_dir + "/", "")
        to_ignore_search_path = False
        for dir_to_ignore in dirs_to_ignore:
            match = re.match("^%s/?" % (dir_to_ignore), rel_search_path)
            if match:
                to_ignore_search_path = True
                break
        if not to_ignore_search_path:
            dir_list.append(rel_search_path)

    # create directories
    [os.mkdir(d) for d in dir_list if not os.path.exists(d)]


def install_template_files():
    [shutil.copyfile(
            sqlite_benchmark_dir + "/" + template_file,
            template_file)
     for template_file in template_files]

    # Only README-template.org should be copied separately
    # since sqlite3_benchmark has its own README.org
    shutil.copyfile(
        sqlite_benchmark_dir + "/" + "README-template.org",
        "README.org")


def install_scripts():
    # find scripts
    commited_files = commands.getoutput(
        "(cd %s ; git ls-files)" % (sqlite_benchmark_dir))
    commited_scripts = []
    for commited_file in commited_files.split():
        for script_dir in script_to_update_dirs:
            match = re.match("^%s" % (script_dir), commited_file)
            if match:
                commited_scripts.append(commited_file)

    # exclude template files
    scripts_to_install = []
    for commited_script in commited_scripts:
        if commited_script not in template_files:
            scripts_to_install.append(commited_script)

    # copy
    [shutil.copyfile(
            sqlite_benchmark_dir + "/" + script,
            script)
     for script in scripts_to_install]


def check_env():
    n_template_files = 0
    for template_file in template_files:
        if not os.path.exists(template_file):
            n_template_files += 1
    if n_template_files == 0:
        print(
"""
This directory does not seem to be an sqlite-benchmark directory.
(Too few template files exist)
Use this command in empty directory or sqlite-benchmark directory.
"""
        )
        exit(1)


def build_env():
    create_dirs()
    install_template_files()
    install_scripts()


def update_scripts():
    print("Updating scripts...")
    create_dirs()
    install_scripts()


def is_dir_empty():
    n_files = int(commands.getoutput("ls -a |wc -l"))
    return n_files == 2


def main():
    if is_dir_empty():
        print("Directory is empty. Newly build environment.")
        build_env()
    else:
        check_env()
        update_scripts()


if __name__ == '__main__':
    main()
