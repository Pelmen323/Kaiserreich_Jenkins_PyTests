##########################
# Test script to check if ai factors with 4+ digits after decimal point are used
# Hoi4 supports only 3 digits after decimal, ignoring it results in huge ussues with the factors (like '0.4286' results in '4' factor instead)
# See here for proof https://hoi4.paradoxwikis.com/AI_modding
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from ..test_classes.generic_test_class import TestClass
import logging


def test_check_values_digits_after_decimal(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if 'ambient_object' in filename: continue
        text_file = test.open_text_file(filename).lower()

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            pattern_matches = re.findall('\\d\\.\\d{4,10}', current_line)
            if len(pattern_matches) > 0:
                if '#' not in current_line:
                    results[f'{os.path.basename(filename)}, line {line}'] = current_line

    if results != {}:
        logging.warning("Values with 4+ digits after decimal point found!:")
        for i in results.items(): 
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} values with 4+ digits after decimal point found.')
        raise AssertionError("Values with 4+ digits after decimal point found, Hoi4 factors supports only 3 digits after decimal point! Check console output")
