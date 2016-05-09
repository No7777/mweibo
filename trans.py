#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
s = open('77777.txt', 'r').read()
ls = s.split(r'}')
f = open('77777d.txt', 'w+')
for l in ls:
    dic = eval(l + '}')
    f.write(u"话题:" + dic['topic'] + '\n')
    f.write(u"类别:" + dic['category'] + '\n')
    f.write(u"描述1:" + dic['desc1'].replace('\n', ' ') + '\n')
    f.write(u"描述2:" + dic['desc2'] + '\n')
    f.write(u"发表时间:" + str(dic['time']) + '\n')
    
