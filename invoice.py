# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from sql import Cast
from sql.functions import Substring
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserWarning

__all__ = ['Invoice', 'InvoiceLine']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def post(cls, invoices):
        cls.check_warning_move_state(invoices)
        super(Invoice, cls).post(invoices)

    @classmethod
    def validate_invoice(cls, invoices):
        cls.check_warning_move_state(invoices)
        super(Invoice, cls).validate_invoice(invoices)

    @classmethod
    def check_warning_move_state(cls, invoices):
        Warning = Pool().get('res.user.warning')
        for invoice in invoices:
            if invoice.type != 'in':
                continue
            to_warning = set()
            for line in invoice.lines:
                if line.origin and line.origin.__name__ == 'stock.move':
                    if line.origin.state != 'done':
                        if line.origin.shipment:
                            to_warning.add(line.origin.shipment.rec_name)
                        else:
                            to_warning.add(line.origin.rec_name)
            if to_warning:
                key = 'warning_move_state.%s' % invoice.id,
                if Warning.check(key):
                    raise UserWarning(key, gettext('teb.confirm_run',
                            moves=', '.join(to_warning),
                            invoice=invoice.recname))


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    stock_move_state = fields.Function(fields.Selection([
            (None, ''),
            ('staging', 'Staging'),
            ('draft', 'Draft'),
            ('assigned', 'Assigned'),
            ('done', 'Done'),
            ('cancel', 'Canceled'),
            ], 'Stock Move State'),
        'get_stock_move_state', searcher='search_stock_move_state')

    @classmethod
    def get_stock_move_state(cls, lines, names):
        res = {n: {r.id: None for r in lines} for n in names}
        for name in names:
            for line in lines:
                if line.origin and line.origin.__name__ == 'stock.move':
                    res[name][line.id] = line.origin.state
        return res

    @classmethod
    def search_stock_move_state(cls, name, clause):
        pool = Pool()
        Move = pool.get('stock.move')

        table = cls.__table__()
        move = Move.__table__()
        _, operator, value = clause

        Operator = fields.SQL_OPERATORS[operator]
        query = table.join(move, type_='LEFT', condition=Cast(
            Substring(table.origin, 12), 'INTEGER') == move.id).select(
                table.id, where=(
                    table.origin.like('stock.move,%')
                    & Operator(move.state, value)))

        return [('id', 'in', query)]
