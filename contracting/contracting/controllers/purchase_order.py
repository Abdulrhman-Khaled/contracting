import frappe 
from frappe import _

def validate_items_qty(doc,event):
    if not doc.contracting:
        return 
    
    for item in doc.get("items"):
        if not item.allowed_qty:
            continue
        
        if not item.qty:
            continue
        
        if item.qty > item.allowed_qty:
            frappe.throw(_("You can't exceed item qty in row {0}").format(item.idx))




def update_remaining_qty_on_submit(doc, method):
    if not doc.contracting:
        return 
    
    for item in doc.items:
        tot_qty = 0
        qty = frappe.get_value("Costing Note Merge Item", item.item_row, "remaining_qty")

        if not qty:
            tot_qty = item.qty
        else:
            tot_qty = float(qty) - item.qty
            
        if not qty:
            continue
  
        if item.qty > float(qty) :
            frappe.throw("You can't exceed document qty")

        frappe.db.set_value("Costing Note Merge Item", item.item_row, "remaining_qty", tot_qty)
        

def restore_qty_on_cancel_or_delete(doc, method):
    if not doc.contracting:
        return 
    
    for item in doc.items:
        tot_qty = 0
        qty = frappe.get_value("Costing Note Merge Item", item.item_row, "remaining_qty")

        if not qty:
            tot_qty = item.qty
        else:
            tot_qty =  float(qty) + item.qty
        
        frappe.db.set_value("Costing Note Merge Item", item.item_row, "remaining_qty", tot_qty)
