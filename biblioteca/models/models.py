# -*- coding: utf-8 -*-

from odoo import models, fields, api


class lector(models.Model):
    _name = 'biblioteca.lector'
    _description = 'Representa el lector de un libro'

    dni = fields.Char('Dni', required=True, size=7)
    nombre = fields.Char('Nombre', required=True)
    prestamos_ids = fields.One2many('biblioteca.prestamo', 'lector_id', string='lector-prestamo')


class prestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Representa el prestamo de un libro'

    identification = fields.Integer(string='Id', max=10) 
    fechaInicio = fields.Date(string='Fecha de inicio')
    fechaFin = fields.Date(string='Fecha de fin')
    lector_id = fields.Many2one('biblioteca.lector', string='prestamo-lector')


class libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Representa un libro'

    isbn = fields.Char('Isbn', required=True, size=17)
    titulo = fields.Char('Titulo', required=True)
    numeroDePaginas = fields.Integer(string='numero de paginas') 
    editorial_ids = fields.One2many('biblioteca.editorial', 'libro_id', string='libro-editorial')
    autor_ids = fields.Many2many('biblioteca.autor', string='libro-autor')
   

class editorial(models.Model):
    _name = 'biblioteca.editorial'
    _description = 'Representa la editorial de un libro'
    
    nombre = fields.Char('Nombre', required=True)
    libro_id = fields.Many2one('biblioteca.libro', string='editorial-libro')


class autor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Representa un autor'

    dni = fields.Char('Dni_autor', required=True, size=7)
    nombre = fields.Char('Nombre', required=True)
    nacimiento = fields.Date(string='Fecha de nacimiento del autor')
    edad = fields.Integer(string='Edad', compute='calculaEdad')
    libro_ids = fields.Many2many('biblioteca.libro', string='autor-libro')

    @api.depends
    def calculaEdad(self):
        for autor in self:
            #calculamos edad
            pass


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100