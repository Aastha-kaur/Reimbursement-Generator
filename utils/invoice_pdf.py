import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_invoice_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header
    header = ParagraphStyle('Header', parent=styles['Heading2'], alignment=1, spaceAfter=10)
    story.append(Paragraph("CLINICAL TRIAL REIMBURSEMENT INVOICE", header))

    # Invoice Info Line
    story.append(Paragraph(f"Invoice no: INV-{data['visit_id']} | Issued to: {data['participant_name']} | Visit Date: {data.get('visit_date', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Participant & Reimbursement Details
    details = [
        ["Participant ID:", data['participant_id']],
        ["Participant Name:", data['participant_name']],
        ["Study:", data['study_name']],
        ["Visit Date:", str(data.get('visit_date', 'N/A'))],
        ["Transport Method:", data.get('transport_method', 'N/A')],
        ["Distance (km):", f"{data['distance']}"],
        ["Duration (hrs):", str(data.get('visit_duration', 'N/A'))],
        ["KM Reimbursement:", f"${data.get('km_reimbursement', 0.00):.2f}"],
        ["Meal Allowance:", f"${data.get('meal_allowance', 0.00):.2f}"],
        ["TOTAL REIMBURSEMENT:", f"${data['total_reimbursement']:.2f}"]
    ]
    table = Table(details, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Banking Info
    story.append(Paragraph("Banking Information:", styles['Heading3']))
    bank_info = [
        ["Bank Name:", data.get("bank_name", "N/A")],
        ["Account No:", data.get("account_no", "N/A")],
        ["BSB:", data.get("bsb", "N/A")],
        ["Account Name:", data.get("account_name", "N/A")]
    ]
    bank_table = Table(bank_info, hAlign='LEFT')
    bank_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f2f2f2")),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    story.append(bank_table)

    doc.build(story)
    buffer.seek(0)
    return buffer
