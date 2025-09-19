from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_type = fields.Selection([
        ('domestic', 'Domestic'),
        ('import', 'Import')
    ], string='Purchase Type', default='domestic', tracking=True)
    partner_domain_ids = fields.Many2many('res.partner', compute='_compute_partner_domain_ids')

    partner_id = fields.Many2one(
        'res.partner', string='Vendor', domain="[('id', 'in', partner_domain_ids)]", tracking=True)

    @api.depends('purchase_type')
    def _compute_partner_domain_ids(self):
        for order in self:
            domain = [
                ('supplier_rank', '>', 0),
                # REMOVED: ('approval_state', '=', 'approved') - This field doesn't exist on res.partner
            ]
            if order.purchase_type:
                # We are doing this because in partner Tags(Category) is many2many. we can't use '=' operator
                category = self.env['res.partner.category'].search([('name', '=', order.purchase_type.capitalize())],
                                                                   limit=1)
                if category:
                    domain.append(('category_id', 'in', [category.id]))
            order.partner_domain_ids = self.env['res.partner'].search(domain)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
            self_comp = self.with_company(company_id)

            purchase_type = vals.get('purchase_type', 'domestic')

            if vals.get('name', 'New') == 'New':
                seq_date = None
                if 'date_order' in vals:
                    seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))

                if purchase_type == 'import':
                    sequence_code = 'purchase.order.import'
                else:
                    sequence_code = 'purchase.order.domestic'

                vals['name'] = self_comp.env['ir.sequence'].next_by_code(sequence_code, sequence_date=seq_date) or '/'

        return super().create(vals_list)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Add the missing fields that are causing the error
    is_storable = fields.Boolean(
        string='Is Storable',
        compute='_compute_is_storable',
        store=False
    )

    forecasted_issue = fields.Boolean(
        string='Forecasted Issue',
        default=False
    )

    @api.depends('product_id', 'product_id.type')
    def _compute_is_storable(self):
        for line in self:
            line.is_storable = line.product_id and line.product_id.type == 'product'