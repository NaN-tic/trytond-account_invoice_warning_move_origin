# This file is part account_invoice_warning_move_origin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountInvoiceWarningMoveOriginTestCase(ModuleTestCase):
    'Test Account Invoice Warning Move Origin module'
    module = 'account_invoice_warning_move_origin'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceWarningMoveOriginTestCase))
    return suite
