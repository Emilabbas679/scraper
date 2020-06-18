from sqlalchemy import String, Integer, Boolean, ForeignKey, Float, DateTime, Date, Column
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Jobs(db.Model):
    __tablename__ = 'avirdigital_jobustan_jobs'
    id = db.Column(db.Integer, primary_key=True)
    boss_id = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    unicid = db.Column(db.String, nullable=True)
    slug = db.Column(db.String, nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    subcategory_id = db.Column(db.Integer, nullable=True)
    position_id = db.Column(db.Integer, nullable=True)
    positionlevel_id = db.Column(db.Integer, nullable=True)
    workingtype_id = db.Column(db.Integer, nullable=True)
    lang_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    jobexperience_id = db.Column(db.Integer, nullable=True)
    gender_id = db.Column(db.Integer, nullable=True)
    employeecount = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=0)
    deadline = db.Column(db.Date, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    deleted_at = db.Column(db.Date, nullable=True)
    activated_at = db.Column(db.Date, nullable=True)
    qualifications = db.Column(db.Text, nullable=True)
    aboutjob = db.Column(db.Text, nullable=True)
    jobtype = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, nullable=True)
    agemin_id = db.Column(db.Integer, nullable=True)
    agemax_id = db.Column(db.Integer, nullable=True)
    educationlevel_id = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    salaryfix = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    unicid = db.Column(db.String, nullable=True)
    minsalary = db.Column(db.Integer, nullable=True)
    maxsalary = db.Column(db.Integer, nullable=True)


class Select(db.Model):
    __tablename__ = 'avirdigital_jobustan_selectables'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    type_id = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)


class Categories(db.Model):
    __tablename__ = 'avirdigital_jobustan_categories'
    id = db.Column(db.Integer, primary_key=True)
    sort_order = db.Column(db.Integer)
    name = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    slug = db.Column(db.String, nullable=True)
    is_home = db.Column(db.Boolean, default=1)


class Subcategories(db.Model):
    __tablename__ = 'avirdigital_jobustan_subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    sort_order = db.Column(db.Integer)
    slug = db.Column(db.String, nullable=True)
    category_id = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)


class Positions(db.Model):
    __tablename__ = 'avirdigital_jobustan_positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=1)
    sort_order = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    category_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, default='Created-automatically')
    is_activated = db.Column(db.Boolean, default=1)
    activated_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    last_login = db.Column(db.Date, default=datetime.datetime.utcnow)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    is_company = db.Column(db.Boolean)


class Company(db.Model):
    __tablename__ = 'avirdigital_jobustan_companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.datetime.utcnow)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=True)

