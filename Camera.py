import salabim as sim
import enum
import random

#摄像头的状态持续时间
CAMERA_ACTIVE_TIME=20
CAMERA_SLEEP_TIME=50
CAMERA_POS_Y_OFFSET=10

#服务器位置
SERVER_POS_Y_OFFSET=30

# 照片的不同状态，暂时废除
# class DeviceState(enum.Enum):
#     Error = enum.auto()  
#     Running = enum.auto()
#     Warning = enum.auto()
# DEVICE_STATE_2_STRING = {
#     DeviceState.Error: "E",
#     DeviceState.Running: "R",
#     DeviceState.Warning: "W",
# }
 
#摄像头的闪烁状态，
class Camera_color(enum.Enum):
    Red = enum.auto()
    Gray = enum.auto()
CAMERA_COLOR_2_STRING = {
    Camera_color.Red: "red",
    Camera_color.Gray :"50%gray"
}
#绘制画面的主要逻辑
def do_animation():

    #照片素材的绘制尺寸信息
    global xvisitor_dim
    global yvisitor_dim

    #调整各类容量上限的参数信息
    global capacity_last, nPipes_last, maxpath_last
    global visitor_num

    #env.modelname("Elevator")
    env.speed(32)
    env.background_color("20%gray")
    # if make_video:
    #     env.video("Elevator.mp4")

    xvisitor_dim = 40
    yvisitor_dim = xvisitor_dim

    #路径的绘制基准位置
    ypath0 = 300

    xled = {}

    #摄像头集合
    cams = []
    
    #通过设置的尺寸和容量得到初始生成点的位置信息
    x = env.width()-serverCapacity*xvisitor_dim
    x -= (pipeCapacity + 5) * xvisitor_dim #减去的值等于信道长度
    xsign = x #显示编号的位置
    x -= xvisitor_dim / 2
    for direction in (up, down):
        x -= xvisitor_dim / 2
        xled[direction] = x
    x -= xvisitor_dim
    xwait = x #指示灯的位置
    #对每个路径都进行位置计算和绘制
    for path in paths:
        y = ypath0 + path.n * yvisitor_dim*1.5
        path.y = y
        b = xvisitor_dim / 4
        cam=Camera(x=xled[up],y=y,b=b)#生成一个摄像头和通路绑定
        path.setCam(cam=cam)
        cams.append(cam)
        sim.AnimateLine(x=0, y=y, spec=(0, 0, xwait, 0))
        sim.AnimateText(x=xsign, y=y, text=str(path.n), fontsize=xvisitor_dim / 2)

        sim.AnimateQueue(queue=path.visitors, x=xwait - xvisitor_dim, y=path.y, direction="w", title="")

    #对每条路径的数据传输管道进行位置计算和绘制
    for Pipe in Pipes:
        x = xsign+xvisitor_dim
        Pipe.setStartx(x=x)
        y = ypath0 + Pipe.n * yvisitor_dim*1.5
        Pipe.pic = sim.AnimateRectangle(
            x=Pipe.x, y=y, spec=(0, 0, pipeCapacity * xvisitor_dim, yvisitor_dim), fillcolor="lightblue", linewidth=0
        )
        sim.AnimateQueue(queue=Pipe.visitors, x=Pipe.x, y=y, direction="e", title="", arg=Pipe,reverse=True)

    #对服务器的位置进行计算和绘制
    for Server in Servers:
        x = env.width()-xvisitor_dim*serverCapacity
        y = ypath0 + Server.n * yvisitor_dim*1.5
        Server.pip = sim.AnimateRectangle(
            x=x, y=y+SERVER_POS_Y_OFFSET, spec=(0, 0, serverCapacity * xvisitor_dim, yvisitor_dim), fillcolor="gray", linewidth=0
        )
        sim.AnimateQueue(queue=Server.visitors, x=x, y=y+SERVER_POS_Y_OFFSET, direction="e", title="", arg=Pipe,reverse=True)
    nPipes_last = nPipes
    env.animate(True)

    #调整上限容量和通路大小，暂时废除
    # sim.AnimateSlider(
    #     x=510,
    #     y=0,
    #     width=90,
    #     height=20,
    #     vmin=1,
    #     vmax=11,
    #     resolution=1,
    #     v=nPipes,
    #     label="#Pipes",
    #     action=set_nPipes,
    #     xy_anchor="nw",
    # )

    # maxpath_last = maxpath
    # sim.AnimateSlider(
    #     x=610,
    #     y=0,
    #     width=90,
    #     height=20,
    #     vmin=2,
    #     vmax=10,
    #     resolution=1,
    #     v=maxpath,
    #     label="max path",
    #     action=set_maxpath,
    #     xy_anchor="nw",
    # )

    # capacity_last = capacity
    # sim.AnimateSlider(
    #     x=710,
    #     y=0,
    #     width=90,
    #     height=20,
    #     vmin=2,
    #     vmax=6,
    #     resolution=1,
    #     v=capacity,
    #     label="capacity",
    #     action=set_capacity,
    #     xy_anchor="nw",
    # )


