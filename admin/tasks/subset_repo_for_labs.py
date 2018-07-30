#!/usr/bin/env python
"""
Script to generate directories (or git branches) corresponding to subsets of the repo appropriate for different labs.

The script creates a subset of files corresponding to labs with index less than or equal than the one given,
as specified in lab_specific_files.yml

Furthermore, it also strips out text between blocks like
    # Your code below here (lab1)
    # <content>
    # Your code above here (lab1)
for labs with index greater than or equal to the one given.

"""
import argparse
import pathlib
import re
import shutil

import yaml


REPO_DIRNAME = pathlib.Path(__file__).parents[1].resolve()
INFO_FILENAME = REPO_DIRNAME / 'tasks' / 'lab_specific_files.yml'


def create_directory(output_dirname, lab_number):

    if output_dir.exists():
        shutil.rmtree(output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dirname', type=str, help='Where to output the lab subset directories.')
    args = parser.parse_args()

    with open(INFO_FILENAME) as f:
        info = yaml.load(f.read())

    output_dir = pathlib.Path(args.output_dirname)
    if output_dir.exists():
        shutil.rmtree(output_dir)

    for lab_number in info.keys():
        lab_output_dir = output_dir / f'lab{lab_number}'
        lab_output_dir.mkdir(parents=True)

        # Copy selected files
        selected_paths = sum([info.get(number, []) for number in range(lab_number + 1)], [])
        new_paths = []
        for path in selected_paths:
            new_path = lab_output_dir / path
            new_path.parents[0].mkdir(parents=True, exist_ok=True)
            shutil.copy(path, new_path)
            new_paths.append(new_path)

        # Strip out stuff between "Your code here" blocks
        beginning_comment = f'# Your code below here \(Lab {lab_number}\)'
        ending_comment = f'# Your code above here \(Lab {lab_number}\)'
        for path in new_paths:
            if path.suffix != '.py':
                continue
            with open(path) as f:
                contents = f.read()
            if not re.search(beginning_comment, contents):
                continue
            filtered_lines = []
            filtering = False
            for line in contents.split('\n'):
                if not filtering:
                    filtered_lines.append(line)
                if re.search(beginning_comment, line):
                    filtering = True
                    filtered_lines.append('')
                if re.search(ending_comment, line):
                    filtered_lines.append(line)
                    filtering = False
            with open(path, 'w') as f:
                f.write('\n'.join(filtered_lines))