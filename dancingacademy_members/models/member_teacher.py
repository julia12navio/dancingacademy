from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from datetime import datetime

class MemberTeacher(models.Model):
    _inherit = 'member.teacher'

    sueldo = fields.Float()    
    bank_account = fields.Char(string="Cuenta Bancaria")
    dni = fields.Char(string="DNI")
    
    is_user_teacher = fields.Boolean(string="Es el mismo usuario Profesor", compute="_compute_is_user_teacher")
    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")
    is_teacher = fields.Boolean(string="Es Profesor", compute="_compute_is_teacher")

    invoice_lines = fields.One2many('invoice.line', 'teacher_id', string="Líneas de Facturas")

    @api.depends('user_id')
    def _compute_is_teacher(self):
        for record in self:
            record.is_user_teacher = self.env.user.has_group('dancingacademy_base.group_academy_teacher')

    @api.depends('user_id')
    def _compute_is_user_teacher(self):
        for record in self:
            record.is_user_teacher = self.env.user.id == record.user_id.id and \
                                    self.env.user.has_group('dancingacademy_base.group_academy_teacher')

    @api.depends('user_id')
    def _compute_is_user_management(self):
        for record in self:
            record.is_user_management = self.env.user.has_group('dancingacademy_base.group_academy_management_team')

    def generar_facturas_xml(self):
        # Obtener todas las líneas de factura no pagadas de los profesores seleccionados
        invoice_lines = self.mapped('invoice_lines').filtered(lambda line: not line.is_paid)

        if not invoice_lines:
            raise UserError("No hay facturas pendientes de pago para exportar.")

        # Generar el XML combinado
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">\n'
        xml_content += '  <CstmrCdtTrfInitn>\n'
        xml_content += '    <GrpHdr>\n'
        xml_content += f'      <MsgId>{datetime.now().strftime("%Y%m%d%H%M%S")}</MsgId>\n'
        xml_content += f'      <CreDtTm>{datetime.now().isoformat()}</CreDtTm>\n'
        xml_content += f'      <NbOfTxs>{len(invoice_lines)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(line.price for line in invoice_lines):.2f}</CtrlSum>\n'
        xml_content += '      <InitgPty>\n'
        xml_content += f'        <Nm>{self.env.user.company_id.name}</Nm>\n'
        xml_content += '      </InitgPty>\n'
        xml_content += '    </GrpHdr>\n'
        xml_content += '    <PmtInf>\n'
        xml_content += '      <PmtInfId>FACTURAS_TEACHERS</PmtInfId>\n'
        xml_content += '      <PmtMtd>TRF</PmtMtd>\n'
        xml_content += f'      <ReqdExctnDt>{fields.Date.today()}</ReqdExctnDt>\n'
        xml_content += '      <Dbtr>\n'
        xml_content += f'        <Nm>{self.env.user.company_id.name}</Nm>\n'
        xml_content += '      </Dbtr>\n'
        xml_content += '      <DbtrAcct>\n'
        xml_content += f'        <Id><IBAN>ES123456789</IBAN></Id>\n'
        xml_content += '      </DbtrAcct>\n'


        for line in invoice_lines:
            xml_content += '      <CdtTrfTxInf>\n'
            xml_content += '        <PmtId>\n'
            xml_content += f'          <NumFacId>{line.name}</NumFacId>\n'
            xml_content += '        </PmtId>\n'
            xml_content += '        <Amt>\n'
            xml_content += f'          <InstdAmt Ccy="EUR">{line.price:.2f}</InstdAmt>\n'
            xml_content += '        </Amt>\n'
            xml_content += '        <Cdtr>\n'
            xml_content += f'          <Nm>{line.teacher_id.name}</Nm>\n'
            xml_content += f'          <DNI>{line.teacher_id.dni}</DNI>\n'
            xml_content += '        </Cdtr>\n'
            xml_content += '        <CdtrAcct>\n'
            xml_content += f'          <Id><IBAN>{line.teacher_id.bank_account}</IBAN></Id>\n'
            xml_content += '        </CdtrAcct>\n'
            xml_content += '        <RmtInf>\n'
            xml_content += f'          <Ustrd>Pago Factura {line.name}</Ustrd>\n'
            xml_content += '        </RmtInf>\n'
            xml_content += '        <ReqdExctnDt>\n'
            xml_content += f'          {line.date_to_pay or fields.Date.today()}\n'
            xml_content += '        </ReqdExctnDt>\n'
            xml_content += '      </CdtTrfTxInf>\n'

        xml_content += '    </PmtInf>\n'
        xml_content += '  </CstmrCdtTrfInitn>\n'
        xml_content += '</Document>\n'

        # Crear el adjunto
        attachment = self.env['ir.attachment'].create({
            'name': 'Facturas_Pendientes_Teachers.xml',
            'type': 'binary',
            'datas': base64.b64encode(xml_content.encode('utf-8')).decode('utf-8'),
            'mimetype': 'application/xml',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
