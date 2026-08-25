import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(lat, lon, elevation, slope, score, status, depth_m, depth_ft, risk):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1E3A8A'))
    story.append(Paragraph("Groundwater AI Hydrogeological Survey Report", title_style))
    story.append(Spacer(1, 12))
    
    data = [
        ["Parameter", "Value"],
        ["Latitude", f"{lat:.5f}"],
        ["Longitude", f"{lon:.5f}"],
        ["Terrain Elevation", f"{elevation} meters"],
        ["Terrain Slope Angle", f"{slope} degrees"],
        ["Est. Water Depth (Feet)", f"{depth_ft} ft"],
        ["Est. Water Depth (Meters)", f"{depth_m} m"],
        ["Drilling Feasibility", risk],
        ["Infiltration Score", f"{score}%"],
        ["Assessment Result", status]
    ]
    
    table = Table(data, colWidths=[200, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Geological Summary & Recommendation:</b>", styles['Heading3']))
    rec_text = f"Target area evaluated at {depth_ft} ft estimated depth. Feasibility status is '{risk}'. Recommended to verify sub-surface rock fracture mapping before drilling."
    story.append(Paragraph(rec_text, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer