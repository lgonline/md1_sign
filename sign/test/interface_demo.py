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
@file: interface_demo.py
@time: 18-7-21 下午5:09 
Description: 
"""

from zope.interface import Interface
from zope.interface.declarations import implementer

# 定义一个接口
class IHost(Interface):
    def goodmorning(self,host):
        """Say good morning to host"""

# 继承接口
@implementer(IHost)
class Host:
    def goodmorning(self,guest):
        """say goodmorning to guest"""
        return 'Good Morning, %s ' % guest

# def main():
#     pass


if __name__ == '__main__':
    # main()
    p = Host()
    hi = p.goodmorning('Tom')
    print(hi)
    pass 
    
    