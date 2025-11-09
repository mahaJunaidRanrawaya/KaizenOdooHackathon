# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError 
from dateutil.relativedelta import relativedelta
import logging 

_logger = logging.getLogger(__name__)

class CSREmployeeProfile(models.Model):
    _name = 'csr.employee.profile'
    _description = 'CSR Employee Profile Extension'
    _order = "total_impact_points desc"
    
    _inherit = ['mail.thread']  

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    
    department_id = fields.Many2one(related='employee_id.department_id', store=True, readonly=True)
    name = fields.Char(related='employee_id.name', readonly=True, store=True)
    image_128 = fields.Image(related='employee_id.image_128', string="Image 128", readonly=True)
    
    total_impact_points = fields.Integer(string="Total Impact Points", default=0, compute='_compute_csr_metrics', store=True)
    volunteering_hours = fields.Float(string="Total Volunteering Hours", default=0.0, compute='_compute_csr_metrics', store=True)
    donation_amount = fields.Monetary(string="Total Donation Amount", default=0.0, compute='_compute_csr_metrics', store=True, currency_field='company_currency_id')
    company_currency_id = fields.Many2one(related='employee_id.company_id.currency_id', string='Company Currency', readonly=True)
    
    activity_ids = fields.One2many('csr.activity', 'employee_profile_id', string="CSR Activities")
    
    rank_display = fields.Char(string="Current Rank (Total Points)", compute='_compute_rank', store=False)
    improvement_rank_display = fields.Char(string="Rank (Improvement)", compute='_compute_rank', store=False)
    
    last_quarter_points = fields.Integer(string="Last Quarter Points", compute='_compute_last_quarter_points', store=True)
    point_improvement = fields.Integer(string="Point Improvement", compute='_compute_point_improvement', store=True)
    
    @api.depends('activity_ids.status', 'activity_ids.impact_points', 'activity_ids.hours', 'activity_ids.donation_amount')
    def _compute_csr_metrics(self):
        for employee_profile in self:
            approved_activities = employee_profile.activity_ids.filtered(lambda r: r.status == 'approved')
            employee_profile.volunteering_hours = sum(approved_activities.mapped('hours'))
            employee_profile.donation_amount = sum(approved_activities.mapped('donation_amount'))
            employee_profile.total_impact_points = sum(approved_activities.mapped('impact_points'))

    @api.depends('activity_ids.date', 'activity_ids.impact_points', 'activity_ids.status')
    def _compute_last_quarter_points(self):
        today = fields.Date.today()
        end_date = today - relativedelta(days=90)
        start_date = today - relativedelta(days=180)

        for employee_profile in self:
            last_quarter_activities = employee_profile.activity_ids.filtered(lambda r: r.status == 'approved' and r.date and start_date <= r.date < end_date)
            employee_profile.last_quarter_points = sum(last_quarter_activities.mapped('impact_points'))

    @api.depends('total_impact_points', 'last_quarter_points')
    def _compute_point_improvement(self):
        for employee_profile in self:
            employee_profile.point_improvement = employee_profile.total_impact_points - employee_profile.last_quarter_points

    @api.depends('activity_ids.status', 'activity_ids.impact_points', 'activity_ids.date')
    def _compute_rank(self):
        self._compute_csr_metrics()
        self._compute_last_quarter_points()
        self._compute_point_improvement()
        
        sorted_profiles_total = self.env['csr.employee.profile'].search([], order='total_impact_points desc')
        rank_map_total = {profile.id: rank + 1 for rank, profile in enumerate(sorted_profiles_total)}
        
        sorted_profiles_improvement = self.env['csr.employee.profile'].search([], order='point_improvement desc')
        rank_map_improvement = {profile.id: rank + 1 for rank, profile in enumerate(sorted_profiles_improvement)}
        
        for profile in self:
            profile.rank_display = f"#{rank_map_total.get(profile.id, 'N/A')}"
            profile.improvement_rank_display = f"#{rank_map_improvement.get(profile.id, 'N/A')}"
            
    @api.constrains('employee_id')
    def _check_employee_id_unique(self):
        for record in self:
            if self.search_count([('employee_id', '=', record.employee_id.id), ('id', '!=', record.id)]) > 0:
                raise ValidationError('An employee can only have one CSR Profile.')

    def action_redeem_reward(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Redeem Rewards'),
            'res_model': 'csr.reward',
            'view_mode': 'kanban',
            'domain': [('is_active', '=', True)],
            'target': 'new',
        }
    
    def action_view_activities(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('My Activities'),
            'res_model': 'csr.activity',
            'view_mode': 'list,form',
            'domain': [('employee_profile_id', '=', self.id)],
            'context': {
                'default_employee_profile_id': self.id,
                'default_employee_id': self.employee_id.id
            }
        }
        
    # --- MODIFIED: This function now calls the central utility file ---
    def action_share_on_linkedin(self):
        self.ensure_one()
        
        # 1. Call the central utility function to get the simulated message
        message = self.env['csr.utils'].simulate_linkedin_share(self)
        
        # 2. Return the success notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('LinkedIn Share (Simulated)'),
                'message': _("Successfully posted to LinkedIn: '%s'") % message,
                'sticky': True, 
                'type': 'success',
            }
        }