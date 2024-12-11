from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from datetime import datetime

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
    mandate_reference = fields.Char(string="Referencia de Mandato")
    mandate_date = fields.Date(string="Fecha de Mandato")
    payment_status = fields.Selection([
        ('unpaid', 'No pagado'),
        ('paid', 'Pagado')
    ], string="Estado de Pago", default='unpaid')
    address = fields.Char(string="Dirección")
    bic = fields.Char(string="Dirección")

    invoice_ids = fields.One2many('account.move', 'dancer_id', string="Facturas", help="Facturas generadas para el alumno.")

    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")
    is_user = fields.Boolean(string="Es Usuario", compute="_compute_is_user", store=False)


    @api.onchange('is_user')
    def _compute_is_user(self):
        for record in self:
            record.is_user = record.user_id.id == self.env.user.id

    @api.onchange('is_user_management')
    def _compute_is_user_management(self):
        for record in self:
            record.is_user_management = self.env.user.has_group('dancingacademy_base.group_academy_management_team')

    @api.model
    def update_payment_status(self):
        """Actualizar el estado de pago cada 1 de cada mes."""
        # Alumnos con método de pago domiciliado: se marcan como pagados automáticamente.
        domiciliados = self.search([('payment_method', '=', 'direct_debit')])
        domiciliados.write({'payment_status': 'unpaid'})

        # Alumnos con método de pago en efectivo: se marcan como no pagados.
        no_domiciliados = self.search([('payment_method', '=', 'cash')])
        no_domiciliados.write({'payment_status': 'unpaid'})


    @api.depends('class_ids.price', 'class_ids')
    def _compute_total_due(self):
        """Calcula el total a pagar por las clases del mes actual."""
        for dancer in self:
            total = sum(dancer.class_ids.mapped('price'))
            dancer.total_due = total

    def generate_monthly_invoices(self):
        """Genera facturas mensuales para los alumnos con clases activas."""
        product_model = self.env['product.product']

        for dancer in self:
            if dancer.total_due <= 0:
                continue

            # Crear líneas de factura basadas en las clases del alumno
            invoice_lines = []
            for dance_class in dancer.class_ids:
                # Verificar o crear el producto para la clase
                product = product_model.search([('name', '=', dance_class.name)], limit=1)
                if not product:
                    product = product_model.create({
                        'name': dance_class.name,
                        'type': 'service',
                        'list_price': dance_class.price,
                    })

                invoice_lines.append((0, 0, {
                    'product_id': product.id,
                    'name': dance_class.name,
                    'quantity': 1,
                    'price_unit': dance_class.price,
                    'tax_ids': [(6, 0, [])],  # Sin IVA
                }))

            # Crear factura
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': dancer.user_id.partner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines,
                'dancer_id': dancer.id
            }
            invoice = self.env['account.move'].create(invoice_vals)

            # Confirmar factura automáticamente
            invoice.action_post()

            # Asociar factura al alumno
            dancer.invoice_ids = [(4, invoice.id)]


    def generate_sepa_xml(self):
        """Genera un archivo XML SEPA (pain.001.001.03) para transferencias de crédito."""
        direct_debit_dancers = self.filtered(lambda r: r.payment_method == 'direct_debit')

        if not direct_debit_dancers:
            raise UserError('No hay alumnos con el método de pago "Domiciliado".')

        # Validar datos
        for dancer in direct_debit_dancers:
            if not dancer.bank_account:
                raise UserError(f'El alumno {dancer.name} no tiene una cuenta bancaria configurada.')
            if dancer.total_due <= 0:
                raise UserError(f'El alumno {dancer.name} no tiene un monto válido para cobrar.')

        company = self.env.user.company_id
        company_bank = company.partner_id.bank_ids[:1]
        if not company_bank:
            raise UserError('La cuenta bancaria de la compañía no está configurada.')
        company_iban = company_bank.acc_number
        company_bic = company_bank.bank_id.bic

        # Cabecera XML
        xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml_content += '<Document xmlns="urn:iso:std:iso.20022:tech:xsd:pain.001.001.03" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        xml_content += '  <CstmrCdtTrfInitn>\n'

        # Grupo de encabezado
        xml_content += '    <GrpHdr>\n'
        xml_content += f'      <MsgId>{datetime.now().strftime("%Y%m%d%H%M%S")}</MsgId>\n'
        xml_content += f'      <CreDtTm>{datetime.now().isoformat()}</CreDtTm>\n'
        xml_content += f'      <NbOfTxs>{len(direct_debit_dancers)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(dancer.total_due for dancer in direct_debit_dancers):.2f}</CtrlSum>\n'
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

        # Información de pago
        xml_content += '    <PmtInf>\n'
        xml_content += f'      <PmtInfId>{datetime.now().strftime("%Y%m%d%H%M%S")}</PmtInfId>\n'
        xml_content += '      <PmtMtd>TRF</PmtMtd>\n'
        xml_content += f'      <NbOfTxs>{len(direct_debit_dancers)}</NbOfTxs>\n'
        xml_content += f'      <CtrlSum>{sum(dancer.total_due for dancer in direct_debit_dancers):.2f}</CtrlSum>\n'
        xml_content += '      <PmtTpInf>\n'
        xml_content += '        <SvcLvl>\n'
        xml_content += '          <Cd>SEPA</Cd>\n'
        xml_content += '        </SvcLvl>\n'
        xml_content += '      </PmtTpInf>\n'
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
        for dancer in direct_debit_dancers:
            xml_content += '      <CdtTrfTxInf>\n'
            xml_content += '        <PmtId>\n'
            xml_content += f'          <InstrId>{dancer.mandate_reference}</InstrId>\n'
            xml_content += f'          <EndToEndId>{datetime.now().strftime("%Y%m%d%H%M%S")}{dancer.name}</EndToEndId>\n'
            xml_content += '        </PmtId>\n'
            xml_content += '        <Amt>\n'
            xml_content += f'          <InstdAmt Ccy="EUR">{dancer.total_due:.2f}</InstdAmt>\n'
            xml_content += '        </Amt>\n'
            xml_content += '        <CdtrAgt>\n'
            xml_content += '          <FinInstnId>\n'
            xml_content += f'            <BIC>{dancer.bic}</BIC>\n'
            xml_content += '          </FinInstnId>\n'
            xml_content += '        </CdtrAgt>\n'
            xml_content += '        <Cdtr>\n'
            xml_content += f'          <Nm>{dancer.name}</Nm>\n'
            xml_content += '          <PstlAdr>\n'
            xml_content += '            <Ctry>ES</Ctry>\n'
            xml_content += f'            <AdrLine>{dancer.address}</AdrLine>\n'
            xml_content += '          </PstlAdr>\n'
            xml_content += '        </Cdtr>\n'
            xml_content += '        <CdtrAcct>\n'
            xml_content += '          <Id>\n'
            xml_content += f'            <IBAN>{dancer.bank_account}</IBAN>\n'
            xml_content += '          </Id>\n'
            xml_content += '        </CdtrAcct>\n'
            xml_content += '        <RmtInf>\n'

            # Generar mensaje con facturas no pagadas
            unpaid_invoices = dancer.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.payment_state != 'paid')
            invoice_details = ', '.join([f"Factura: {invoice.name}" for invoice in unpaid_invoices])

            # Incluir información del alumno y sus facturas no pagadas
            xml_content += f'          <Ustrd>Pago de {dancer.name}. {invoice_details}</Ustrd>\n'
            xml_content += '        </RmtInf>\n'
            xml_content += '      </CdtTrfTxInf>\n'

            # Marcar al alumno como pagado
            dancer.write({'payment_status': 'paid'})

            # Marcar las facturas no pagadas como pagadas
            unpaid_invoices.write({'payment_state': 'paid'})


        xml_content += '    </PmtInf>\n'
        xml_content += '  </CstmrCdtTrfInitn>\n'
        xml_content += '</Document>'

        attachment = self.env['ir.attachment'].create({
            'name': f'cobros_alumnos_{fields.Date.today()}.xml',
            'type': 'binary',
            'datas': base64.b64encode(xml_content.encode('utf-8')).decode('utf-8'),
            'mimetype': 'application/xml',
            'res_model': 'member.dancer',
            'res_id': self[0].id if len(self) == 1 else None,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    
