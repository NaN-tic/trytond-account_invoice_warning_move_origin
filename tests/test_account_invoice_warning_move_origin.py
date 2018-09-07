# This file is part account_invoice_warning_move_origin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceWarningMoveOriginTestCase(ModuleTestCase):
    'Test Account Invoice Warning Move Origin module'
    module = 'account_invoice_warning_move_origin'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceWarningMoveOriginTestCase))
    return suite
