import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(patient_id: str, age: int, metrics: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1A365D"), spaceAfter=15)
    body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=11, spaceAfter=8)
    
    story.append(Paragraph("<b>CLINICAL NEUROSCIENCE OUTCOME ANALYSIS BRIEF</b>", title_style))
    story.append(Paragraph(f"<b>Patient Identifier:</b> {patient_id} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Age:</b> {age} Years Old", body_style))
    story.append(Spacer(1, 10))
    
    data = [
        ["Clinical Marker / Risk Vector", "Assigned Value / Point Contribution"],
        ["Total Computed ASTRAL Score", f"{metrics['score']} Points"],
        ["Predicted 3-Month Unfavorable Outcome Probability", f"{metrics['probability']*100:.1f}%"],
        ["95% Statistical Confidence Boundary", f"[{metrics['ci_lower']*100:.1f}% - {metrics['ci_upper']*100:.1f}%]"]
    ]
    
    t = Table(data, colWidths=[300, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F7FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<i>Disclaimer: This document represents an automated predictive analysis model built for computational neuroscience portfolio review during the 2027 Residency Match cycle. Final management protocols must rely on direct board-certified neurological assessment.</i>", body_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
