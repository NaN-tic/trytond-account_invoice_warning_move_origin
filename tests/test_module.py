
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceWarningMoveOriginTestCase(CompanyTestMixin, ModuleTestCase):
    'Test AccountInvoiceWarningMoveOrigin module'
    module = 'account_invoice_warning_move_origin'


del ModuleTestCase
