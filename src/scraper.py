import sys
import utils.func as func
import re
import formulate as form
import update as up

# 1 = FORMULATE
# 2 = BULLETIN VARIFICATION & UPDATE
def main(case):
    if case == 1:
        form.formulate()
    elif case == 2:
        up.bulletin()
    else:
        usage = 'python3 scraper.py (case)\n case:\n 1 = Formulate table\n 2 = Update'
        print('usage : '+ usage)


if __name__ == '__main__':
    case = int(sys.argv[1])
    main(case)