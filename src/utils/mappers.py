from src.domain.invoices.entities.invoice import Invoice
from src.utils.formatters import colombian_number_format
from datetime import datetime


def invoice_to_template_context(invoice: Invoice) -> dict:
    """
    Transforma tu entidad de dominio Invoice en el dict
    que espera tu plantilla .docx (docxtpl).
    """
    return {
        "today": datetime.now().date(),
        "invoice": {
            "reference_code": invoice.reference_code,
            "observation": invoice.observation,
            "payment_method": invoice.payment_method_code,
            "total": colombian_number_format(invoice.total),
        },
        "customer": {
            "identification": invoice.customer.identification,
            "company": invoice.customer.company,
            "names": invoice.customer.names,
            "address": invoice.customer.address,
            "email": invoice.customer.email,
            "phone": invoice.customer.phone,
        },
        "items": [
            {
                "code_reference": item.code_reference,
                "name": item.name,
                "quantity": item.quantity,
                "price": colombian_number_format(item.price),
                "total": colombian_number_format(item.total),
            }
            for item in invoice.items
        ],
    }
