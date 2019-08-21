import requests
import imgkit
from PIL import Image
import numpy as np

"""
查询英语四六级成绩，并生成截图
可选择给准考证号打马赛克！
详细教程可关注公众号「裸睡的猪」，回复：查询四六级 查看

@Author:猪哥

"""

def query(exam_number, name):
    """
    查询英语四六级
    :param exam_number: 准考证号
    :param name: 姓名
    :return:
    """
    query_url = 'https://www.chsi.com.cn/cet/query'
    data = {'zkzh': exam_number, 'xm': name}
    headers = {'user-agent': 'Mozilla/5.0', 'Referer': 'https://www.chsi.com.cn/cet/index.jsp'}
    try:
        response = requests.post(query_url, data, headers=headers, timeout=3)
        response.raise_for_status()
    except Exception as e:
        print('查询英语四六级请求失败！原因：')
        raise e
    # 判断是否返回成绩结果
    index = response.text.find('成绩查询结果')
    if index == -1:
        print(f'查询失败，返回网页：\n{response.text}')
        return
    # 保存网页
    with open('cet.html', 'w', encoding=response.encoding) as f:
        f.write(response.text)
    # 生成图片
    html_to_png()


def html_to_png(is_add_mosaic=True):
    """
    生成图片，可添加马赛克挡住准考证号
    :param is_add_mosaic: 是否添加马赛克
    :return:
    """
    # 生成图片，需要安装wkhtmkltopdf软件
    imgkit.from_file('cet.html', 'cet.png')
    # 剪切图片
    img = Image.open('cet.png')
    cropped = img.crop((310, 300, 700, 700))  # (left, upper, right, lower)
    cropped.save("cut_cet.png")
    if is_add_mosaic:
        add_mosaic(5, (146, 158), (170, 300))


def add_mosaic(mosaic_size, y_start_end, x_start_end):
    """
    给图片添加马赛克，主要通过中间值的rgb对局部范围块的rgb做修改
    :param mosaic_size: 马瑟克块元素大小，mosaic_size值越小越精确
    :param y_start_end: 马赛克纵向起点值和终点值(相当于高度差)
    :param x_start_end: 马赛克横向起点值和终点值（相当于宽度差）
    :return:
    """
    cut_img = np.array(Image.open('cut_cet.png'))
    for i in range(y_start_end[0], y_start_end[1], mosaic_size):
        for j in range(x_start_end[0], x_start_end[1], mosaic_size):
            cut_img[i:i + mosaic_size, j:j + mosaic_size] = cut_img[i + (mosaic_size // 2)][j + (mosaic_size // 2)]
    mosaic_img = Image.fromarray(cut_img.astype("uint8"))
    mosaic_img.save('mosaic_cet.png')
    mosaic_img.show()


if __name__ == '__main__':
    exam_number = '你的准考证号'
    name = '你的姓名'
    query(exam_number, name)
