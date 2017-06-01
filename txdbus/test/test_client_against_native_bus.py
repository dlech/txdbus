import os
import sys

import six
from twisted.trial import unittest

from txdbus.test import client_tests


# Only test against the native bus if it's available

if 'DBUS_SESSION_BUS_ADDRESS' in os.environ:
    orig_env = os.environ['DBUS_SESSION_BUS_ADDRESS']

    class NativeBusMixin (object):

        def _setup(self):
            os.environ['DBUS_SESSION_BUS_ADDRESS'] = orig_env

        def _teardown(self):
            pass
            
    
    # "Copy" the objects unit tests into this module
    m = sys.modules[ __name__ ]

    for k,v in six.iteritems(client_tests.__dict__):
        if isinstance(v, type) and issubclass(v, client_tests.ServerObjectTester) \
                    and v is not client_tests.ServerObjectTester:
            setattr(m, k, type(k, (NativeBusMixin, v, unittest.TestCase), dict()))


