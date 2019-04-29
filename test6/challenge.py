from openpyxl import load_workbook

def combine():
    wb_path = 'courses.xlsx'
    wb = load_workbook(wb_path)

    students = wb['students']
    times = wb['time']

    cp_sheet = wb.copy_worksheet(students)
    cp_sheet.title = 'combine'

    _map = {i[1]:i[2] for i in times.values}

    for i, v in enumerate(cp_sheet.values):
        value = '学习时间'
        if i:
            value = _map.get(v[1])
        cp_sheet['D{}'.format(i+1)] = value

    wb.save('courses.xlsx')

if __name__ == '__main__':
    combine()
