"""
Offline Application Form Generator - Creates PDF application forms
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

class ApplicationFormGenerator:
    """Generate PDF application forms for offline submission"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=8,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='FieldLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold'
        ))
    
    def generate_form(self, output_path=None):
        """Generate application form PDF"""
        buffer = io.BytesIO() if output_path is None else output_path
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Header
        story.append(Paragraph("SKL UNIVERSITI", self.styles['Title']))
        story.append(Paragraph("OFFLINE APPLICATION FORM", self.styles['Title']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%d %B %Y')}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Personal Information Section
        story.append(Paragraph("1. PERSONAL INFORMATION", self.styles['SectionHeader']))
        
        personal_data = [
            ['Full Name (as per IC/Passport):', '________________________________________________'],
            ['', ''],
            ['IC/Passport Number:', '________________________________________________'],
            ['', ''],
            ['Date of Birth (DD/MM/YYYY):', '________ / ________ / ________'],
            ['', ''],
            ['Gender:', '☐ Male  ☐ Female  ☐ Other'],
            ['', ''],
            ['Nationality:', '________________________________________________'],
            ['', ''],
            ['Email Address:', '________________________________________________'],
            ['', ''],
            ['Phone Number:', '________________________________________________'],
            ['', ''],
            ['Mailing Address:', ''],
            ['', '________________________________________________'],
            ['', '________________________________________________'],
            ['', '________________________________________________'],
            ['', ''],
        ]
        
        personal_table = Table(personal_data, colWidths=[2.5*inch, 4*inch])
        personal_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(personal_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Academic Information Section
        story.append(Paragraph("2. ACADEMIC INFORMATION", self.styles['SectionHeader']))
        
        academic_data = [
            ['Level of Study:', '☐ Foundation  ☐ Diploma  ☐ Bachelor  ☐ Master  ☐ PhD'],
            ['', ''],
            ['Program Applied For:', '________________________________________________'],
            ['', ''],
            ['Faculty:', '________________________________________________'],
            ['', ''],
            ['Intake Semester:', '☐ Semester 1  ☐ Semester 2  ☐ Semester 3'],
            ['', ''],
            ['Academic Year:', '_____________'],
            ['', ''],
        ]
        
        academic_table = Table(academic_data, colWidths=[2.5*inch, 4*inch])
        academic_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(academic_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Educational Background Section
        story.append(Paragraph("3. EDUCATIONAL BACKGROUND", self.styles['SectionHeader']))
        story.append(Paragraph("Highest Qualification:", self.styles['FieldLabel']))
        
        education_data = [
            ['Qualification:', '________________________________________________'],
            ['', ''],
            ['Institution:', '________________________________________________'],
            ['', ''],
            ['Year of Completion:', '_____________'],
            ['', ''],
            ['CGPA/Grade:', '________________________________________________'],
            ['', ''],
        ]
        
        education_table = Table(education_data, colWidths=[2.5*inch, 4*inch])
        education_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(education_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Additional Information Section
        story.append(Paragraph("4. ADDITIONAL INFORMATION", self.styles['SectionHeader']))
        
        additional_data = [
            ['English Proficiency:', '☐ IELTS  ☐ TOEFL  ☐ MUET  ☐ Other: _____________'],
            ['', ''],
            ['Score:', '________________________________________________'],
            ['', ''],
            ['Special Needs/Requirements:', ''],
            ['', '________________________________________________'],
            ['', '________________________________________________'],
            ['', ''],
        ]
        
        additional_table = Table(additional_data, colWidths=[2.5*inch, 4*inch])
        additional_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(additional_table)
        story.append(PageBreak())
        
        # Declaration Section
        story.append(Paragraph("5. DECLARATION", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.1*inch))
        
        declaration_text = """
        I hereby declare that:
        <br/><br/>
        1. All information provided in this application form is true and accurate to the best of my knowledge.
        <br/><br/>
        2. I understand that any false or misleading information may result in the rejection of my application or termination of my enrollment.
        <br/><br/>
        3. I have read and understood the admission requirements and agree to comply with all university policies and regulations.
        <br/><br/>
        4. I authorize the university to verify the information provided and to contact relevant institutions if necessary.
        <br/><br/>
        5. I consent to the processing of my personal data for admission purposes.
        """
        
        story.append(Paragraph(declaration_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        signature_data = [
            ['Applicant Signature:', '________________________________________________'],
            ['', ''],
            ['Date:', '________ / ________ / ________'],
            ['', ''],
        ]
        
        signature_table = Table(signature_data, colWidths=[2.5*inch, 4*inch])
        signature_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(signature_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Instructions
        story.append(Paragraph("6. SUBMISSION INSTRUCTIONS", self.styles['SectionHeader']))
        instructions_text = """
        <b>Please submit this completed form along with the following documents:</b>
        <br/><br/>
        • Certified copies of academic certificates and transcripts
        <br/>
        • Copy of IC/Passport
        <br/>
        • Passport-sized photographs (2 copies)
        <br/>
        • English proficiency test results (if applicable)
        <br/>
        • Application fee payment receipt (RM 50)
        <br/><br/>
        <b>Submission Methods:</b>
        <br/><br/>
        1. <b>In Person:</b> Submit to the Admission Office during office hours (Mon-Fri, 9AM-5PM)
        <br/>
        2. <b>By Mail:</b> Send to: Admission Office, SKL Universiti, [Address]
        <br/>
        3. <b>Email:</b> Scan and email to: admission@skl.edu.my
        <br/><br/>
        <b>Contact Information:</b>
        <br/>
        Phone: +60-3-1234-5678
        <br/>
        Email: admission@skl.edu.my
        <br/>
        Website: www.skl.edu.my
        """
        
        story.append(Paragraph(instructions_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        if output_path is None:
            buffer.seek(0)
            return buffer
        
        return output_path

