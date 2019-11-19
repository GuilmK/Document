# -*- coding: utf-8 -*-
"""
这个类负责处理所有的文件处理操作
包括新建、打开并载入、存储、另存为
主要调用LabItem类
"""
import LabItem
import ImageProcess
import os
import wx
import codecs


class FileHandler:

    everything = {}

    curTransFilePath = ""  # 用于实现载入不同名称的文件而实现的变量

    def __init__(self,OutEverything):
        self.everything = OutEverything
        pass

    # 菜单中的创建文件按钮,需要一个imageProcess的实例来修改左边文件显示
    def CreateTranslation(self, imageProcess):
        # wx.MessageBox(("当前工作路径" + str(os.getcwd())), "创建翻译", wx.ICON_INFORMATION)
        dlg = wx.DirDialog(None, u"选择文件夹创建翻译文本", style=wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            os.chdir(dlg.GetPath())
            # wx.MessageBox(("当前工作路径" + str(os.getcwd())), "创建翻译", wx.ICON_INFORMATION)
            ImageProcess.MyImage.ChangeDir(imageProcess)
            # curFile和curTransFilePath相互独立，绝对不能干扰
            self.curTransFilePath = os.getcwd() + "\\Translation.txt"
            file = open(self.curTransFilePath, 'w', encoding='utf-8')
            file.write("")
            wx.MessageBox(("翻译文件位置：" + str(self.curTransFilePath)), "创建翻译", wx.OK | wx.ICON_INFORMATION)

            #真正写信息的部分
            for filename, labitem in self.everything.items():
                file.write("\n>>>>>>>>[" + filename + "]<<<<<<<<\n")
            file.close()
        dlg.Destroy()
        pass

    # open是最有挑战性的
    def OpenTranslation(self,imageProcess):
        wildcard = u"文本文件 (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(None, message=u"选择文件",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.curTransFilePath = dlg.GetPath()
            ImageProcess.MyImage.ChangeDir(imageProcess)

            with codecs.open(self.curTransFilePath, 'r', 'utf-8') as file:
                isList = False
                curPicName = ""
                tempList = []
                tempx = 0.0
                tempy = 0.0
                tempText = ""
                for line in file.readlines():
                    if line[0:9] == ">>>>>>>>[" and line[-11:-2] == "]<<<<<<<<":
                        # 这代表是刚开始的循环
                        if curPicName == "":
                            tempText = ""
                            curPicName = line[9:-11]
                            tempList = self.everything[curPicName]
                            isList = True
                        else:
                            tempLabel = LabItem.LabelItem(tempx, tempy, tempText)
                            tempList.append(tempLabel)
                            curPicName = line[9:-11]
                            tempText = ""
                            isList = True
                    elif line[0:17] == "----------------[":
                        if isList:
                            tempList = self.everything[curPicName]
                            isList = False
                            pass
                        else:
                            tempLabel = LabItem.LabelItem(tempx, tempy, tempText)
                            tempList.append(tempLabel)
                        tempText = ""
                        tempx = float(line[-16:-11])
                        tempy = float(line[-10:-5])
                    elif line == "\r\n":
                        pass
                    else:
                        tempText += line
                tempLabel = LabItem.LabelItem(tempx, tempy, tempText)
                tempList.append(tempLabel)
            ImageProcess.MyImage.LabelAll(imageProcess)
            wx.MessageBox(("文件位置：" + self.curTransFilePath), "创建翻译",
                          wx.OK | wx.ICON_INFORMATION)
        dlg.Destroy()
        pass




    def SaveTranslation(self):
        if self.curTransFilePath == "":
            wx.MessageBox("你没有打开任何文件！ε=(´ο｀*)))" , "警告", wx.OK | wx.ICON_INFORMATION).Show()
        file =open(self.curTransFilePath, 'w', encoding='utf-8')

        # 真正写信息的部分
        for filename, labitem in self.everything.items():
            file.write("\n>>>>>>>>[" + filename + "]<<<<<<<<")
            i = 1
            for item in labitem:
                tmpx = "%.3f" % item.X_percent
                tmpy = "%.3f" % item.Y_percent
                file.write("\n----------------[" + str(i) + "]----------------[" +
                           tmpx + "," + tmpy + ",1]\n")
                file.write(item.text + "\n")
                i += 1
        file.close()
        wx.MessageBox("保存成功", "保存翻译", wx.OK | wx.ICON_INFORMATION)
        pass

    def SaveAsTranslation(self):
        wildcard = u"文本文件 (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(None, message=u"保存翻译文件",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.FD_SAVE)
        dlg.SetFilterIndex(0)  # 设置默认保存文件格式，这里的0是txt，1是所有文件类型
        if dlg.ShowModal() == wx.ID_OK:
            # 确保另存为后原来的文件不再被修改，直接修改文件路径
            self.curTransFilePath = dlg.GetPath()
            if not os.path.splitext(self.curTransFilePath)[1]:  # 6 确保文件名后缀
                self.curTransFilePath += ".txt"
            file = open(self.curTransFilePath, "w", encoding='utf-8')

            for filename, labitem in self.everything.items():
                file.write("\n>>>>>>>>[" + filename + "]<<<<<<<<\n")
                i = 1
                for item in labitem:
                    tmpx = "%.3f" % item.X_percent
                    tmpy = "%.3f" % item.Y_percent
                    file.write("----------------[" + str(i) + "]----------------[" +
                               tmpx + "," + tmpy + ",1]\n")
                    file.write(item.text + "\n")
                    i += 1
            file.close()

            wx.MessageBox("另存成功", "另存翻译", wx.OK | wx.ICON_INFORMATION)
        dlg.Destroy()
        pass
