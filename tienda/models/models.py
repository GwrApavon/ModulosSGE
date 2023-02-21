# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from enum import Enum
from odoo import models, fields, api

class cliente(models.Model):
    _name = 'tienda.cliente'
    _description = 'Características de un cliente'

    id_ltr = fields.Char('DNI', required = True)
    name = fields.Char('Nombre', required = True)
    b_date = fields.Date('Fecha de nacimiento')
    age = fields.Integer('Edad', compute = 'ageCalculator')
    address = fields.Char('Dirección')
    phone_number = fields.Integer('Telefono', required =  True)
    bills_id = fields.One2many('tienda.factura', 'client_id', 'cliente-facturas')
    @api.depends("b_date")
    def ageCalculator(self):
        for cliente in self:
            hoy = date.today()
            cliente.age = relativedelta(hoy, cliente.b_date).years
    @api.constrains("phone_number")
    def _check_phone_number(self):
        for record in self:
            if record.phone_number < 600000000 or record.phone_number > 700000000:
                raise ValidationError("Error al intrudcir el telefono")

class factura(models.Model):
    _name = 'tienda.factura'
    _description = "Facturas de una tienda"

    bill_num = fields.Integer('Número de Factura', required = True)
    emission_date = fields.Date('Fecha de emision', required = True)
    total = fields.Float('Suma total', (4,2),  required = True)
    client_id = fields.Many2one('tienda.cliente', 'facturas-cliente')
    products_id = fields.One2many('tienda.producto', 'bills_id','factura-prodcutos')

class producto(models.Model):
    _name = 'tienda.producto'
    _description = 'Productos de una tienda'

    id = fields.Integer('ID', required = True, size = 4)
    name = fields.Char('Nombre', required =True)
    description = fields.Char('Descripción')
    price = fields.Float('Precio', required = True)
    stock = fields.Integer('Stock', required = True)
    bills_id = fields.Many2one('tienda.factura', 'producto-facturas')
    supplier_id = fields.Many2one('tienda.proveedor', 'productos-proveedor')
    categorie_id = fields.Many2one('tienda.categoria','prodcutos-categoria')

class categoria(models.Model): 
    _name = 'tienda.categoria'
    _description = 'categorias de los productos de una tienda'

    name = fields. Selection(string ='Nombre ', selection =[('o','Ordenadores'), ('s','Smartphones'), ('a','Audiovisual'), ('p','Perifericos'), ('t','Televisores'), ('g','Gaming')], default='o')

    product_id = fields.One2many('tienda.producto', 'categorie_id', 'categoria-prodcutos')

class proveedor(models.Model): 
    _name = 'tienda.proveedor'
    _description = 'proveedores de una tienda'

    id_ltr = fields.Char('DNI', requiered = True ,store = True)        
    name = fields.Char('Nombre', required = True)
    address = fields.Char('Direccion')
    phone_number = fields.Integer('Telefono', required =  True)    
    product_id = fields.One2many('tienda.producto', 'supplier_id', 'proveedor-prodcutos')
    @api.constrains("phone_number")
    def _check_phone_number(self):
        for record in self:
            if record.phone_number < 600000000 or record.phone_number > 700000000:
                raise ValidationError("Error al intrudcir el telefono")



    