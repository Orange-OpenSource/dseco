#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023-2026 Orange. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#     This product includes software developed by Orange.
#     4. Neither the name of Orange nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Module for executing smart diff between two ontologies.
"""

import argparse
from . import __version__
import contextlib
import re
import tempfile
from .ontology_stats import OntologyStats


ANSI_ESCAPE_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text):
        """Remove ANSI escape codes from a string."""
        return ANSI_ESCAPE_RE.sub('', text)

def is_ignorable(line):
    """Return True if the line should be skipped (empty, [+], [-])."""
    return not line or line.startswith('[+]') or line.startswith('[-]')


def is_section_title(line):
    """Return True if the line is a section title (=== ... ===)."""
    return line.startswith('===')


def extract_section_name(line):
    """Extract section name from a title line like '=== Triples Count ==='."""
    return line.strip('= ')


def parse_pipe_line(line):
    """Parse a pipe-separated line 'key | value' and return (key, value)."""
    parts = line.split('|', maxsplit=1)
    return parts[0].strip(), parts[1].strip()



def parse_stats_file(filepath):
        """Parse a stats file into a dictionary.
        Format: pipe-separated 'dseco:isCNAMEOf | 7456' -> {'dseco:isCNAMEOf': '7456'}
        Section titles (=== ... ===) are used as keys for standalone numeric lines.
        Lines starting with [+] or [-] are ignored.
        """
        stats = {}
        current_section = None
        with open(filepath, 'r') as f:
            for line in f:
                stripped = strip_ansi(line).strip()
                if is_ignorable(stripped):
                    continue
                if is_section_title(stripped):
                    current_section = extract_section_name(stripped)
                    continue
                if '|' in stripped:
                    key, value = parse_pipe_line(stripped)
                    stats[key] = value
                elif stripped.isdigit() and current_section:
                    stats[current_section] = stripped
        return stats

class OntologySmartDiff():
    """
    Class for handling ontology smart diff operations.
    """

    def __init__(self, new_stats, old_stats):
            """
            Initialize the ontology smart diff with paths to the new and old stats files.
            """
            self.new_stats = new_stats
            self.old_stats = old_stats

    def compare_stats(self, threshold=0.05):
        """Compare two stats dictionaries.
        Returns a dict of differences where:
        - Values differ by more than threshold (relative to the max of both)
        - Keys exist only in one of the two dicts
        Each entry contains: old_value, new_value, and status.
        """
        differences = {}
        encountered_keys = set()

        old_dict_stats = parse_stats_file(self.old_stats)
        new_dict_stats = parse_stats_file(self.new_stats)

        # First pass: iterate over old keys
        for key in old_dict_stats:
            encountered_keys.add(key)
            if key in new_dict_stats:
                old_val = old_dict_stats[key]
                new_val = new_dict_stats[key]
                old_num = float(old_val)
                new_num = float(new_val)
                max_val = max(abs(old_num), abs(new_num))

                if abs(old_num - new_num) / max_val > threshold:
                    differences[key] = {
                        'old': old_val,
                        'new': new_val,
                        'status': 'changed',
                    }

            else:
                differences[key] = {
                    'old': old_dict_stats[key],
                    'new': None,
                    'status': 'removed',
                }

        # Second pass: keys only in new_dict_stats
        for key in new_dict_stats:
            if key not in encountered_keys:
                differences[key] = {
                    'old': None,
                    'new': new_dict_stats[key],
                    'status': 'added',
                }

        return differences

def get_stats_file_path(stats):
    ontology_stats_new = OntologyStats(stats)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        new_stats_path = f.name
        with contextlib.redirect_stdout(f):
            ontology_stats_new.execute_all_queries()
    return new_stats_path

def format_output(differences):
    """Format the differences dict into readable output lines."""
    lines = []
    if not differences:
        lines.append("No significant differences found.")
        return lines

    changed = {k: v for k, v in differences.items() if v['status'] == 'changed'}
    removed = {k: v for k, v in differences.items() if v['status'] == 'removed'}
    added = {k: v for k, v in differences.items() if v['status'] == 'added'}

    if changed:
        lines.append("=== Changed (>5% difference) ===")
        for key, val in sorted(changed.items()):
            lines.append(f"  {key}: {val['old']} -> {val['new']}")

    if removed:
        lines.append("=== Removed (only in old) ===")
        for key, val in sorted(removed.items()):
            lines.append(f"  {key}: {val['old']}")

    if added:
        lines.append("=== Added (only in new) ===")
        for key, val in sorted(added.items()):
            lines.append(f"  {key}: {val['new']}")

    return lines

def print_formatted_output(differences):
    """Print the formatted differences to stdout."""
    lines = format_output(differences)
    for line in lines:
        print(line)
    


def main():
    """Parse command line arguments and execute predefined ontology statistics queries."""
    parser = argparse.ArgumentParser(description="Generate statistics for the ontology using predefined SPARQL queries.")
    parser.add_argument("--new", help="new ontology file", required=True)
    parser.add_argument("--old", help="old ontology file", required=True)

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    new_stats_path = get_stats_file_path(args.new)
    old_stats_path = get_stats_file_path(args.old)

    ontology_smart_diff = OntologySmartDiff(new_stats_path, old_stats_path)
    differences = ontology_smart_diff.compare_stats()
    print_formatted_output(differences)


if __name__ == "__main__":
    main()
