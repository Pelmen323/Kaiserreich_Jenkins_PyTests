##########################
# Test script to check for political having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_political_invalid_traits(test_runner: object):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    advisor_traits = Characters.get_advisors_traits(test_runner=test_runner, trait_type="political_advisor" , lowercase=True)
    results = []
       
    for adv in advisors:
        if adv.count('slot = political_advisor') > 0:
            try:
                advisor_name = re.findall('idea_token = (\w*)', adv)[0]
            except:
                results.append((adv, paths[adv], f'Missing idea_token'))
            invalid_trait_syntax = len(re.findall('traits = \\{\\n', adv)) > 0
            one_trait = re.findall('traits = \{ (\w*) \}', adv)
            if invalid_trait_syntax:
                 results.append((advisor_name, paths[adv], f'This advisor trait syntax is multiline - single-line syntax is strongly recommended'))
            elif one_trait != []:
                if one_trait[0] not in advisor_traits:
                    results.append((advisor_name, paths[adv], f'Invalid political trait encountered - {one_trait[0]}'))
            else:
                results.append((advisor_name, paths[adv], f'This advisor has <1 or >1 traits'))

    if results != []:
        ResultsReporter.report_results(results=results, message="Political advisors with invalid traits encountered. Check console output")
