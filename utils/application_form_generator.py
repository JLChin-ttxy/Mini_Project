"""
Offline Application Form Generator - Creates PDF application forms
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import os


class ApplicationFormGenerator:
    """Generate PDF application forms for offline submission"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Use unique style names to avoid clashing with default styles
        self.styles.add(
            ParagraphStyle(
                name="FormTitle",
                parent=self.styles["Heading1"],
                fontSize=18,
                textColor=colors.HexColor("#1e3a8a"),
                spaceAfter=6,
                alignment=TA_CENTER,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="FormSubtitle",
                parent=self.styles["Normal"],
                fontSize=10,
                leading=12,
                textColor=colors.HexColor("#111827"),
                spaceAfter=2,
                alignment=TA_LEFT,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=13,
                textColor=colors.HexColor("#ffffff"),
                backColor=colors.HexColor("#1e3a8a"),
                spaceAfter=4,
                spaceBefore=12,
                leftIndent=4,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="FieldLabel",
                parent=self.styles["Normal"],
                fontSize=9,
                fontName="Helvetica-Bold",
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="FieldValue",
                parent=self.styles["Normal"],
                fontSize=9,
            )
        )

    def _build_header(self, story):
        """Build the header: title row, then logo + contact info aligned in one row"""
        # First row: big title only
        story.append(Paragraph("Offline Application Form", self.styles["FormTitle"]))
        story.append(Spacer(1, 0.1 * inch))

        # Try to load logo from static folder
        logo_path = os.path.join(
            os.path.dirname(__file__), "..", "static", "images", "SKL logo.png"
        )
        logo_elem = None
        if os.path.exists(logo_path):
            try:
                # Slightly smaller logo so it lines up nicely with text
                logo_elem = Image(logo_path, width=1.4 * inch, height=1.4 * inch)
            except Exception:
                logo_elem = None

        # Second row: logo on the left, info on the right
        info_lines = [
            "SKL University",
            "123, Jalan Bandar Timah, 31900 Kampar Perak.",
            "Phone: +60-3-1234-5678",
            "Email: SKL123@edu.my",
        ]
        info_para = Paragraph("<br/>".join(info_lines), self.styles["FormSubtitle"])

        if logo_elem:
            header_table_data = [[logo_elem, info_para]]
            col_widths = [1.8 * inch, 5.2 * inch]
        else:
            header_table_data = [[info_para]]
            col_widths = [7.0 * inch]

        header_table = Table(header_table_data, colWidths=col_widths)
        header_table.setStyle(
            TableStyle(
                [
                    # Vertically center logo and text so they share the same row nicely
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )

        story.append(header_table)
        story.append(Spacer(1, 0.25 * inch))

    def _build_section_table(self, title, rows):
        """Helper to build a nicely boxed grid section"""
        # Section title as a full-width row
        section_title = Paragraph(title, self.styles["SectionHeader"])
        data = [[section_title]]
        table = Table(data, colWidths=[7.0 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BOX", (0, 0), (-1, 0), 1, colors.HexColor("#1e3a8a")),
                ]
            )
        )

        # Fields grid below the header
        field_table = Table(rows, colWidths=[2.5 * inch, 4.5 * inch])
        field_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        return table, field_table

    def generate_form(self, output_path=None):
        """Generate application form PDF"""
        buffer = io.BytesIO() if output_path is None else output_path

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        story = []

        # Header with logo and contact info
        self._build_header(story)

        # 1. PERSONAL INFORMATION
        personal_rows = [
            [
                Paragraph("Full Name (as per IC/Passport):", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("IC/Passport Number:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Date of Birth (DD/MM/YYYY):", self.styles["FieldLabel"]),
                Paragraph("________ / ________ / ________", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Gender:", self.styles["FieldLabel"]),
                Paragraph(
                    "☐ Male    ☐ Female    ☐ Other", self.styles["FieldValue"]
                ),
            ],
            [
                Paragraph("Nationality:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Email Address:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Phone Number:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Mailing Address:", self.styles["FieldLabel"]),
                Paragraph(
                    "______________________________________________<br/>"
                    "______________________________________________<br/>"
                    "______________________________________________",
                    self.styles["FieldValue"],
                ),
            ],
        ]
        p_header, p_table = self._build_section_table(
            "1. PERSONAL INFORMATION", personal_rows
        )
        story.append(p_header)
        story.append(p_table)
        story.append(Spacer(1, 0.2 * inch))

        # 2. ACADEMIC INFORMATION
        academic_rows = [
            [
                Paragraph("Level of Study:", self.styles["FieldLabel"]),
                Paragraph(
                    "☐ Foundation    ☐ Diploma    ☐ Bachelor    ☐ Master    ☐ PhD",
                    self.styles["FieldValue"],
                ),
            ],
            [
                Paragraph("Program Applied For:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Faculty:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Intake Semester:", self.styles["FieldLabel"]),
                Paragraph(
                    "☐ Semester 1    ☐ Semester 2    ☐ Semester 3",
                    self.styles["FieldValue"],
                ),
            ],
            [
                Paragraph("Academic Year:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
        ]
        a_header, a_table = self._build_section_table(
            "2. ACADEMIC INFORMATION", academic_rows
        )
        story.append(a_header)
        story.append(a_table)
        story.append(Spacer(1, 0.2 * inch))

        # 3. EDUCATIONAL BACKGROUND
        edu_rows = [
            [
                Paragraph("Highest Qualification:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Institution:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Year of Completion:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("CGPA/Grade:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
        ]
        e_header, e_table = self._build_section_table(
            "3. EDUCATIONAL BACKGROUND", edu_rows
        )
        story.append(e_header)
        story.append(e_table)
        story.append(PageBreak())

        # 4. ADDITIONAL INFORMATION
        add_rows = [
            [
                Paragraph("English Proficiency:", self.styles["FieldLabel"]),
                Paragraph(
                    "☐ IELTS    ☐ TOEFL    ☐ MUET    ☐ Other: _____________",
                    self.styles["FieldValue"],
                ),
            ],
            [
                Paragraph("Score:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph(
                    "Special Needs / Requirements:", self.styles["FieldLabel"]
                ),
                Paragraph(
                    "______________________________________________<br/>"
                    "______________________________________________",
                    self.styles["FieldValue"],
                ),
            ],
        ]
        add_header, add_table = self._build_section_table(
            "4. ADDITIONAL INFORMATION", add_rows
        )
        story.append(add_header)
        story.append(add_table)
        story.append(Spacer(1, 0.2 * inch))

        # 5. DECLARATION
        story.append(Paragraph("5. DECLARATION", self.styles["SectionHeader"]))
        story.append(Spacer(1, 0.1 * inch))

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

        story.append(Paragraph(declaration_text, self.styles["Normal"]))
        story.append(Spacer(1, 0.25 * inch))

        signature_rows = [
            [
                Paragraph("Applicant Signature:", self.styles["FieldLabel"]),
                Paragraph("", self.styles["FieldValue"]),
            ],
            [
                Paragraph("Date:", self.styles["FieldLabel"]),
                Paragraph("________ / ________ / ________", self.styles["FieldValue"]),
            ],
        ]
        s_header, s_table = self._build_section_table("Signature", signature_rows)
        story.append(s_table)
        story.append(Spacer(1, 0.2 * inch))

        # 6. SUBMISSION INSTRUCTIONS
        story.append(Paragraph("6. SUBMISSION INSTRUCTIONS", self.styles["SectionHeader"]))
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
        2. <b>By Mail:</b> Send to: Admission Office, SKL Universiti, 123, Jalan Bandar Timah, 31900 Kampar Perak.
        <br/>
        3. <b>Email:</b> Scan and email to: SKL123@edu.my
        <br/><br/>
        <b>Contact Information:</b>
        <br/>
        Phone: +60-3-1234-5678
        <br/>
        Email: SKL123@edu.my
        <br/>
        Website: www.skl.edu.my
        """

        story.append(Paragraph(instructions_text, self.styles["Normal"]))

        # Build PDF
        doc.build(story)

        if output_path is None:
            buffer.seek(0)
            return buffer

        return output_path
