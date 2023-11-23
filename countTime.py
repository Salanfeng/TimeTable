import tkinter as tk
import datetime

class TimeCounter:
    #constant
    time_path = "C:\\Users\\abc\\Desktop\\no use\\TimeTable\\time.txt"
    is_work_state = False
    is_entertainment_state = False

    plan_list = []

    def __init__(self):
        self.rest_time = self.get_data()
        self.system_time = datetime.datetime.now()
        self.window_state = 0
        # 创建一个窗口
        self.window = tk.Tk()
        self.window.iconbitmap("D:\Genshin Impact\launcher.exe")
        self.height = 230
        self.width = 200
        self.window.geometry(f"{self.width}x{self.height}+1500+0")
        self.window.title("卷！")
        self.set_window()

        # 根据初始状态设置按钮状态
        self.plan_element = []
        self.rest_time_last = self.rest_time
        self.window.attributes("-topmost", False)

        self.update_time()
        self.update_plan_label()


    def set_window(self):


        # 创建标签来显示状态
        self.status_label = tk.Label(self.window, text="状态: 暂停")
        self.status_label.grid(row=0,padx=68)

        # 创建一个标签来显示时间
        self.time_label = tk.Label(self.window, text="时间: 00:00:00")
        self.time_label.grid(row=1)

        self.toggle_button = tk.Button(self.window, text="切换大小", command=self.toggle_height)
        self.toggle_button.grid(row=2)

        self.work_button = tk.Button(self.window, text="学习", command=self.set_work_state)
        self.work_button.grid(row=3,ipadx=12)

        self.entertainment_button = tk.Button(self.window, text="娱乐", command=self.set_entertainment_state)
        self.entertainment_button.grid(row=4,ipadx=12,padx=(0,0))

        self.pause_button = tk.Button(self.window, text="暂停", command=self.set_pause_state)
        self.pause_button.grid(row=5,ipadx=12)

        self.toggle_button = tk.Button(self.window, text="切换置顶", command=self.toggle_topmost)
        self.toggle_button.grid(row=6)

        self.plan_label = tk.Label(self.window, text="计划:")
        self.plan_label.grid(row=7,sticky=tk.W)
        self.plan = tk.Entry(self.window, width=16)
        self.plan.grid(row=7)
        self.plan.bind('<Return>', lambda event: self.add_plan())
        self.plan_button = tk.Button(self.window, text="添加", command=self.add_plan)
        self.plan_button.grid(row=7,sticky=tk.E)

    def set_work_state(self):
        self.rest_time_last = self.rest_time
        self.system_time = datetime.datetime.now()
        self.is_work_state = True
        self.is_entertainment_state = False
        self.status_label.config(text="状态: 学习")

    def set_entertainment_state(self):
        self.rest_time_last = self.rest_time
        self.system_time = datetime.datetime.now()
        self.is_work_state = False
        self.is_entertainment_state = True
        self.status_label.config(text="状态: 娱乐")

    def set_pause_state(self):
        self.is_work_state = False
        self.is_entertainment_state = False
        self.status_label.config(text="状态: 暂停")

    def toggle_topmost(self):
        current_state = self.window.attributes("-topmost")
        self.window.attributes("-topmost", not current_state)

    def toggle_height(self):
        if self.window_state == 0:
            self.window.geometry("200x75")  # 设置新的窗口高度
            self.window_state = 1
        else:
            self.window.geometry(f"{self.width}x{self.height}")  # 设置新的窗口高度
            self.window_state = 0

    def add_plan(self):
        new_plan = self.plan.get()
        if new_plan:
            self.plan_list.append(new_plan)
            self.plan.delete(0, tk.END)
            self.update_plan_label()


    def update_plan_label(self):
        # 更新计划标签，先清空再添加
        for widget in self.plan_element:
            widget.destroy()
        self.plan_element = []
        for i in range(len(self.plan_list)):
            t_label = tk.Label(self.window, text=self.plan_list[i])
            t_label.grid(row=i+8, sticky=tk.W)
            self.plan_element.append(t_label)
            t_button = tk.Button(self.window, text="删除", command=lambda index=i: self.delete_plan(index))
            t_button.grid(row=i+8, sticky=tk.E)
            self.plan_element.append(t_button)

        self.height = 230 + 30*(len(self.plan_list))
        self.window.geometry(f"{self.width}x{self.height}+1500+0")

        self.window.update()

    def delete_plan(self, index):
        # 删除所有标签 
        self.plan_list.pop(index)
        self.update_plan_label()

    def get_data(self):
        #时间为datetime
        try:
            with open(self.time_path, "r+",encoding='utf-8') as file:
                data = file.readlines()
                data = [i.strip() for i in data]
                if data:
                    self.plan_list = data[1:]
                    return datetime.datetime.strptime(data[0], "%H:%M:%S") #小时：分钟：秒
                else:
                    return datetime.datetime(1, 1, 1)
        except FileNotFoundError:
            return datetime.datetime(1, 1, 1)

    def update_time(self):
        current_time = datetime.datetime.now()
        if self.is_work_state:
            elapsed_time = current_time - self.system_time
            self.rest_time = self.rest_time_last + elapsed_time
        elif self.is_entertainment_state:
            elapsed_time = current_time - self.system_time
            self.rest_time = self.rest_time_last - 4*elapsed_time
        rest_time_label = self.rest_time.strftime("%H:%M:%S")
        self.time_label.config(text=f"时间: {rest_time_label}")
        self.window.after(1000, self.update_time)

    def on_closing(self):
        try:
            with open("C:/Users/abc/Desktop/no use/TimeTable/time.txt", "w",encoding='utf-8') as file:
                file.write(self.rest_time.strftime("%H:%M:%S"))
                for i in self.plan_list:
                    file.write("\n")
                    file.write(i)
            self.window.destroy()
        except:
            self.window.destroy()

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", TC.on_closing)
        self.window.mainloop()

if __name__ == '__main__':
    # 定时刷新时间标签
    TC = TimeCounter()
    TC.run()
    

    
