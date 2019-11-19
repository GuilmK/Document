# -*- coding: utf-8 -*-
"""
这个类负责处理有关Item的数据存储
负责辅助WorkSpace类
"""


class LabelItem:
    # 这个类会被创建很多个
    X_percent = 0.0
    Y_percent = 0.0
    text = ""

    def __init__(self, x, y, txt):
        self.X_percent = x
        self.Y_percent = y
        self.text = txt
    pass
