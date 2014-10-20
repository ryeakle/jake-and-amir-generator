#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jake_and_amir_generator_api.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
