import datetime
def calculate_difference(payroll_wage_history): 
  return payroll_wage_history.current_wage - payroll_wage_history.previous_wage

def calculate_percentage(payroll_wage_history):
  return 100.0 * (payroll_wage_history.current_wage - payroll_wage_history.previous_wage) / payroll_wage_history.previous_wage

def calculate_revision(revision_format, contract_ref, changes_count, effective_year):
  return revision_format.format(
    contract_ref=contract_ref,
    changes_count=changes_count,
    effective_year=effective_year
  )
  
def extract_month_from_date(date):
  tmp = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m')
  return int(tmp)

def extract_year_from_date(date):
  tmp = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y')
  return int(tmp)
