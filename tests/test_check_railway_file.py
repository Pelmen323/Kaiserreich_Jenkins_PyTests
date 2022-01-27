##########################
# The script analyzes the railways.txt file, if the line includes more or less provinces than specified - it throws error
# The error is very important as the game draws level 4 railways in half of the world if you provide less provinces than should
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest
from .imports.decorators import util_decorator_no_false_positives
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\map\\railways.txt"


@pytest.mark.parametrize("filepath", [(FILEPATH)])
@util_decorator_no_false_positives
def test_check_railways_file(filepath: str) -> bool:
    results = []
    lines = open_text_file(filepath).split('\n')
    line_counter = 0

    for line in lines:
        line_counter += 1
        if line == '':
            continue
        elif line[3] != ' ':
            counter_of_provinces_in_line = line[2:4]
        else:
            counter_of_provinces_in_line = line[2]
        str_with_provinces = line[4:].strip()
        list_with_provinces = str_with_provinces.split()
        if int(counter_of_provinces_in_line) != len(list_with_provinces):
            results.append(f"Line {line_counter} - expected {counter_of_provinces_in_line} provinces, got {list_with_provinces}. Line: {line}")

    if results != []:
        for i in results:
            print(f'- [ ] {i}')
        print(f'{len(results)} lines in railway file with issues found.')
        raise AssertionError("Encountered issues in railway file! Check console output")
