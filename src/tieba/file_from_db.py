import csv
from collections import OrderedDict

from src.sci.utils import get_db


def file_from_db(page, page_size):
    start = int(page * page_size)
    end = int((page + 1) * page_size)

    if start >= 44187:
        start = 44186
    if end >= 44187:
        end = 44186
    print(start)
    print(end)
    db = get_db()
    cursor = db.cursor()
    with open('result.csv', 'a+', encoding='utf8') as f:
        cursor.execute("SELECT * FROM project ORDER BY id ")
        projects = cursor.fetchall()
        for project in projects[start:end]:
            row = []
            number_key = project[3]
            cursor.execute("SELECT * FROM rela_project WHERE number_key='{}' AND is_master='1';".format(number_key))
            master_projects = cursor.fetchall()
            cursor.execute("SELECT * FROM rela_project WHERE number_key='{}' AND is_master='0';".format(number_key))
            part_projects = cursor.fetchall()
            row.extend(map(str, project[:-3]))

            # 科研成果
            study_result = project[-3]
            study_list = study_result.split(';')
            row.extend(map(str, study_list))
            # 人数统计
            cursor.execute("SELECT POSITION,COUNT(id) FROM part_person WHERE number_key='{}' GROUP BY POSITION;".format(
                number_key))
            part_person = cursor.fetchall()
            position_dict = OrderedDict({"硕士生": 0, "博士生": 0, "博士后": 0, "助教": 0, "讲师": 0, "副教授": 0, "教授": 0})
            people_list = []
            person_count=0
            for _ in part_person:
                if _[0] in position_dict.keys():
                    position_dict[_[0]] += _[1]
                person_count+=_[1]
            # 加上主项目负责人
            if project[8] in position_dict.keys():
                position_dict[project[8]] += 1
            person_count+=1
            for k, v in position_dict.items():
                people_list.append(v)
            # 总人数
            people_list.append(person_count)
            row.extend(map(str, people_list))

            # 项目参与人
            cursor.execute("SELECT * FROM part_person WHERE number_key='{}' ;".format(number_key))
            part_person_list = cursor.fetchall()
            for _ in part_person_list:
                row.extend(_[:3])
            for i in range(20 - len(part_person_list)):
                row.extend(['   ', '   ', '   '])

            for master_p in master_projects:
                row.extend(map(str, master_p[:6]))
            for i in range(20 - len(master_projects)):
                row.extend(['   ', '   ', '   ', '   ', '   ', '   '])
            for part_p in part_projects:
                row.extend(map(str, part_p[:6]))
            for i in range(20 - len(part_projects)):
                row.extend(['   ', '   ', '   ', '   ', '   ', '   '])

            print(row)
            row_str = ",".join(row)
            f.write(row_str + '\n')


if __name__ == '__main__':
    from multiprocessing import Process
    from threading import Thread
    import time

    start = time.time()
    process = list()
    pageCount=8
    for page in range(pageCount):
        t = Process(target=file_from_db, args=(page,int(44187/pageCount)+1))
        process.append(t)
        t.start()
    for t in process:
        t.join()
    end = time.time()
    print("耗时{}".format(end - start))
