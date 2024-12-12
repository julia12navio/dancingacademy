from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from datetime import datetime

class MemberTeacher(models.Model):
    _inherit = 'member.teacher'

    sueldo = fields.Float(compute="_compute_sueldo")    
    bank_account = fields.Char(string="Cuenta Bancaria")
    dni = fields.Char(string="DNI")
    address = fields.Char(string="Dirección")   
    
    is_user_teacher = fields.Boolean(string="Es el mismo usuario Profesor", compute="_compute_is_user_teacher")
    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")
    is_teacher = fields.Boolean(string="Es Profesor", compute="_compute_is_teacher")
    bic = fields.Char(string="Dirección")

    invoice_lines = fields.One2many('invoice.line', 'teacher_id', string="Líneas de Facturas")
    
    @api.depends('invoice_lines')
    def _compute_sueldo(self):
        for record in self:
            price = self.invoice_lines[0].price
            if price:
                self.sueldo = price


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

    def generate_teacher_payments_xml(self):
        """Genera un archivo XML SEPA (pain.001.001.03) para pagos a profesores."""
        unpaid_invoice_lines = self.mapped('invoice_lines').filtered(lambda line: not line.is_paid)

        if not unpaid_invoice_lines:
            raise UserError("No hay pagos pendientes para los profesores.")

        # Obtener información de la compañía
        company = self.env.user.company_id
        company_bank = company.partner_id.bank_ids[:1]
        if not company_bank:
            raise UserError('La cuenta bancaria de la compañía no está configurada.')
        company_iban = company_bank.acc_number
        company_bic = company_bank.bank_id.bic

        # Generar XML
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<Document xmlns="urn:iso:std:iso.20022:tech:xsd:pain.001.001.03" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        xml_content += '  <CstmrCdtTrfInitn>\n'

        # Encabezado
        xml_content += '    <GrpHdr>\n'
        xml_content += f'      <MsgId>{datetime.now().strftime("%Y%m%d%H%M%S")}</MsgId>\n'
        xml_content += f'      <CreDtTm>{datetime.now().isoformat()}</CreDtTm>\n'
        xml_content += f'      <NbOfTxs>{len(unpaid_invoice_lines)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(line.price for line in unpaid_invoice_lines):.2f}</CtrlSum>\n'
        xml_content += '      <InitgPty>\n'
        xml_content += f'        <Nm>{company.name}</Nm>\n'
        xml_content += '        <Id>\n'
        xml_content += '          <OrgId>\n'
        xml_content += '            <Othr>\n'
        xml_content += f'              <Id>{company.vat or "UNKNOWN"}</Id>\n'
        xml_content += '            </Othr>\n'
        xml_content += '          </OrgId>\n'
        xml_content += '        </Id>\n'
        xml_content += '      </InitgPty>\n'
        xml_content += '    </GrpHdr>\n'

        # Información de pagos
        xml_content += '    <PmtInf>\n'
        xml_content += f'      <PmtInfId>PAGOS_PROFESORES_{datetime.now().strftime("%Y%m%d")}</PmtInfId>\n'
        xml_content += '      <PmtMtd>TRF</PmtMtd>\n'
        xml_content += f'      <NbOfTxs>{len(unpaid_invoice_lines)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(line.price for line in unpaid_invoice_lines):.2f}</CtrlSum>\n'
        xml_content += f'      <ReqdExctnDt>{fields.Date.today()}</ReqdExctnDt>\n'
        xml_content += '      <Dbtr>\n'
        xml_content += f'        <Nm>{company.name}</Nm>\n'
        xml_content += '        <PstlAdr>\n'
        xml_content += '          <Ctry>ES</Ctry>\n'
        xml_content += f'          <AdrLine>{company.street}</AdrLine>\n'
        xml_content += '        </PstlAdr>\n'
        xml_content += '      </Dbtr>\n'
        xml_content += '      <DbtrAcct>\n'
        xml_content += '        <Id>\n'
        xml_content += f'          <IBAN>{company_iban}</IBAN>\n'
        xml_content += '        </Id>\n'
        xml_content += '        <Ccy>EUR</Ccy>\n'
        xml_content += '      </DbtrAcct>\n'
        xml_content += '      <DbtrAgt>\n'
        xml_content += '        <FinInstnId>\n'
        xml_content += f'          <BIC>{company_bic}</BIC>\n'
        xml_content += '        </FinInstnId>\n'
        xml_content += '      </DbtrAgt>\n'
        xml_content += '      <ChrgBr>SLEV</ChrgBr>\n'

        # Transacciones individuales
        for line in unpaid_invoice_lines:
            xml_content += '      <CdtTrfTxInf>\n'
            xml_content += '        <PmtId>\n'
            xml_content += f'          <InstrId>{line.id}</InstrId>\n'
            xml_content += f'          <EndToEndId>PAY-{line.id}</EndToEndId>\n'
            xml_content += '        </PmtId>\n'
            xml_content += '        <Amt>\n'
            xml_content += f'          <InstdAmt Ccy="EUR">{line.price:.2f}</InstdAmt>\n'
            xml_content += '        </Amt>\n'
            xml_content += '        <CdtrAgt>\n'
            xml_content += '          <FinInstnId>\n'
            xml_content += f'            <BIC>{line.teacher_id.bic}</BIC>\n'
            xml_content += '          </FinInstnId>\n'
            xml_content += '        </CdtrAgt>\n'
            xml_content += '        <Cdtr>\n'
            xml_content += f'          <Nm>{line.teacher_id.name}</Nm>\n'
            xml_content += '          <PstlAdr>\n'
            xml_content += '            <Ctry>ES</Ctry>\n'
            xml_content += f'            <AdrLine>{line.teacher_id.address}</AdrLine>\n'
            xml_content += '          </PstlAdr>\n'
            xml_content += '        </Cdtr>\n'
            xml_content += '        <CdtrAcct>\n'
            xml_content += '          <Id>\n'
            xml_content += f'            <IBAN>{line.teacher_id.bank_account}</IBAN>\n'
            xml_content += '          </Id>\n'
            xml_content += '        </CdtrAcct>\n'
            xml_content += '        <RmtInf>\n'
            xml_content += f'          <Ustrd>Pago Factura {line.name}</Ustrd>\n'
            xml_content += '        </RmtInf>\n'
            xml_content += '      </CdtTrfTxInf>\n'

            # Marcar la factura como pagada
            line.write({'is_paid': True})

        xml_content += '    </PmtInf>\n'
        xml_content += '  </CstmrCdtTrfInitn>\n'
        xml_content += '</Document>\n'

        # Crear el adjunto
        attachment = self.env['ir.attachment'].create({
            'name': f'Pagos_Profesores_{fields.Date.today()}.xml',
            'type': 'binary',
            'datas': base64.b64encode(xml_content.encode('utf-8')).decode('utf-8'),
            'mimetype': 'application/xml',
            'res_model': 'teacher.payment',
            'res_id': self[0].id if len(self) == 1 else None,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
    }