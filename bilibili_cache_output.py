# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:41:38 2019
没做异常，有问题就弹出，自己分析
@author: CefcaZJ
"""
# =============================================================================
# os：各类系统、文件操作以及ffmpeg调用
# json：解析json文件
# requests：下载封面
# =============================================================================
import os
import json
import requests

#获取当前目录
root =os.getcwd()
print(root)
dirlist = os.listdir(root)
#print(dirlist)

if input("开始导出缓存，请输入y(es) or n(o)：\n") != 'y':
    exit()
else:
    
    for path in dirlist:
        if os.path.isdir(path):
#进入AVXXXXXXXXXX目录
            os.chdir(path)
            os.mkdir('..\\output') 
            plist = os.listdir(os.getcwd())
            print()
            for dir in plist:
                if os.path.isdir(dir):
#进入PXXX目录            
                    os.chdir(dir)
#读取JSON文件                    
                    with open('entry.json','r',encoding='UTF-8') as f:
                        data = json.load(f)
                        title = str(data['title']).replace('/','').replace('\\','')
                        pname = str(data['page_data']['part'].replace('/','').replace('\\',''))
#进入实际存放视频文件夹的目录                    
                    os.chdir(str(data['type_tag']))  
#调用CMD ffmpeg合并多个blv文件  
#ffmpeg需要配置环境变量或者直接改为具体位置    
###############################################################################  
                    with open('filelist.txt','w+') as lst:
                        for blv in os.listdir(os.getcwd()):
                            if os.path.splitext(blv)[1] == ".blv":
                                lst.write('file \''+blv+'\'\n')
                    lst.close()
                    os.system("ffmpeg -f concat -i filelist.txt -c copy output.flv")
                    os.remove('filelist.txt') 
###############################################################################                    
#合并后的文件更名剪切至输出目录
                    if len(plist) != 1:
                        os.rename('output.flv', root+'/output/P'+str(dir)+'_'+pname+'.flv')
                    else:
                        os.rename('output.flv', root+'/output/'+title+'.flv')
#返回AV目录                    
                    os.chdir('..\\..\\')
#返回根目录             
            os.chdir('..\\')

            
#下载封面，需要就解除屏蔽            
# =============================================================================
#            with open(root+'/output/'+title+'_cover.jpg','wb+') as c:
#                c.write(requests.get(data['cover']).content)
#                c.close()
# =============================================================================
            os.rename(root+'/output', root+'/'+title)
            print(str(data['title'])+'导出完成')
if input("导出完成，输入y退出：\n") != 'y':
    exit()
