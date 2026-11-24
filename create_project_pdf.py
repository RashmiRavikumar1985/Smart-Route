"""
Generate Professional Project Summary PDF for Smart Route
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus import Table, TableStyle, Flowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        self.drawRightString(letter[0] - 0.75*inch, 0.5*inch,
                            f"Page {self._pageNumber} of {page_count}")

def create_project_pdf():
    """Generate a professional 2-page project summary PDF"""
    
    output_file = "Smart_Route_Project_Summary.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                           leftMargin=0.75*inch, rightMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    story = []
    
    # Define custom styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1565C0'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#424242'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1565C0'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=5,
        leftIndent=20,
        bulletIndent=10,
        leading=13
    )
    
    # Title
    story.append(Paragraph("SMART ROUTE", title_style))
    story.append(Paragraph("AI-Powered Traffic Signal Optimization System", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Project Overview
    story.append(Paragraph("PROJECT OVERVIEW", heading_style))
    overview_text = """
    Smart Route is an intelligent and adaptive traffic signal control system that integrates 
    computer vision, reinforcement learning, and traffic simulation to overcome the limitations 
    of conventional fixed-time traffic signals. The system dynamically adjusts traffic signal 
    phases based on real-time traffic conditions, aiming to reduce congestion, waiting time, 
    fuel consumption, and emissions.
    """
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Problem Statement
    story.append(Paragraph("PROBLEM STATEMENT", heading_style))
    problem_text = """
    Traditional traffic signal systems operate using fixed signal timings and lack real-time 
    adaptability. Such systems fail to respond effectively to fluctuating traffic demand, 
    leading to congestion, increased waiting time, fuel wastage, and pollution—especially 
    in heterogeneous traffic environments.
    """
    story.append(Paragraph(problem_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # System Architecture
    story.append(Paragraph("SYSTEM ARCHITECTURE", heading_style))
    
    story.append(Paragraph("1. Perception Layer", subheading_style))
    story.append(Paragraph("• Uses YOLOv8 for vehicle detection and traffic density estimation", bullet_style))
    story.append(Paragraph("• Converts raw visual/simulation data into numerical traffic states", bullet_style))
    
    story.append(Paragraph("2. Decision Layer", subheading_style))
    story.append(Paragraph("• Uses Reinforcement Learning (PPO as primary algorithm)", bullet_style))
    story.append(Paragraph("• Observes traffic state and selects optimal signal phase actions", bullet_style))
    story.append(Paragraph("• Learns policies that minimize waiting time and congestion", bullet_style))
    
    story.append(Paragraph("3. Simulation & Control Layer", subheading_style))
    story.append(Paragraph("• SUMO (Simulation of Urban Mobility) simulates real-world traffic", bullet_style))
    story.append(Paragraph("• TraCI enables real-time control of traffic signals from Python", bullet_style))
    story.append(Paragraph("• Returns reward and next state to the learning agent", bullet_style))
    story.append(Spacer(1, 0.15*inch))
    
    # RL Formulation
    story.append(Paragraph("REINFORCEMENT LEARNING FORMULATION", heading_style))
    
    rl_data = [
        ['Component', 'Description'],
        ['State (S)', 'Vehicle count per lane, queue length, waiting time, current signal phase'],
        ['Action (A)', 'Selection of traffic signal phase (e.g., North-South green, East-West green)'],
        ['Reward (R)', 'Negative waiting time and queue length to encourage smooth traffic flow'],
    ]
    
    rl_table = Table(rl_data, colWidths=[1.5*inch, 4.5*inch])
    rl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(rl_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Page Break
    story.append(PageBreak())
    
    # Algorithms Used
    story.append(Paragraph("ALGORITHMS USED", heading_style))
    story.append(Paragraph("• <b>PPO (Proximal Policy Optimization)</b> – Primary algorithm (stable & efficient)", bullet_style))
    story.append(Paragraph("• <b>DQN (Deep Q-Network)</b> – Baseline comparison", bullet_style))
    story.append(Paragraph("• <b>A2C (Advantage Actor-Critic)</b> – Performance comparison", bullet_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Tools & Technologies
    story.append(Paragraph("TOOLS & TECHNOLOGIES", heading_style))
    
    tech_data = [
        ['Category', 'Technology'],
        ['Simulator', 'SUMO (Simulation of Urban Mobility)'],
        ['Interface', 'TraCI (Traffic Control Interface)'],
        ['RL Framework', 'Stable-Baselines3'],
        ['Computer Vision', 'YOLOv8 (Ultralytics)'],
        ['Programming', 'Python 3.11'],
        ['Visualization', 'TensorBoard, Matplotlib'],
    ]
    
    tech_table = Table(tech_data, colWidths=[2*inch, 4*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Key Results
    story.append(Paragraph("KEY RESULTS & OBSERVATIONS", heading_style))
    story.append(Paragraph("• PPO learns adaptive signal control strategies effectively", bullet_style))
    story.append(Paragraph("• Reduced average waiting time compared to fixed-time control", bullet_style))
    story.append(Paragraph("• Stable learning behavior observed through TensorBoard metrics", bullet_style))
    story.append(Paragraph("• System adapts dynamically to changing traffic conditions", bullet_style))
    story.append(Paragraph("• Real-time decision making with 5-second action intervals", bullet_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Future Scope
    story.append(Paragraph("FUTURE SCOPE", heading_style))
    story.append(Paragraph("• Multi-intersection coordination using Multi-Agent PPO", bullet_style))
    story.append(Paragraph("• Integration with real-world CCTV feeds", bullet_style))
    story.append(Paragraph("• Emergency vehicle prioritization", bullet_style))
    story.append(Paragraph("• Accident and road-hazard awareness", bullet_style))
    story.append(Paragraph("• Deployment on edge devices (Jetson / Raspberry Pi)", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Project Structure
    story.append(Paragraph("PROJECT STRUCTURE", heading_style))
    structure_text = """
    <b>Smart-Route/</b><br/>
    ├── sumo_env/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # SUMO network, routes, configuration<br/>
    ├── yolo/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # YOLOv8 vehicle detection module<br/>
    ├── models/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Trained RL models (PPO, DQN, A2C)<br/>
    ├── outputs/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Training logs, CSVs, plots<br/>
    ├── train_all.py &nbsp;&nbsp;&nbsp;&nbsp; # Complete training pipeline<br/>
    ├── train_ppo.py &nbsp;&nbsp;&nbsp;&nbsp; # PPO training script<br/>
    ├── evaluate_gui.py &nbsp; # Visual simulation with trained model<br/>
    └── generate_plots.py # Performance visualization<br/>
    """
    story.append(Paragraph(structure_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # How to Run
    story.append(Paragraph("HOW TO RUN", heading_style))
    story.append(Paragraph("<b>1. Setup Environment:</b>", body_style))
    story.append(Paragraph("conda create -n smart_route python=3.9", bullet_style))
    story.append(Paragraph("conda activate smart_route", bullet_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>2. Install Dependencies:</b>", body_style))
    story.append(Paragraph("pip install -r requirements.txt", bullet_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>3. Train the Model:</b>", body_style))
    story.append(Paragraph("python train_ppo.py", bullet_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>4. View Training Metrics:</b>", body_style))
    story.append(Paragraph("tensorboard --logdir runs", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Footer with metadata
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"""
    <b>Smart Route</b> | AI-Powered Traffic Signal Optimization<br/>
    Generated on {datetime.now().strftime("%B %d, %Y")}
    """
    story.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ PDF created successfully: {output_file}")
    return output_file

if __name__ == "__main__":
    create_project_pdf()
