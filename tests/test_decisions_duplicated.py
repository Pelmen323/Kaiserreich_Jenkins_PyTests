##########################
# Test script to check for duplicated decisions
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.decisions_class import Decisions


def test_check_duplicated_decisions(test_runner: object):
# Part 1 - get the dict of all decisions 
    decisions = Decisions.get_all_decisions(test_runner=test_runner)

# Part 2 - throw the error if entity is duplicated
    results = [i for i in decisions if decisions.count(i) > 1]
    ResultsReporter.report_results(results=results, message="Duplicated decisions were encountered. Check console output")
