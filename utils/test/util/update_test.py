#!/usr/bin/env python
import sys
import subprocess
import traceback

for x in sys.argv[1:]:
    try:
        sys.stderr.write("... updating %s\n" % x)
        with open(x) as f:
            lines = f.readlines()

        if not lines[0].startswith("# RUN: "):
            sys.stderr.write("Unexpected test\n")
            sys.exit(1)

        command = lines[0][7:]
        command, b, suffix = command.partition('|')
        if 'FileCheck' not in suffix:
            sys.stderr.write("Unexpected test\n")
            sys.exit(1)

        with open(x, 'w') as f:
            f.write(lines[0])
            f.write('\n')
            stderr = subprocess.STDOUT if '2>&1' in command else None
            output = subprocess.check_output(command, shell=True, stderr=stderr)
            for line in output.splitlines():
                line = line.strip()
                if line == '':
                    f.write('\n')
                    continue
                f.write('CHECK: ' + line + "\n")
    except:
        traceback.print_exc()
