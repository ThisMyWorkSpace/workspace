import re  # 导入re模块
from datetime import date, datetime, timedelta  # 从datetime模块中导入date,datetime,timedelta模块
import calendar  # 导入calendar模块


def calculate(num1, num2, operator):
    """
    :param num1: 一个float型数字
    :param num2: 一个float型数字
    :param operator: * / + -
    :return: 一个float型数字
    """
    global result
    result = 0
    if operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2
    elif operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    return result


def is_operator(exp):
    """
    判断是不是运算符，如果是返回1
    :param exp: str
    :return: 0或1
    """
    operators = ["*", "/", "+", "-"]
    if exp in operators:
        return 1
    else:
        return 0


def equation_format(formula):
    """将算式处理成列表，解决横杆是负数还是减号的问题"""
    formula = re.sub(" ", "", formula)  # 去掉算式中的空格
    formula_list = [i for i in re.split("/-/d+/.?/d*", formula) if i]
    # 列表生成式、正则表达式(以“横杠数字”分割)
    final_formula_list = []  # 最终的算式列表
    for item in formula_list:
        # 如果第一个数是个负数，则横杠就不是减号
        if len(final_formula_list) == 0 and re.search("^/-/d+/.?/d*$", item):
            final_formula_list.append(item)
            continue
        # 如果final_formal_list最后一个元素是运算符，则横杠数字不是负数
        elif len(final_formula_list) > 0:
            if re.search("[+\\-*/(]$", final_formula_list[-1]):
                final_formula_list.append(item)
                continue
        # 按照运算符分割开
        item_split_list = [j for j in re.split("([+\\-*/()])", item) if j]
        final_formula_list += item_split_list
    return final_formula_list


def decision(last_ope, now_ope):
    """
    :param last_ope: 运算符栈的最后一个运算符
    :param now_ope: 从算式列表取出的当前运算符
    :return: 1 代表弹栈运算，0 代表弹运算符栈最后一个元素， -1 表示入栈
    """
    # 定义4种运算符级别
    rate1 = ["+", "-"]
    rate2 = ["*", "/"]
    rate3 = ["("]
    rate4 = [")"]
    if last_ope in rate1:
        if now_ope in rate2 or now_ope in rate3:
            # 如果连续两个运算优先级不一样，则需要入栈
            return -1
        else:
            return 1
    elif last_ope in rate2:
        if now_ope in rate3:
            return -1
        else:
            return 1
    elif last_ope in rate3:
        if last_ope in rate4:
            return 0
        else:
            return -1
    else:
        return -1


def final_calculate(formula_list):
    num_stack = []  # 数字栈
    ope_stack = []  # 运算符栈
    for exp in formula_list:
        operator = is_operator(exp)
        if not operator:
            # 压入数字栈
            # 字符串转换为浮点数
            num_stack.append(float(exp))
        # 如果是运算符
        else:
            while True:
                # 如果运算符栈 = 0，则无条件入栈
                if len(ope_stack) == 0:
                    ope_stack.append(exp)
                    break
                # 函数decision()做决策
                label = decision(ope_stack[-1], exp)
                if label == -1:
                    # 如果 = -1,则压入运算符栈进入下一次循环
                    ope_stack.append(exp)
                    break
                elif label == 0:
                    # 如果 = 0,则弹出运算符栈内最后一个，进入下一次循环
                    ope_stack.pop()
                    break
                elif label == 1:
                    # 如果 = 1,则弹出运算符栈内最后两个元素，弹出数字栈最后两位元素
                    ope = ope_stack.pop()
                    num1 = num_stack.pop()
                    num2 = num_stack.pop()
                    # 执行计算
                    # 计算之后压入数字栈
                    num_stack.append(calculate(num1, num2, ope))
    # 处理大循环结束后（数字栈和运算符栈中可能还有元素）的情况
    while len(ope_stack) != 0:
        ope = ope_stack.pop()
        num1 = num_stack.pop()
        num2 = num_stack.pop()
        num_stack.append(calculate(num1, num2, ope))
    return num_stack, ope_stack


"-----------------------------------------------------------------------"


def judge():
    judge_date = input("请输入您需要判断的日期:(格式如2019-10-7)")
    judge_date_t = datetime.strptime(judge_date, "%Y-%m-%d").date()
    judge_year = int(judge_date[0:4])
    basic_date = date(judge_year, 1, 1)
    res = (judge_date_t - basic_date + timedelta(days=1)).days
    print("您所输入的日期是当年的第{}天".format(res))


"-----------------------------------------------------------------------"


def cale():
    Year = int(input("请输入您需要打印的日历表的年份:"))  # 将用户输入的年份赋值给整型变量Year
    Month = int(input("请输入您需要打印的日历表的月份:"))  # 将用户输入的月份赋值给整型变量Month
    print(calendar.month(Year, Month))


if __name__ == '__main__':
    # First_Calculator
    # 方法一：直接用函数eval()实现计算功能
    print("运算结果为:{}".format(eval(input("请输入您需要计算的式子:"))))
    print("----------------------------------------------")
    # 方法二:只能进行加减乘除的基本运算
    expression = input("请输入您需要计算的式子:")
    expression_list = equation_format(expression)
    result, _ = final_calculate(expression_list)
    print("运算结果为:{}".format(result[0]))
    print("----------------------------------------------")
    # Second_TimeJudge
    judge()
    print("----------------------------------------------")
    # Third_Calendar_Query
    cale()
