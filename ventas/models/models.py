# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import *
from datetime import date


# class ventas(models.Model):
#     _name = 'ventas.ventas'
#     _description = 'ventas.ventas'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class cliente(models.Model):
    _name = 'ventas.cliente'
    _description = 'Caracteristicas de un cliente'

    dni = fields.Char(string = 'DNI', required = True, size = 8)
    nombre = fields.Char(string = 'Nombre', required = True, size = 30)
    fecha_nacimiento = fields.Date(string = 'Fecha de nacimiento', required = True)
    edad = fields.Integer(string = 'Edad', compute = '_get_edad')
    direccion = fields.Char(string = 'Direccion', required = True, size = 45)
    telefono = fields.Integer(string = 'Numero de telefono')
        
    factura_ids = fields.One2many('ventas.factura', 'cliente_id', string = 'Codigo factura')

    @api.constrains('dni')
    def _check_dni(self):
        if len(self.dni) != 9:
            raise ValidationError("Debes introducir un DNI valido")
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        if not self.dni.endsWith(letras[int(self.dni[:8]) % 23]):
            raise ValidationError("Debes introducir un DNI valido")

    @api.constrains('telefono')
    def _check_value(self):
        if self.telefono < 600000000 or self.telefono > 700000000:
            raise ValidationError("Debes introducir un valor entre 600 000 000 y 700 000 000")

    @api.depends('fecha_nacimiento')
    def _get_edad(self):
        for cliente in self:
            hoy = date.today()
            cliente.edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < self.fecha_nacimiento.month, self.fecha_nacimiento.day)

class factura(models.Model):
    _name = 'ventas.factura'
    _description = 'Caracteristicas de una factura'

    num_factura = fields.Integer(string = 'Numero de factura', required = True)
    fecha_emision = fields.Date(string = 'Fecha de emision', required = True)
    total = fields.Float(string = 'Importe total', digit = (6,2), required = True)

    cliente_id = fields.Many2one('ventas.cliente', string = 'Codigo cliente')
    producto_ids = fields.One2many('ventas.producto', 'factura_id', string = 'Codigo producto')

class producto(models.Model):
    _name = 'ventas.producto'
    _description = 'Caracteristicas de un producto'

    nombre = fields.Char(string = 'Nombre', required = True, size = 30)
    descripcion = fields.Char(string = 'Descripcion', required = True, size = 120)
    precio = fields.Float(string = 'Precio', required = True, digits = 2)
    stock = fields.Integer(string = 'Cantidad en stock', required = True)

    factura_id = fields.Many2one('ventas.factura', string = 'Codigo de factura')
    categoria_id = fields.Many2one('ventas.categoria', string = 'Codigo de categoria')
    proveedor_id = fields.Many2one('ventas.proveedor', string = 'Codigo de proveedor')

class categoria(models.Model):
    _name = 'ventas.categoria'
    _description = 'Caracteristicas de una categoria'
    
    nombre = fields.Selection(string = 'Categoria ', required = True,
            selection = [('o', 'ordenadores'), ('s','smartphones'), ('a','audiovisual'),
            ('p','perifericos'), ('t','televisores'), ('g','gaming')], default = 'o')

    producto_ids = fields.One2many('ventas.producto', 'categoria_id', string = 'Codigo producto')
    
class proveedor(models.Model):
    _name = 'ventas.proveedor'
    _description = 'Caracteristicas de un proveedor'

    nif = fields.Char(string = 'NIF', required = True, size = 30)
    nombre = fields.Char(string = 'Nombre', required = True, size = 30)
    direccion = fields.Char(string = 'Direccion', required = True, size = 45)
    telefono = fields.Integer(string = 'Numero de telefono')

    producto_ids = fields.One2many('ventas.producto', 'proveedor_id', string = 'Codigo producto')
    