import unittest
from nose.plugins import Plugin, PluginTester
from plugin import JsonExtendedPlugin

from collections import namedtuple


class Helper(PluginTester, unittest.TestCase):
    activate = '--with-json-extended'
    plugins = [JsonExtendedPlugin()]

    def makeSuite(self):
        class Stub(unittest.TestCase):
            def runTest(tc):
                self.stubtest(tc)

        return [Stub('runTest')]

    @property
    def results(self):
        return self.plugins[0]._sink.records


class SucceedsTest(Helper):

    def stubtest(self, tc):
        tc.assertTrue(True)

    def test(self):
        result = self.results[0]

        self.assertEquals(result.result, 'success')
        self.assertEquals(result.testcase.module,
                          'nosetests_json_extended.test_plugin.Stub')
        self.assertEquals(result.testcase.name, 'runTest')
        self.assertEquals(result.error, None)


class FailureTest(Helper):

    def stubtest(self, tc):
        tc.assertTrue(False)

    def test(self):
        result = self.results[0]
        self.assertEquals(result.result, 'failed')
        message = 'AssertionError: False is not true'
        self.assertEquals(result.error.message, message)
        self.assertIsInstance(result.error.traceback, list)


class ErrorTest(Helper):

    def stubtest(self, tc):
        raise Exception('errormessage')

    def test(self):
        result = self.results[0]
        self.assertEquals(result.result, 'error')
        self.assertEquals(result.error.message, 'Exception: errormessage')
        self.assertIsInstance(result.error.traceback, list)