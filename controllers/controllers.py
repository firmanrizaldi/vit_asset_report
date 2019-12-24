
from odoo import api, fields, models
import time
import datetime
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


# class BaseWebsite(http.Controller):
#     @http.route('/vit/index', type='http', auth='public', website=True)
#     def index(self, **kw):
#         user_obj = request.env['res.users']
#         user = user_obj.browse (request.uid)
#         is_admin = user.has_group('base.group_system')
#         return request.render('vit_has_group.index', {
#             'is_admin' : is_admin
#         })
