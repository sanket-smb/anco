
__version__ = '0.0.1'
import frappe
import json
from frappe.utils import strip_html_tags

@frappe.whitelist()
def push_issue(name):
	setting = frappe.get_doc("On My Way Setting")
	doc = frappe.get_doc("Issue", name)
	item = []
	for i in doc.air_conditioner:
		dict = {}
		dict["air_conditioner_type"] = i.air_conditioner_type
		dict["model"] = i.model
		dict["number"] =i.number
		item.append(dict)
	import requests
	url = setting.site_url.strip()+"api/addTask?api_key={1}&token={0}".format(setting.api_token.strip(), setting.api_key.strip())
	payload={
		""
		"trans_type":"Maintenance",
		"issue_number": doc.name,
		"issue_type": doc.issue_type,
		"restaurant_name": doc.subject,
		"contract_number": doc.contract,
		"task_description": strip_html_tags(doc.description),
		"customer_name": doc.customer or ''+" " + doc.last_name or '',
		"raised_by_contact_no": doc.raised_by_number,
		"raised_by_contact": doc.raised_by_contact,
		"dropoff_contact_name": doc.raised_by_contact,
		"contact_number": doc.contact_number,
		"paci_no": doc.paci_number,
		"address": doc.address,
		"delivery_address": doc.address,
		"location_link": doc.location,
		'order_product_details': json.dumps(item),
	}
	files=[]
	headers = {}
	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	msg = json.loads(response.text[1:-1])
#	frappe.db.sql("""update `tabSales Order` set omw_order_id=\'{0}\' where docstatus!=2 and reference_num=\'{1}\'""".format(msg["details"], doc.reference_num))
	#frappe.db.set_value("Issue", name, "omw_order_id", msg["details"])
	res = {}
	if response.status_code == 200:
		status = msg["msg"]
		res['status'] = True
		res['id'] = msg["details"]
	else:
		res['status'] = False
		res['error'] = msg
	return res
