from flask import Flask
from flask import jsonify
from scraping import scrape, vacancies, ejobScrape, ejobVacancies, jobScrape
from flask_sqlalchemy import SQLAlchemy
from models.models import Jobs, Select, Positions, Categories, Subcategories, User, Company, Test
import random
from flask import session
import string
import sys

app = Flask(__name__)
app.secret_key = 'secret s key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/last_jobs'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://club941_jobustan:5,-*[62oi[,T@192.254.185.1:3306/club941_jobustan'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xarezncgdwtmeo:1cbd10d0a9dff21ee58b9b41f562cdbb887a0bbc5365dab6b687098f30307e0d@ec2-54-75-249-16.eu-west-1.compute.amazonaws.com:5432/d3si22qqc83i3o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/', methods=['GET'])
def index(i=0):
    return 'ok'


@app.route('/insert', methods=['GET'])
def insert():
    print('function is started')
    i=0;
    jobs = vacancies()
    months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'İyun', 'İyul', 'Avqust', 'Sentyabr', 'Oktyabr',
              'Noyabr', 'Dekabr']
    new_users = {}
    new_positions = {}
    for job in jobs:
        replacejob = Jobs.query.filter_by(boss_id=job['vac_id']).first()
        if replacejob:
            continue
        else:
            #--------------------Position Category and Subcategory---------------
            position = Positions.query.filter_by(name=job['title']).first()
            if position:
                position_id = position.id
                category_id = position.category_id
                subcategory_id = position.subcategory_id
            else:
                if job['title'] in new_positions.values():
                    values = list(new_positions.values())
                    keys = list(new_positions.keys())
                    ids = keys[values.index(job['title'])]
                    ids = ids.split('-')
                    position_id = int(ids[0])
                    subcategory_id = int(ids[2])
                    category_id = int(ids[1])
                else:
                    cat_other = Categories.query.filter_by(name='Müxtəlif').first()
                    if cat_other:
                        category_id = cat_other.id
                    else:
                        category = Categories(name='Digər', is_active=1, sort_order=Categories.query.count()+1, slug='miscellanious', is_home=1)
                        db.session.add(category)
                        db.session.commit()
                        category = Categories.query.order_by(Categories.id.desc()).first()
                        category_id = category.id
                    sub_other = Subcategories.query.filter_by(name='Digər').first()
                    if sub_other:
                        subcategory_id = sub_other.id
                    else:
                        sub = Subcategories(name='Digər', is_active=1, sort_order=Categories.query.count()+1, slug='miscellanious', category_id=category_id)
                        db.session.add(sub)
                        db.session.commit()
                        sub = Subcategories.query.order_by(Subcategories.id.desc()).first()
                        subcategory_id = sub.id

                    position = Positions(name=job['title'], is_active=1, sort_order=Positions.query.count()+1,
                                         category_id=category_id, subcategory_id=subcategory_id)
                    db.session.add(position)
                    db.session.flush()
                    position_id = position.id
                    db.session.commit()
                    new_positions.update({str(position_id)+'-'+str(category_id)+'-'+str(subcategory_id): job['title']})

            #---------------------Company----------------
            mail = job['email'].split('@')
            search = "%{}%".format(mail[1])
            user = User.query.filter_by(email=job['email'], is_company=1).first()
            if user:
                company = Company.query.filter_by(user_id=user.id).first()
                company_id = company.id
                user_id = user.id
            else:
                if job['email'] in new_users.values():
                    values = list(new_users.values())
                    keys = list(new_users.keys())
                    ids = keys[values.index(job['email'])]  # 'foo'
                    ids = ids.split('-')
                    user_id = int(ids[0])
                    company_id = int(ids[1])
                else:
                    user = User(name=job['email'], email=job['email'], is_company=1)
                    db.session.add(user)
                    db.session.flush()
                    user_id = user.id
                    company = Company(name=job['company'], user_id=user.id)
                    db.session.add(company)
                    db.session.flush()
                    company_id = company.id
                    db.session.commit()
                    new_users.update({str(user_id)+'-'+str(company_id): job['email']})

            # --------------------Deadline---------------
            time = job['expires_on'].split(' ')
            time[1] = time[1].strip(',')
            month = months.index(time[0])+1
            deadline = time[2]+'-'+str(month)+'-'+time[1]
            #---------------------SALARY-----------------
            salary = job['salary']
            salary = salary.strip(' AZN')
            salary_list = salary.split('-')
            if len(salary_list)>1:
                print(salary)
                print(salary_list)
                if salary_list[0] == '':
                    salary = 3
                    minsalary = None
                    salaryfix = None
                    maxsalary = None
                else:
                    salary = 2
                    minsalary = salary_list[0]
                    print('minsalary='+minsalary)
                    maxsalary = salary_list[1]
                    salaryfix = None
            else:
                if salary_list[0] == '-':
                    salary = 3
                    minsalary = None
                    salaryfix = None
                    maxsalary = None
                else:
                    salary = 1
                    salaryfix = salary_list[0]
                    minsalary = None
                    maxsalary = None
            # -------------------Age-----------------
            if 'minimum' in job['age']:
                age = job['age'].split(' ')
                agemin = Select.query.filter_by(title=age[1], type_id=11).first()
                if agemin:
                    agemin_id = agemin.id
                else:
                    addAge = Select(type=11, title=age[0])
                    db.session.add(addAge)
                    db.session.flush()
                    agemin_id = addAge.id
                agemax = Select.query.filter_by(title='Digər', type_id=11).first()
                if agemax:
                    agemax_id = agemax.id
                else:
                    addAge = Select(type_id=11, title='Digər')
                    db.session.add(addAge)
                    db.session.flush()
                    agemax_id = addAge.id
            elif 'maks' in job['age']:
                age = job['age'].split(' ')
                agemax = Select.query.filter_by(title=age[1], type_id=11).first()
                if agemax:
                    agemax_id = agemax.id
                else:
                    addAge = Select(type=11, title=age[0])
                    db.session.add(addAge)
                    db.session.flush()
                    agemax_id = addAge.id
                agemin = Select.query.filter_by(title='Digər', type_id=11).first()
                if agemin:
                    agemin_id = agemin.id
                else:
                    addAge = Select(type_id=11, title='Digər')
                    db.session.add(addAge)
                    db.session.flush()
                    agemin_id = addAge.id
            else:
                age = job['age'].split('-')
                age[1] = age[1].strip(' yaş')
                agemin = Select.query.filter_by(title=age[0], type_id=11).first()
                if agemin:
                    agemin_id = agemin.id
                else:
                    addAge = Select(type=11, title=age[0])
                    db.session.add(addAge)
                    db.session.flush()
                    agemin_id = addAge.id
                agemax = Select.query.filter_by(title=age[1], type_id=11).first()
                if agemax:
                    agemax_id = agemax.id
                else:
                    addAge = Select(type_id=11, title=age[1])
                    db.session.add(addAge)
                    db.session.flush()
                    agemax_id = addAge.id

            # EDUCATION ID
            education = Select.query.filter_by(title=job['education'], type_id=10).first()
            if education:
                edu_level = education.id
            else:
                education = Select.query.filter_by(title='Digər', type_id=10).first()
                if education:
                    edu_level = education.id
                else:
                    education = Select(
                        title='Digər',
                        type_id=10,
                    )
                    db.session.add(education)
                    db.session.flush()
                    edu_level = education.id
                    db.session.commit()
            #----------------------------------EXPERIENCE ID--------------------------
            experience_list = job['experience'].split(' ')
            if 'aşağı' in job['experience']:
                experience = Select.query.filter_by(title='Vacib deyil', type_id=17).first()
                experience_id=experience.id
            elif 'artıq' in job['experience']:
                experience = Select.query.filter_by(title='5-10 il', type_id=17).first()
                experience_id = experience.id
            else:
                experience_format = experience_list[0]+'-'+experience_list[2]+' il'
                experience = Select.query.filter_by(title=experience_format, type_id=17).first()
                experience_id = experience.id
    #-----------------------------------------POSITION LEVEL----------------------------------------------------------------
            position_level = Select.query.filter_by(title='Digər', type_id=13).first()
            if position_level:
                position_level_id = position_level.id
            else:
                position_level = Select(
                    title='Digər',
                    type_id=13
                )
                db.session.add(position_level)
                db.session.flush()
                position_level_id = position_level.id
                db.session.commit()
    #-----------------------------------------WORKING TYPE------------------------------------------------------------------
            working = Select.query.filter_by(title='Digər', type_id=14).first()
            if working:
                workingtype_id = working.id
            else:
                working = Select(title='Digər', type_id=14)
                db.session.add(working)
                db.session.flush()
                workingtype_id = working.id
                db.session.commit()
            # FIND LOCATION
            location = Select.query.filter_by(title=job['region'], type_id=15).first()
            if location:
                location_id = location.id
            else:
                location = Select(title=job['region'], type_id=15)
                db.session.add(location)
                db.session.flush()
                location_id = location.id
                db.session.commit()

    #-----------------------------------------JOB INFORMATION--------------------------------------------------------------
            job['information'] = job['information'] + "\n- Əlaqə üçün: "+job['email']
            job['information'] = job['information'].replace("\n", "<br>")
            job['information'] = job['information'].replace("[email", '')
            job['information'] = job['information'].replace("([email", '')
            job['information'] = job['information'].replace("protected]", job['email'])
            job['information'] = job['information'].replace("protected])", job['email'])

            job['requirements'] = job['requirements'].replace('-', '<br> -')
            job['requirements'] = job['requirements'].replace("([email", '')
            job['requirements'] = job['requirements'].replace("[email", '')
            job['requirements'] = job['requirements'].replace("protected])", job['email'])
            job['requirements'] = job['requirements'].replace("protected]", job['email'])
            job = Jobs(
                title=job['title'],
                aboutjob=job['information'],
                qualifications=job['requirements'],
                educationlevel_id=edu_level,
                boss_id=job['vac_id'],
                jobexperience_id=experience_id,
                category_id=category_id,
                subcategory_id=subcategory_id,
                position_id=position_id,
                lang_id=2,
                location_id=location_id,
                positionlevel_id=position_level_id,
                workingtype_id=workingtype_id,
                jobtype=1,
                status=2,
                is_active=1,
                employeecount=1,
                deadline=deadline,
                agemin_id=agemin_id,
                agemax_id=agemax_id,
                salary=salary,
                salaryfix=salaryfix,
                maxsalary=maxsalary,
                minsalary=minsalary,
                company_id=company_id,
                user_id=user_id,
                unicid=id_generator(31)
            )
            db.session.add(job)
            db.session.commit()
            session.clear()
            db.session.remove()
            i=i+1;
            print(i)
    print('finish')
    return 'okay', 200


@app.route('/jobs')
def jobs():
    return jsonify(Jobs=scrape())


@app.route('/vac')
def vac():
    return jsonify(Jobs=vacancies())
    jobs = vacancies()
    for job in jobs:
        print(job['information'])
        job = Jobs(
            title=job['title'],
            aboutjob=job['information'],
            qualifications=job['requirements'],
        )
        db.session.add(job)
        db.session.commit()
    return 'yes'


@app.route('/ejob')
def ejob():
    return jsonify(Jobs=ejobScrape())


@app.route('/ejob-vac')
def ejobVac():
    return jsonify(Jobs=ejobVacancies())


@app.route('/job')
def jobVac():
    return jsonify(Jobs=jobScrape())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
