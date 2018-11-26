class StaffMovementSummaryReport:
    def __init__(self, dept_name):
        self.dept_name = dept_name

        self.no_of_senior_staff = " - "
        self.no_of_junior_staff = " - "
        self.total_no_of_staff = " - "
        self.entry = " - "
        self.exit_cases = " - "
        self.promotion_no = " - "
        self.disciplinary_cases = " - "
        self.suspention_cases = " - "
        self.no_of_annual_leave = " - "
        self.maternity_leave = " - "
        self.sick_leave = " - "
        self.casual_L = " - "
        self.total = " - "

class MonthlyTrainingMatterReport:
    def __init__(self, dept_name):
        self.dept_name = dept_name

        self.total_no_of_staff = " - "
        self.number_trained_staff = " - "
        self.nysc = " - "
        self.industry_training = " - "
        self.siwes = " - "
        self.study_leave = " - "
        self.completion_of_study = " - "

