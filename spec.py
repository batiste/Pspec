import sys
import unittest
import types
import inspect
import six

class expect(unittest.TestCase):

    _expect_pspec = True

    def __init__(self, v):
        self.value = v
        unittest.TestCase.__init__(self)

    def to_equal(self, v):
        self.assertEqual(self.value, v)
        return self
    #to_eq = to_equal
    #eq = to_equal

    def to_not_equal(self, v):
        self.assertNotEqual(self.value, v)
        return self
    #not_eq = to_not_equal
    #to_not_eq = to_not_equal

    def runTest(self):
        pass


class Spec(unittest.TestCase):

    _pspec_testcase = True

    def __init__(self):
        unittest.TestCase.__init__(self)

    def test_methods(self):
        methods = []
        for m in dir(self):
            if m.startswith('it_'):
                methods.append(m)
        return methods

    def runTest(self):
        methods = self.test_methods()
        for m in methods:
            method = getattr(self, m)
            method()

def suite(name_or_module):
    suite = unittest.TestSuite()
    tests = gather_tests(name_or_module)
    for test in tests:
        suite.addTest(test)
    return suite


def gather_tests(name_or_module):
    tests = []

    if isinstance(name_or_module, six.string_types):
        module = sys.modules[name_or_module]
    else:
        module = name_or_module

    if not inspect.ismodule(module):
        raise "Not a module"
    
    for m_name in dir(module):

        m_object = getattr(module, m_name)

        if inspect.isfunction(m_object):
            if m_name.startswith('it_'):
                desc = m_name[3:].replace('_', ' ')
                tc = unittest.FunctionTestCase(m_object, description=desc)
                tests.append(tc)

        if inspect.isclass(m_object):
            if getattr(m_object, '_pspec_testcase', False):
                tests.append(m_object())

    return tests

def run(name_or_module):
    runner = unittest.TextTestRunner()
    _suite = suite(name_or_module)
    return runner.run(_suite)

