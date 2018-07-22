#!/usr/bin/env python  
# -*- coding: utf-8 -*-

""" 
@version: v1.0 
@author: 330mlcc 
@Software: PyCharm
@license: Apache Licence  
@Email   : mlcc330@hotmail.com
@contact: 3323202070@qq.com
@site:  
@software: PyCharm 
@file: demo.py
@time: 18-7-21 下午5:06 
Description: 
"""


class Host(object):
    def goodmoning(self,name):
        return 'good morning, %s' % name

def main():
    pass


if __name__ == '__main__':
    # main()
    h = Host()
    hi = h.goodmoning('liugang9')
    print(hi)
    pass 
    
    