# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError  

class CSRDepartment(models.Model):
    _name = 'csr.department'
    _description = 'CSR Departmental Carbon Budget'
    _rec_name = 'department_id'

    department_id = fields.Many2one('hr.department', string="HR Department", required=True, ondelete='cascade', index=True)
    
    name = fields.Char(related='department_id.name', readonly=True, store=False)

    # Carbon Budget Fields
    carbon_budget = fields.Float(string="Annual Carbon Budget (kg)", default=10000.0, help="The maximum CO2 budget allocated to this department.")
    
    total_carbon_offset = fields.Float(
        string="Total Carbon Offset (kg)",  
        compute='_compute_carbon_metrics',  
        store=True,  
        help="Sum of carbon offsets from all approved activities by employees in this department."
    )
    
    carbon_used = fields.Float(
        string="Simulated Carbon Used (kg)",  
        compute='_compute_carbon_metrics',  
        store=True,  
        help="Simulated metric for carbon usage (e.g., 50% of offset is used as a placeholder for actual usage)."
    )
    
    budget_usage_percentage = fields.Float(
        string="Budget Usage (%)",  
        compute='_compute_carbon_metrics',  
        store=True
    )

    @api.depends('carbon_budget')
    def _compute_carbon_metrics(self):
        
        # --- THIS IS THE FIX ---
        # 1. Switched from internal '_read_group' to public 'read_group'.
        # 2. Changed 'aggregates' to 'fields' and added ':sum' (the Odoo 19.0 way).
        # 3. Added 'lazy=False' to ensure the query runs correctly.
        #
        # 'read_group' IS GUARANTEED to return a list of dictionaries,
        # which makes the dictionary comprehension code below (line 59) work.
        
        activity_data = self.env['csr.activity'].read_group(
            domain=[('status', '=', 'approved'), ('department_id', 'in', self.department_id.ids)],
            fields=['carbon_offset_estimate:sum'],  # <-- FIX 2
            groupby=['department_id'],
            lazy=False  # <-- FIX 3
        )
        
        # This line (line 59) will now work, because 'data' is a dict.
        # data['department_id'] will be a tuple like (5, 'Sales')
        offset_map = {data['department_id'][0]: data['carbon_offset_estimate'] for data in activity_data if data['department_id']}

        for dept in self:
            # Get the offset from our map, defaulting to 0.0
            offset = offset_map.get(dept.department_id.id, 0.0)
            
            dept.total_carbon_offset = offset
            
            # Simulate carbon usage as 50% of the offset (as per your plan)
            dept.carbon_used = offset * 0.5 
            
            if dept.carbon_budget > 0:
                dept.budget_usage_percentage = (dept.carbon_used / dept.carbon_budget) * 100
            else:
                dept.budget_usage_percentage = 0.0

    @api.constrains('department_id')
    def _check_department_id_unique(self):
        for record in self:
            if self.search_count([('department_id', '=', record.department_id.id), ('id', '!=', record.id)]) > 0:
                raise ValidationError('A CSR Department record already exists for this HR Department.')