#同上
# def set_capacity(val):
#     global capacity
#     global capacity_last
#     capacity = int(val)
#     if capacity != capacity_last:
#         capacity_last = capacity
#         env.main().activate()


# def set_nPipes(val):
#     global nPipes
#     global nPipes_last
#     nPipes = int(val)
#     if nPipes != nPipes_last:
#         nPipes_last = nPipes
#         env.main().activate()


# def set_maxpath(val):
#     global maxpath
#     global nPipes
#     global nServers
#     global maxpath_last
#     maxpath = int(val)
#     nPipes =maxpath+1
#     nServers = maxpath
#     if maxpath != maxpath_last:
#         maxpath_last = maxpath
#         env.main().activate()

#数据的状态颜色标注，暂时废除
# def state_color(state):
#     if state == 1:
#         return "red"
#     if state == 2:
#         return "green"
#     if state == 3:
#         return "orange"
#     else :
#         return "gray"

class Camera(sim.Component):
    def setup(self,x,y,b):
        self.x=x
        self.y=y+CAMERA_POS_Y_OFFSET
        self.b=b
        #为摄像头设置指示灯
        self.Cameraslight=[]
        self.light = Camera_color.Red
        #刚开始将摄像机设置为开
        self.lightTrun = True
        sim.AnimateCircle(
            radius=12,
            x=self.x,
            y=self.y,
            fillcolor= "white",
            linecolor= "black",
        )
        Light = sim.AnimateCircle(
            radius=5,
            x=self.x,
            y=self.y,
            fillcolor= lambda arg,t:(
                CAMERA_COLOR_2_STRING[self.light]
                if self.light == Camera_color.Red
                else "50%gray"
            ),
            linecolor= "black",
        )
        self.Cameraslight.append(Light)

    def set_light(self, light):
        self.light=light
        if self.light==Camera_color.Gray:
            self.lightTrun=False
        elif self.light==Camera_color.Red:
            self.lightTrun=True
    
    def get_lightTrun(self):
        return self.lightTrun
    
    def process(self):
        while True:
            if self.light == Camera_color.Gray:
                self.hold(CAMERA_SLEEP_TIME)
                self.set_light(Camera_color.Red)
            elif self.light == Camera_color.Red:
                self.hold(CAMERA_ACTIVE_TIME)
                self.set_light(Camera_color.Gray)

class VisitorGenerator(sim.Component):
    def setup(self, from_, to):
        #设置数据生成的初始位置和流向的服务器接口
        self.from_ = from_
        self.to = to

    def process(self):
        while True:
            #随机生成上述参数
            from_ = sim.IntUniform(self.from_[0], self.from_[1])()
            to = sim.IntUniform(self.to[0], self.to[1])()
            if paths[from_].capacity > paths[from_].vnum:
                Visitor(from_=from_, to=to)
            if load == 0:
                self.passivate()
            else:
                iat = 3600 / load
                r = sim.Uniform(0.5, 1.5)()
                self.hold(r * iat)
#获取数据状态，暂时废除
# def getState(state):
#         if state == 1:
#             return DeviceState.Error
#         elif state == 2:
#             return DeviceState.Running
#         elif state == 3:
#             return DeviceState.Warning
#         else :
#             return state
class Visitor(sim.Component):
    def setup(self, from_, to):
        self.frompath = paths[from_]
        #输入路径的当前数据包数量
        paths[from_].vnum +=  1
        self.topath = paths[to]
        self.to=to
        self.direction = getdirection(self.frompath, self.topath)
        self.setVisitornum()
    def setVisitornum(self):
        global visitor_num #设置一个全局的数据计数标记
        self.num=visitor_num
        visitor_num+=1
    def animation_objects(self, q):#决定了在队列中的动画展现方式
        size_x = xvisitor_dim
        size_y = yvisitor_dim
        b = 0.1 * xvisitor_dim
        an0 = sim.AnimateRectangle(
            spec=(b, 2, xvisitor_dim - b, yvisitor_dim - b),
            linewidth=0,
            fillcolor="Green",
            # text=str(self.topath.n),
            text=str(self.num),
            fontsize=xvisitor_dim * 0.7,
            textcolor="white",
        )
        return size_x, size_y, an0

    def process(self):
        self.enter(self.frompath.visitors)
        if not (self.frompath, self.direction) in requests:
            requests[self.frompath, self.direction] = self.env.now()
        for Pipe in Pipes:
            if Pipe.ispassive():
                Pipe.activate()
        self.passivate()


