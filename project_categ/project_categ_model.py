# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Daniel Reis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'
    task_categ_id = fields.Many2one(comodel_name='project.category',
                                    string='Root Category for Tasks')

class ProjectCategory(models.Model):
    _name = 'project.category'
    _order = 'parent_id,name'

    @api.multi
    def _name_get(self):
        return [(obj.id, obj.parent_id.name + ' / ' or '' + obj.name)
                for obj in self]

    @api.multi
    def _name_get_fnc(self):
        for obj in self:
            obj.complete_name = obj._name_get()

    name = fields.Char(string='Name')
    project_id = fields.Many2one(comodel_name='project.project',
                                 string='Project')
    parent_id = fields.Many2one(comodel_name='project.category',
                                string='Parent Category', index=True)
    child_ids = fields.One2many(comodel_name='project.category',
                                inverse_name='parent_id',
                                string='Child Categories')
    complete_name = fields.Char(compute='_name_get_fnc', string='Name')
    code = fields.Char(string='Code', size=10)


class ProjectTask(models.Model):
    _inherit = 'project.task'
    # TODO check if this code is still necessary
    # def onchange_project(self, cr, uid, id, project_id, context=None):
    #     # on_change is necessary to populate fields on create, before saving
    #     try:
    #         res = super(ProjectTask, self).onchange_project(
    #             cr, uid, id, project_id, context) or {}
    #     except AttributeError:
    #         res = {}
    #
    #     if project_id:
    #         obj = self.pool.get('project.project').browse(
    #             cr, uid, project_id, context=context)
    #         if obj.task_categ_id:
    #             res.setdefault('value', {})
    #             res['value']['task_categ_id'] = obj.task_categ_id.id
    #     return res
    task_categ_id = fields.Many2one(comodel_name='project.category',
                                    string='Category Root',
                                    related='project_id.task_categ_id',
                                    readonly=True)
    categ_ids = fields.Many2many(comodel_name='project.category',
                                 string='Tags',
                                 domain="[('id','child_of',task_categ_id),"
                                        "('id','!=',task_categ_id)]")
