<div align = "center">

## 测试百度识图在测试集上的表现
</div>

**目的：** 得到百度识图在测试集上的准确率　　  
**分析：** 百度识图只支持本地上传以及输入url方式,（这里采用后者）且未提供API接口，因此只能爬取网页获取预测结果．　　  
**流程：**　   
![](http://upload-images.jianshu.io/upload_images/8798237-d92e55d170436e28.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  

百度识图预览:　　

![ ](http://upload-images.jianshu.io/upload_images/8798237-6197900c68d063a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

识别页面预览:　　
![](http://upload-images.jianshu.io/upload_images/8798237-d47b9d48513f825a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 步骤一:为每张图片生成url链接　　
测试集预览：　　

![](http://upload-images.jianshu.io/upload_images/8798237-f365f0c4557c841c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这里我的测试集是以绝对路径的方式存放在txt中,要为每张图片生成一个外链,因此需要一个平台来存储图片,这里我选择**七牛**,并且用脚本批量上传.(ps用到了七牛提供的qshell工具)　　
![](http://upload-images.jianshu.io/upload_images/8798237-79855806a78a580e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)　　

上传之后：　　

![](http://upload-images.jianshu.io/upload_images/8798237-3faef2504ec27737.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)　　

然后批量下载外链到本地txt　　


## 步骤二:爬取网页获取预测信息　　   
识图结果(top5)　　    

![](http://upload-images.jianshu.io/upload_images/8798237-d874c117b7885a8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)　
　  
## 步骤三：计算top1-error／top5-error　　 

得到:  
top1-error rate = 0.6419  
top5-error rate = 0.4151  

查看日志文件分析:  
![ ](http://upload-images.jianshu.io/upload_images/8798237-4a350cdace56b04c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  

将识别失败的样本拿出:   
![ ](http://upload-images.jianshu.io/upload_images/8798237-f7dc7e10c6344ab5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到百度识图对于有些轻微遮挡(水印较多)以及花卉在图中占比较小时,无法准确识别.
