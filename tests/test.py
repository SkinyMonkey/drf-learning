from valid_tests import tests as valid_tests
from invalid_tests import tests as invalid_tests

#try:
    # Testing a normal use of the API
valid_results = valid_tests()

    # Testing the error/bad requests are handled correctly
invalid_tests(valid_results)
#except Exception as e:
#    print "Error: %s" % e.message
