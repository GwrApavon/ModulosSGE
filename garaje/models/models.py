# -*- coding: utf-8 -*-

from odoo import models, fields, api

#hace falta para _get_annios(self)
from dateutil.relativedelta import *
from datetime import date



# class garaje(models.Model):
#     _name = 'garaje.garaje'
#     _description = 'garaje.garaje'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class aparcamiento(models.Model):
    _name = 'garaje.aparcamiento'
    _description = 'Características de un aparcamiento'

    name = fields.Char('Direccion', required = True)
    plazas = fields.Integer(string='Plazas', required = True)

    #Campos relacionales. En el padre tendríamos la colección de hijos y en hijo tendríamos la entidad padre
    #En un aparcamiento hay varios coches. Por convenio se utiliza nombreDeLaClase_id si es un solo objeto, o nombreDeLaClase_id si son varios objetos
    #La relación es oneToMany, porque un aparcamiento puede tener varios coches
    
    coche_ids = fields.One2many('garaje.coche', 'aparcamiento_id', string='field_name')


class coche(models.Model):
    _name='garaje.coche'
    _description = 'Características de un coche'
    _order = 'matricula' # Campo por defecto para buscar los datos

    matricula = fields.Char(string='Matrícula', required = True, size=7)
    modelo = fields.Char('Modelo', required =True )
    construido = fields.Date(string='Fecha de construcción')
    consumo = fields.Float('Consumo', (4,1)) #4 dígitos con un decimal.
    #El campo siguiente podría tener algo así como store=True, lo cual significaría que no se recalcularían los años del coche a no ser que se cambie la fecha de construcción
    annios = fields.Integer('Años', compute='_get_annios') #Este campo lo vamos a calcular nosotros, a partir de la fecha de construcción y la actual
    descripcion = fields.Text('Descripcion')
    averiado = fields.Boolean('Averiado')
    
    #Campos relacionales
    aparcamiento_id = fields.Many2one('garaje.aparcamiento', string='Aparcamiento')
    mantenimiento_ids = fields.Many2many('garaje.mantenimiento' , string="Mantenimientos")

    @api.depends('construido') #Cuando se modifique el parámetro construido en un objeto coche, automáticamente se lanazará esta función
    def _get_annios(self): # el self representa una colección de objetos, en este caso una colección de coches
        for coche in self: #Cuando ponemos una función definida a un modelo, el self representa una colección de objetos. 
        #Siempre está pensado para una colección de datos. Aunque yo elija una única entidad, me va a llegar una array con un único elemento
            hoy = date.today()
            coche.annios = relativedelta(hoy, coche.construido).years

        
class mantenimiento(models.Model):
    _name = 'garaje.mantenimiento'
    _description = 'Para mantenimientos rutinarios'
    _order = 'fecha' # Por la forma en la que está creado define de forma única un mantenimiento
    fecha = fields.Date('Fecha', required = True, default = fields.Date.today())
    tipo = fields. Selection (string = 'Tipo ', selection =[('l','lavar'),('r','revisión'),('m','mecánica'), ('p','pintura')], default='l')
    coste = fields.Float('Coste', (8,2), help='Coste total de mantenimeinto') # 5 números naturales más 2 decimales

    #Campos relacionales
    coche_ids = fields.Many2many('garaje.coche', string='Coches')


