import sys
#import utils.func as func
import re
import formulate as form
import download as down

# 1 = FORMULATE
# 2 = BULLETIN DOWNLOAD
# 3 = APPLICATION OF BULLETINS

def main(case):
    if case == 1:
        form.formulate()
    elif case == 2:
        down.bulletin()
    elif case == 3:
        print('apply')
    else:
        usage = 'python3 scraper.py (case)\n case:\n 1 = Formulate table\n \
        2 = download bulletins \n 3 = apply bulletins'
        print('usage : '+ usage)


if __name__ == '__main__':
    case = int(sys.argv[1])
    main(case)