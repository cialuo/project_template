from psycopg2 import IntegrityError
from odoo.tools import mute_logger
from odoo.exceptions import AccessError
from faker import Faker
import inspect
from .. import constants as c
faker = Faker()
pwh_model = c.pwh_model
employee_model = c.employee_model #'hr.employee'
job_model = c.job_model #'hr.job'
contract_model = c.contract_model #'hr.contract'
department_model = c.department_model # 'hr.department'
name_field = c.name_field # 'name'
wage_field = c.wage_field #'wage'
job_field = c.job_field #'job_id'
employee_field = c.employee_field # 'employee_id'
job_title_field = c.job_title_field #'job_title'
department_field = c.department_field # 'department_id'
revision_format = c.revision_format
wage = 10000
wage_2 = 20000
wage_3 = 30000
zero = 0
one = 1
two = 2
three = 3
def create_test_employee(self, name = faker.name()):
  dep = self.env[department_model].create({ name_field: faker.name() })
  return self.env[employee_model].create({
    name_field: name,
    job_title_field: faker.job(),
    department_field: dep.id
  })
def create_test_pwh(self, values):
  return self.env[pwh_model].create(values)
def assert_equal(self, a, b):
  return self.assertEqual(a, b)

def assert_not_equal(self, a, b):
  return self.assertNotEqual(a, b)

def assert_raise_integrity_error(self, callable):
  with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
    callable(self)

def assert_raise_access_error(self, callable):
  with self.assertRaises(AccessError):
    callable(self)
    
def get_latest(self, model_name):
  return self.env[model_name].search([], order='id desc', limit=1)

def get_recents(self, model_name, limit = 1):
  return self.env[model_name].search([], order='id desc', limit=limit)

def get_function_name():
  return inspect.currentframe().f_code.co_name

def filter_by_employee(employee):
  return (employee_field, '=', employee.id)

def raise_integrity_error(func):
  def wrapper(self):
    with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
      func(self)
  return wrapper

def raise_access_error(func):
  def wrapper(self):
    with self.assertRaises(AccessError):
      func(self)
  return wrapper

def reset_id_seq(*tables):
  def decorator(func):
    def wrapper(self):
      print('Testing {fname}'.format(fname=func.__name__))
      func(self)
      tmpl = "ALTER SEQUENCE {model}_{column}_seq RESTART WITH {initial}"
      #self.cr.execute(alter_seq_sql)
      #print(tmpl.format(model='hr.contract', column='id', initial=1))
      column = 'id'
      initial = 1
      alter_seq_sql = ';'.join(tuple(map(lambda s: tmpl.format(model=s.replace('.', '_'), column=column, initial=initial), tables)))
      #print(sql)
      self.cr.execute(alter_seq_sql)
      
    return wrapper
  return decorator