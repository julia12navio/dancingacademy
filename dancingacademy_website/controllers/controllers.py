from odoo import http
from odoo.http import request

class DancingAcademyWebsite(http.Controller):

    @http.route('/classes', type='http', auth='public', website=True)
    def list_classes(self, **kwargs):
        """Renderiza la lista de clases en la página web."""
        classes = request.env['dancingacademy.class'].sudo().search([])
        return request.render('dancingacademy_website.classes_list_template', {'classes': classes})

    @http.route('/classes/<model("dancingacademy.class"):class_obj>', type='http', auth='public', website=True)
    def class_detail(self, class_obj, **kwargs):
        """Renderiza el detalle de una clase específica."""
        return request.render('dancingacademy_website.class_detail_template', {'class': class_obj})
