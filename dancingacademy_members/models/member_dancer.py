from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

class MemberDancer(models.Model):
    _inherit = 'member.dancer'

    total_due = fields.Float(string="Total a Pagar", compute="_compute_total_due", store=True)
    payment_method = fields.Selection([
        ('cash', 'Efectivo'),
        ('direct_debit', 'Domiciliado')
    ], string="Método de Pago", default='cash', required=True)
    bank_account = fields.Char(string="Cuenta Bancaria")
    attached_document = fields.Binary(string="Documento Adjunto")
    attached_document_name = fields.Char(string="Nombre del Documento")

    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")

    @api.onchange('is_user_management')
    def _compute_is_user_management(self):
        for record in self:
            record.is_user_management = self.env.user.has_group('dancingacademy_base.group_academy_management_team')


    @api.depends('class_ids.price', 'class_ids')
    def _compute_total_due(self):
        """Calcula el total a pagar por las clases del mes actual."""
        for dancer in self:
            total = sum(dancer.class_ids.mapped('price'))
            dancer.total_due = total


    def generar_sepa_xml(self):
        # Filtrar los registros con método de pago 'direct_debit'
        alumnos_domiciliados = self.filtered(lambda r: r.payment_method == 'direct_debit')

        if not alumnos_domiciliados:
            raise UserError('No hay alumnos con el método de pago "Domiciliado".')

        # Crear el XML manualmente como cadena
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02">\n'
        xml_content += '  <CstmrDrctDbtInitn>\n'

        # Cabecera
        xml_content += '    <GrpHdr>\n'
        xml_content += '      <MsgId>SEPA_BATCH</MsgId>\n'
        xml_content += f'      <CreDtTm>{fields.Datetime.now()}</CreDtTm>\n'
        xml_content += f'      <NbOfTxs>{len(alumnos_domiciliados)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(record.total_due for record in alumnos_domiciliados):.2f}</CtrlSum>\n'
        xml_content += '      <InitgPty>\n'
        xml_content += f'        <Nm>{self.env.user.company_id.name}</Nm>\n'
        xml_content += '      </InitgPty>\n'
        xml_content += '    </GrpHdr>\n'

        # Información del pago
        xml_content += '    <PmtInf>\n'
        xml_content += '      <PmtInfId>PAYMENT_001</PmtInfId>\n'
        xml_content += '      <PmtMtd>DD</PmtMtd>\n'
        xml_content += '      <BtchBookg>true</BtchBookg>\n'
        xml_content += f'      <NbOfTxs>{len(alumnos_domiciliados)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(record.total_due for record in alumnos_domiciliados):.2f}</CtrlSum>\n'
        xml_content += f'      <ReqdColltnDt>{fields.Date.today()}</ReqdColltnDt>\n'
        xml_content += '      <Cdtr>\n'
        xml_content += f'        <Nm>{self.env.user.company_id.name}</Nm>\n'
        xml_content += f'        <IBAN>ES123456789</IBAN>\n'
        xml_content += '      </Cdtr>\n'

        # Detalle de cada transacción
        for record in alumnos_domiciliados:
            xml_content += '      <DrctDbtTxInf>\n'
            xml_content += '        <PmtId>\n'
            xml_content += f'          <EndToEndId>{record.name}</EndToEndId>\n'
            xml_content += '        </PmtId>\n'
            xml_content += f'        <InstdAmt Ccy="EUR">{record.total_due:.2f}</InstdAmt>\n'
            xml_content += '        <Dbtr>\n'
            xml_content += f'          <Nm>{record.name}</Nm>\n'
            xml_content += '        </Dbtr>\n'
            xml_content += '        <DbtrAcct>\n'
            xml_content += f'          <IBAN>{record.bank_account}</IBAN>\n'
            xml_content += '        </DbtrAcct>\n'
            xml_content += '      </DrctDbtTxInf>\n'

        # Cierre del XML
        xml_content += '    </PmtInf>\n'
        xml_content += '  </CstmrDrctDbtInitn>\n'
        xml_content += '</Document>\n'

        # Crear un adjunto en Odoo
        attachment = self.env['ir.attachment'].create({
            'name': 'SEPA_DirectDebit.xml',
            'type': 'binary',
            'datas': base64.b64encode(xml_content.encode('utf-8')).decode('utf-8'),
            'mimetype': 'application/xml',
            'res_model': 'member.dancer',
            'res_id': self[0].id,  # Usar el primer registro como referencia para el adjunto
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }