
from odoo import api, fields, models, tools
import time
import datetime
import logging
_logger = logging.getLogger(__name__)


class Assetreports(models.Model):
    _inherit = 'account.asset.asset'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Unit')
    analytic_tag_ids = fields.Many2one('account.analytic.tag', string='Location', 
                                        domain=[('analytic_dimension_id.name','=','LOCATION')])
    
    analytic_tag2_ids = fields.Many2one('account.analytic.tag', string='Bisnis', 
                                        domain=[('analytic_dimension_id.name','=','BISNIS')])
    
    
class Asetreportssd(models.Model):
    _inherit = 'asset.asset.report'
    
    analytic_tag_ids = fields.Many2one('account.analytic.tag', string='Location', 
                                        domain=[('analytic_dimension_id.name','=','LOCATION')])
    
    
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'asset_asset_report')
        self._cr.execute("""
            create or replace view asset_asset_report as (
                                select
                    min(dl.id) as id,
                    dl.name as name,
                    dl.depreciation_date as depreciation_date,
                    a.date as date,
                    (CASE WHEN dlmin.id = min(dl.id)
                      THEN a.value
                      ELSE 0
                      END) as gross_value,
                    dl.amount as depreciation_value,
                    dl.amount as installment_value,
                    (CASE WHEN dl.move_check
                      THEN dl.amount
                      ELSE 0
                      END) as posted_value,
                    (CASE WHEN NOT dl.move_check
                      THEN dl.amount
                      ELSE 0
                      END) as unposted_value,
                    dl.asset_id as asset_id,
                    dl.move_check as move_check,
                    a.category_id as asset_category_id,
                    a.partner_id as partner_id,
                    a.analytic_tag_ids as analytic_tag_ids,
                    a.state as state,
                    count(dl.*) as installment_nbr,
                    count(dl.*) as depreciation_nbr,
                    a.company_id as company_id
                from account_asset_depreciation_line dl
                    left join account_asset_asset a on (dl.asset_id=a.id)
                    left join (select min(d.id) as id,ac.id as ac_id from account_asset_depreciation_line as d inner join account_asset_asset as ac ON (ac.id=d.asset_id) group by ac_id) as dlmin on dlmin.ac_id=a.id
                where a.active is true 
                group by
                    dl.amount,dl.asset_id,dl.depreciation_date,dl.name,
                    a.date, dl.move_check, a.state, a.category_id, a.partner_id, a.company_id,
                    a.value, a.id, a.salvage_value, dlmin.id, a.analytic_tag_ids
        )""")

    