class VisitorsInPipe(sim.Queue):
    pass
class Server(sim.Component):
    def setup(self,n):
        self.capacity = serverCapacity
        self.visitors = VisitorsinServer()
        self.n=n
        #生成一个随机数，赋给服务器的不同接口
        self.solve_time=sim.IntUniform(5,10)()
    def process(self):
        dooropen=False
        while True:
            if len(self.visitors) >= self.capacity:
                    for visitor in self.visitors:
                        self.hold(self.solve_time)
                        visitor.leave(self.visitors)
            self.passivate()


class Pipe(sim.Component):
    def setup(self,n):
        global xvisitor_dim
        
        self.capacity = pipeCapacity
        self.dest=dest
        self.direction = still
        
        #管道的编号
        self.n=n

        self.path = paths[n]
        self.visitors = VisitorsInPipe()
        self.server=Servers
        
        #生成移动的随机数，体现管道的带宽不同
        self.move_time=sim.IntUniform(10,60)()
        
        #设置管道移动的起点和终点
        self.Startx=0
        self.destx = env.width()-pipeCapacity*xvisitor_dim-serverCapacity*xvisitor_dim
    
    def setStartx(self,x):
        self.Startx=x
    #设置移动的纵坐标，暂时废除
    # def y(self, t):
    #     if self.mode() == "Move":
    #         y = sim.interpolate(t, self.mode_time(), self.scheduled_time(), self.path.y, self.nextpath.y)
    #     else:
    #         y = self.path.y
    #     return y

    #设置移动的横坐标
    def x(self, t):
        if self.mode() == "Move":
            x = sim.interpolate(t, self.mode_time(), self.scheduled_time(), self.Startx, self.destx)
        else:
            x = self.Startx
        return x

    def process(self):
        dooropen = False
        self.path = paths[self.n]
        self.direction = still
        dooropen = False
        while True:
            #灯亮门开，数据离开输入路径，传输到管道中
            if self.path.camera.get_lightTrun() == True:
                self.hold(dooropen_time, mode="Door open")
                dooropen = True
                for visitor in self.path.visitors:
                        if len(self.visitors) < self.capacity:
                            visitor.leave(self.path.visitors)
                            self.path.vnum-=1
                            visitor.enter(self.visitors)
                        self.hold(enter_time, mode="Let in")
            else:
                self.hold(doorclose_time, mode="Door close")
                dooropen = False
            if dooropen:
                self.hold(doorclose_time, mode="Door close")
                dooropen = False
                if len(self.visitors) > 0 :

                    self.hold(self.move_time, mode="Move")
                for visitor in self.visitors:
                    visitor.leave(self.visitors)
                    #进入到对应管道编号上
                    visitor.enter(self.server[visitor.to-1].visitors)
                    self.server[visitor.to-1].activate()
                    self.hold(exit_time, mode="Let exit")
                
            
class VisitorsinServer(sim.Queue):
    pass

class Visitors(sim.Queue):
    pass


class path:
    def __init__(self):
        self.visitors = Visitors()
        self.capacity=pathCapacity
        self.vnum = 0
        self.n = self.visitors.sequence_number()

    def count_in_direction(self, dir):
        n = 0
        for visitor in self.visitors:
            if visitor.direction == dir:
                n += 1
        return n
    def setCam(self,cam):
        self.camera=cam


def getdirection(frompath, topath):
    if frompath.n < topath.n:
        return +1
    if frompath.n > topath.n:
        return -1
    return 0

#方向表述，可以删除
up = 1
still = 0
down = -1

visitor_num=1

dooropen_time = 3
doorclose_time = 3

enter_time = 3
exit_time = 3
solve_time =5
dest=100
load = 50
pathCapacity = 1
serverCapacity = 5
pipeCapacity = 1
maxpath =2
nPipes = maxpath+1
nServers = maxpath
xvisitor_dim = 40
while True:
    env = sim.Environment(trace=False)

    vg_1 = VisitorGenerator(from_=(0, 0), to=(1, maxpath),  name="vg_1")
    vg_2 = VisitorGenerator(from_=(1, maxpath), to=(0, 0), name="vg_2")
    vg_3 = VisitorGenerator(from_=(1, maxpath), to=(1, maxpath),name="vg_3")

    requests = {}
    paths = [path() for ipath in range(maxpath+1)]

    Servers=[Server(n=iServer) for iServer in range(nServers)]
    
    Pipes = [Pipe(n=iPipe) for iPipe in range(nPipes)]


    make_video = False

    do_animation()

    if make_video:
        env.run(1000)
        env.video_close()
        break
    else:
        env.run()

