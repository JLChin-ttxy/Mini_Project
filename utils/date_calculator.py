"""
Date Calculator for Consistent Year-to-Year Important Dates
This module calculates registration and application deadlines based on semester structure.
"""
from datetime import datetime, timedelta

class DateCalculator:
    """Calculate important dates for admissions based on semester structure"""
    
    # Semester structure
    SEMESTER_1_START_MONTH = 1  # January
    SEMESTER_1_WEEKS = 14  # Long semester
    
    SEMESTER_2_START_MONTH = 5  # May
    SEMESTER_2_WEEKS = 14  # Long semester
    
    SEMESTER_3_START_MONTH = 9  # September
    SEMESTER_3_WEEKS = 7  # Short semester
    
    # Registration periods (before semester starts)
    REGISTRATION_OPEN_MONTHS_BEFORE = {
        1: 3,  # Semester 1: 3 months before (October of previous year)
        2: 3,  # Semester 2: 3 months before (February)
        3: 2   # Semester 3: 2 months before (July)
    }
    
    REGISTRATION_CLOSE_WEEKS_BEFORE = {
        1: 2,  # Semester 1: 2 weeks before start
        2: 2,  # Semester 2: 2 weeks before start
        3: 1   # Semester 3: 1 week before start
    }
    
    # Application deadlines (before registration opens)
    APPLICATION_DEADLINE_WEEKS_BEFORE_REGISTRATION = 4  # 4 weeks before registration opens
    
    # International student deadlines (before local students)
    INTERNATIONAL_DEADLINE_WEEKS_EARLIER = 2  # 2 weeks earlier for visa processing
    
    @staticmethod
    def get_semester_start_date(year, semester):
        """Get the start date of a semester"""
        if semester == 1:
            return datetime(year, DateCalculator.SEMESTER_1_START_MONTH, 1)
        elif semester == 2:
            return datetime(year, DateCalculator.SEMESTER_2_START_MONTH, 1)
        elif semester == 3:
            return datetime(year, DateCalculator.SEMESTER_3_START_MONTH, 1)
        else:
            raise ValueError(f"Invalid semester: {semester}")
    
    @staticmethod
    def get_semester_end_date(year, semester):
        """Get the end date of a semester based on weeks"""
        start_date = DateCalculator.get_semester_start_date(year, semester)
        
        if semester == 1:
            weeks = DateCalculator.SEMESTER_1_WEEKS
        elif semester == 2:
            weeks = DateCalculator.SEMESTER_2_WEEKS
        elif semester == 3:
            weeks = DateCalculator.SEMESTER_3_WEEKS
        else:
            raise ValueError(f"Invalid semester: {semester}")
        
        # Add weeks to start date
        end_date = start_date + timedelta(weeks=weeks)
        return end_date
    
    @staticmethod
    def get_registration_period(year, semester, is_international=False):
        """
        Calculate registration period for a semester
        
        Returns:
            tuple: (registration_open_date, registration_close_date)
        """
        semester_start = DateCalculator.get_semester_start_date(year, semester)
        
        # Registration opens X months before semester starts
        months_before = DateCalculator.REGISTRATION_OPEN_MONTHS_BEFORE[semester]
        # Approximate months using days (30 days per month)
        registration_open = semester_start - timedelta(days=months_before * 30)
        
        # Registration closes X weeks before semester starts
        weeks_before = DateCalculator.REGISTRATION_CLOSE_WEEKS_BEFORE[semester]
        registration_close = semester_start - timedelta(weeks=weeks_before)
        
        # International students have earlier deadlines
        if is_international:
            weeks_earlier = DateCalculator.INTERNATIONAL_DEADLINE_WEEKS_EARLIER
            registration_open = registration_open - timedelta(weeks=weeks_earlier)
            registration_close = registration_close - timedelta(weeks=weeks_earlier)
        
        return (registration_open.date(), registration_close.date())
    
    @staticmethod
    def get_application_deadline(year, semester, is_international=False):
        """
        Calculate application deadline for a semester
        
        Application deadline is X weeks before registration opens
        """
        registration_open, _ = DateCalculator.get_registration_period(year, semester, is_international)
        
        # Application deadline is X weeks before registration opens
        weeks_before = DateCalculator.APPLICATION_DEADLINE_WEEKS_BEFORE_REGISTRATION
        application_deadline = registration_open - timedelta(weeks=weeks_before)
        
        return application_deadline
    
    @staticmethod
    def get_all_important_dates(year):
        """
        Get all important dates for a given year
        
        Returns a list of date dictionaries with event_type, start_date, end_date, etc.
        """
        dates = []
        
        for semester in [1, 2, 3]:
            # Local student dates
            reg_open, reg_close = DateCalculator.get_registration_period(year, semester, False)
            app_deadline = DateCalculator.get_application_deadline(year, semester, False)
            
            dates.append({
                'event_type': f'Semester {semester} Registration (Local Students)',
                'start_date': reg_open,
                'end_date': reg_close,
                'description': f'Registration period for Semester {semester} - Local Malaysian students',
                'is_international': False,
                'semester': semester
            })
            
            dates.append({
                'event_type': f'Semester {semester} Application Deadline (Local Students)',
                'start_date': app_deadline,
                'end_date': app_deadline,
                'description': f'Application deadline for Semester {semester} - Local Malaysian students',
                'is_international': False,
                'semester': semester
            })
            
            # International student dates
            reg_open_int, reg_close_int = DateCalculator.get_registration_period(year, semester, True)
            app_deadline_int = DateCalculator.get_application_deadline(year, semester, True)
            
            dates.append({
                'event_type': f'Semester {semester} Registration (International Students)',
                'start_date': reg_open_int,
                'end_date': reg_close_int,
                'description': f'Registration period for Semester {semester} - International students (earlier deadline for visa processing)',
                'is_international': True,
                'semester': semester
            })
            
            dates.append({
                'event_type': f'Semester {semester} Application Deadline (International Students)',
                'start_date': app_deadline_int,
                'end_date': app_deadline_int,
                'description': f'Application deadline for Semester {semester} - International students (earlier deadline for visa processing)',
                'is_international': True,
                'semester': semester
            })
        
        return dates
    
    @staticmethod
    def get_calculation_explanation():
        """Get a human-readable explanation of how dates are calculated"""
        return """
        IMPORTANT DATES CALCULATION SYSTEM
        
        This system calculates registration and application deadlines consistently year-to-year:
        
        SEMESTER STRUCTURE:
        - Semester 1: January - April (14 weeks, Long Semester)
        - Semester 2: May - August (14 weeks, Long Semester)  
        - Semester 3: September - October (7 weeks, Short Semester)
        
        REGISTRATION PERIODS:
        - Semester 1 Registration: Opens 3 months before (October of previous year), closes 2 weeks before semester start
        - Semester 2 Registration: Opens 3 months before (February), closes 2 weeks before semester start
        - Semester 3 Registration: Opens 2 months before (July), closes 1 week before semester start
        
        APPLICATION DEADLINES:
        - Always 4 weeks before registration opens (to allow time for processing)
        
        INTERNATIONAL STUDENT DEADLINES:
        - All deadlines are 2 weeks earlier than local students (to allow time for visa processing)
        
        CONSISTENCY:
        - These formulas remain the same every year
        - Only the year changes in the calculations
        - Example: Semester 1 2026 follows the same pattern as 2025, just shifted by one year
        """

