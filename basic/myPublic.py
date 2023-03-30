# -*- coding:utf-8 -*-
import sys
import os
import requests
import traceback
import time
sys.path.append(os.getcwd())
import configparser
import basic.myGlobal as myGlobal
# import xlrd
# import xlwt

logger = myGlobal.getLogger()


class MySwitch(object):
    """case分支"""
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        #Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        #Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
        # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class MyExcelOp(object):
    #
    def myGetExcelCellvalue(fileName, sheetname, rownum, colname):
        """取Excel单元值"""
        try:
            bk = xlrd.open_workbook(fileName)
            sh = bk.sheet_by_name(sheetname)
            nCols = sh.ncols
            ifExistCol = 0
            for Colnum in range(1, nCols + 1):
                cellvalue = sh.cell_value(0, Colnum - 1)
                if colname == cellvalue:
                    ifExistCol = 1
                    cellvalue = sh.cell_value(rownum, Colnum - 1)
                    # cellvalue = sh.cell(Rownum-1,Colnum-1).value
                    # 1为字符串，2为整数，0为空 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    if str(sh.cell_type(rownum, Colnum - 1)) == "2":
                        cellvalue = str(int(cellvalue))
                    logger.error("取Excel值:" + fileName + " 工作表\"" + sheetname + "\" 第" + str(
                        rownum) + "行 列名\"" + colname + "\" 值\"" + cellvalue + "\"")
                    return cellvalue
            if ifExistCol == 0:
                return False
        except:
            logger.error(traceback.format_exc())
            return False


    def myGetExcelCellvalueRowName(fileName, sheetname, RowTitle, RowName, Colname):
        """取Excel单元值"""
        try:
            bk = xlrd.open_workbook(fileName)
            sh = bk.sheet_by_name(sheetname)
            nRows = sh.nrows
            nCols = sh.ncols
            for Colnum in range(1, nCols + 1):
                cellvalue = sh.cell_value(0, Colnum - 1)
                if RowTitle == cellvalue:
                    for Rownum in range(1, nRows):
                        cellvalue = sh.cell_value(Rownum, Colnum - 1)
                        if RowName == cellvalue:
                            return MyGetExcelCellvalue(fileName, sheetname, Rownum, Colname)
            logger.error("Error:" + fileName + " 工作表\"" + sheetname + "\" 列\"" + RowTitle + "\" 不存在值\"" + RowName + "\"")
            return False
        except:
            logger.error(traceback.format_exc())
            return False


    def mySetExcelCellvalue(fileName, sheetname, Rownum, Colname, Value):
        """修改单元格值"""
        try:
            # 修改
            bk = xlrd.open_workbook(fileName)
            sh = bk.sheet_by_name(sheetname)
            nCols = sh.ncols
            ifExistCol = 0
            for Colnum in range(1, nCols + 1):
                cellvalue = sh.cell_value(0, Colnum - 1)
                if Colname == cellvalue:
                    ifExistCol = 1
                    sh.put_cell(Rownum, Colnum - 1, 1, Value, 0)
                    logger.error("修改Excel值:" + fileName + " " + sheetname + " " + str(
                        Rownum) + " " + Colname + " " + Value)
            if ifExistCol == 0:
                return False
                # 全读并保存
            wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
            style = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = "宋体"
            font.bold = False  # 非粗体
            style.font = font  # 为样式设置字体
            for shtname in bk.sheets():
                wttable = wbk.add_sheet(shtname.name, cell_overwrite_ok=True)
                sh = bk.sheet_by_name(shtname.name)
                nRows = sh.nrows
                nCols = sh.ncols
                for Rownum in range(1, nRows + 1):
                    for Colnum in range(1, nCols + 1):
                        cellvalue = sh.cell_value(Rownum - 1, Colnum - 1)
                        if str(sh.cell_type(Rownum - 1, Colnum - 1)) == "2":
                            cellvalue = str(int(cellvalue))
                        wttable.write(Rownum - 1, Colnum - 1, cellvalue, style)
                        wttable.col(Colnum - 1).width = 0x0d00 + len(cellvalue)  # 256 * (len(cellvalue) + 1)
            wbk.save(fileName)
            return True
        except:
            logger.error(traceback.format_exc())
            return False

    #
    def myGetExcelRowNum(fileName, sheetname):
        try:
            bk = xlrd.open_workbook(fileName)
            sh = bk.sheet_by_name(sheetname)
            nRows = sh.nrows
            if nRows > 1:
                return nRows
            else:
                return False
        except:
            logger.error(traceback.format_exc())
            return False
    
