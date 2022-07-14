import sys
#import utils.func as func
import re
import formulate as form
import download as down
import delta
import apply

# 1 = FORMULATE
# 2 = BULLETIN DOWNLOAD
# 3 = APPLICATION OF BULLETINS

def main(case):
    if case == 1:
        print('formulate table')
        form.formulate()
    elif case == 2:
        print('download bulletins')
        down.bulletin()
    elif case == 3:
        print('get delta table')
        delta.get_delta()
    elif case == 4:
        print('patch changes')
        apply.patch_apply()
    else:
        usage = 'python3 scraper.py (case)\n case:\n 1 = Formulate table\n \
        2 = download bulletins \n 3 = get delta\n 4 = patch'
        print('usage : '+ usage)


if __name__ == '__main__':
    case = int(sys.argv[1])
    main(case)