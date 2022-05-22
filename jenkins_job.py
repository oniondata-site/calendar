''' 定时的更新任务，由维护者运行，普通用户请忽视。
'''
import os
import time
from updater import updater


def run():
    print('== update cn json ==')
    updater.update()
    print('== push github ==')
    exit_code = os.system('git commit -am "Sync by robot"')
    exit_code = os.system('git push origin')
    assert(exit_code == 0)
    print('== push gitee ==')
    os.system('git push cn_mirror')
    assert(exit_code == 0)

    print('== job success ==')
    time.sleep(5)


if __name__ == '__main__':
    run()
