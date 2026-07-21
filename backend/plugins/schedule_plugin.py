"""Equipment schedule plugin for Keel.

Returns schedule comparison data (planned vs forecast delivery dates, variance,
origin, route, and alternative suppliers) as JSON for the agents.
"""

import json
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from utils import db as _db

COMPARISON_QUERY = """
SELECT
    p.project_id, p.project_name, p.project_code, p.project_country, p.project_location,
    eq.equipment_id, eq.equipment_code, eq.equipment_name, eq.equipment_type,
    wp.work_package_id, wp.work_package_code, wp.work_package_name,
    m.milestone_id, m.milestone_number, m.milestone_activity,
    ps.p6_schedule_due_date,
    ems.equipment_milestone_due_date,
    CAST(julianday(ems.equipment_milestone_due_date) - julianday(ps.p6_schedule_due_date) AS INTEGER) AS days_variance,
    CAST(julianday(ps.p6_schedule_due_date) - julianday(date('now')) AS INTEGER) AS days_until_p6_due,
    s.supplier_id, s.supplier_name, s.supplier_number,
    po.purchase_order_id, po.purchase_order_number, po.line_item, po.amount,
    es.lead_time_days AS supplier_lead_time,
    ml.location_address AS manufacturing_location,
    li.shipping_port, li.receiving_port, li.logistics_method,
    (
        SELECT GROUP_CONCAT(alt_s.supplier_name || ' (Cost: ' || es2.unit_cost ||
               ', Lead time: ' || es2.lead_time_days || ' days)', ', ')
        FROM dim_equipment_supplier es2
        JOIN dim_supplier alt_s ON es2.supplier_id = alt_s.supplier_id
        WHERE es2.equipment_id = eq.equipment_id AND es2.supplier_id != s.supplier_id
    ) AS alternative_suppliers
FROM fact_p6_schedule ps
JOIN fact_equipment_milestone_schedule ems
    ON ps.equipment_id = ems.equipment_id AND ps.milestone_id = ems.milestone_id
   AND ps.project_id = ems.project_id AND ps.work_package_id = ems.work_package_id
JOIN dim_project p       ON ps.project_id = p.project_id
JOIN dim_equipment eq    ON ps.equipment_id = eq.equipment_id
JOIN dim_work_package wp ON ps.work_package_id = wp.work_package_id
JOIN dim_milestone m     ON ps.milestone_id = m.milestone_id
JOIN fact_purchase_order po ON ems.purchase_order_id = po.purchase_order_id
JOIN dim_supplier s      ON po.supplier_id = s.supplier_id
LEFT JOIN dim_equipment_supplier es
    ON es.equipment_id = eq.equipment_id AND es.supplier_id = s.supplier_id
LEFT JOIN dim_manufacturing_location ml
    ON ml.equipment_id = eq.equipment_id AND ml.supplier_id = s.supplier_id
LEFT JOIN dim_logistics_info li
    ON li.equipment_id = eq.equipment_id AND li.supplier_id = s.supplier_id
WHERE m.milestone_id = 7
GROUP BY ps.p6_schedule_id
ORDER BY days_variance DESC;
"""


class EquipmentSchedulePlugin:
    """A plugin for working with equipment schedule data."""

    def __init__(self, connection_string=None):
        self.connection_string = connection_string

    @kernel_function(description="Retrieves equipment schedule comparison data")
    def get_schedule_comparison_data(self) -> str:
        """Retrieves schedule comparison data for analysis."""
        try:
            print("Called get_schedule_comparison_data")
            conn = _db.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute(COMPARISON_QUERY)
            results = [dict(row) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            print(f"Query returned {len(results)} rows")
            return json.dumps(results, default=str)
        except Exception as e:
            print(f"Error in get_schedule_comparison_data: {str(e)}")
            return json.dumps({"error": str(e)})
