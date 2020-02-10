import turtle as t
import math
import random
import cv2
import numpy as np
import time

t.hideturtle()

POPULATION = 1000                   # 人口数量为1000
WIDTH = 500                         # 领土长度为500
HEIGHT = 400                        # 领土宽度为400

INFECTIVE_RADIUS = 8                # 传染范围为8
INIT_INFECTED_COUNT = 10            # 初始感染人数为10
MIN_LATENCY = 2                     # 最小潜伏期为2天
MAX_LATENCY = 14                    # 最长潜伏期为14天
DEATH_DAY = 7                       # 病情最严重为第7天
CURE_DAY = 10                       # 病情痊愈为第10天
DEATH_RATE_IN_HOSPITAL = 0.02       # 住院死亡概率为2%
DEATH_RATE_OUTSIDE = 0.20           # 非住院死亡概率为20%
IMMUNIZED_PERIOD = 30               # 痊愈后抗体持续时间为30天

TRANSMISSION_RATE = 0.1             # 传播概率为10%

HOSPITAL_CAPACITY = 50              # 医院床位数量为50

MAX_TRAVEL_DISTANCE = 5             # 国民每日最大活动为5

IS_SICK_ISOLATED = True             # 病人在家隔离

human = []
potential_count = POPULATION - INIT_INFECTED_COUNT
incubation_count = INIT_INFECTED_COUNT
sick_count = 0
in_hospital_count = 0
cure_count = 0
death_count = 0
day = -1

def travel(i):
    dist = random.random() * MAX_TRAVEL_DISTANCE
    alpha = random.random() * math.pi * 2
    xoffset = math.sin(alpha)*dist
    yoffset = math.cos(alpha)*dist
    human[i][3] += xoffset
    human[i][3] = max(0,min(WIDTH,human[i][3]))
    human[i][4] += yoffset
    human[i][4] = max(0,min(HEIGHT,human[i][4]))

def infect(i):
    count = 0
    for j in range(0,POPULATION):
        if human[j][0] == 0 and not i == j:
            if math.fabs(human[i][3]-human[j][3])+math.fabs(human[i][4]-human[j][4]) < INFECTIVE_RADIUS:
                will_transmit = random.random()
                if will_transmit < TRANSMISSION_RATE:
                    count += 1
                    human[j][0] = 1
                    human[j][1] = day
                    human[j][5] = (int)(random.random()*(MAX_LATENCY-MIN_LATENCY)+MIN_LATENCY)+day
    return count

TWIDTH = 600
THEIGHT = 400
TDAYS = 1000
PPORTION = 1.05
pos = []
for i in range(0,5):
    pos.append((-TWIDTH/2,-THEIGHT/2))
pos[0] = (-TWIDTH/2,-THEIGHT/2+potential_count/POPULATION*THEIGHT)
pos[1] = (-TWIDTH/2,-THEIGHT/2+incubation_count/POPULATION*THEIGHT)
t.pensize(4)
t.setup(TWIDTH+200, THEIGHT+200, -1, 50)
t.delay(0)
t.pu()
t.goto(-TWIDTH/2,-THEIGHT/2)
t.pd()
t.seth(90)
t.fd(THEIGHT)
t.color("grey")
t.write("人数（总人数："+str(POPULATION)+"）", font=("微软雅黑", 14, "normal"))
t.color("black")
t.goto(-TWIDTH/2,-THEIGHT/2)
t.seth(0)
t.fd(TWIDTH)
t.color("grey")
t.write("天数" , font=("微软雅黑", 14, "normal"))
t.color("black")
t.pu()
t.goto(-TWIDTH/2,-THEIGHT/2)
for i in range(1,21):
    t.pu()
    t.goto(-TWIDTH/2-10,-THEIGHT/2+THEIGHT/20*i-THEIGHT/60)
    t.pd()
    t.write(int(i*POPULATION/20) , align='right', font=("Arial", 8, "bold"))
    t.pu()
t.goto(-TWIDTH/2,-THEIGHT/2)
for i in range(1,21):
    t.pu()
    t.goto(-TWIDTH/2+TWIDTH/20*i-TWIDTH/60,-THEIGHT/2-THEIGHT/20)
    t.pd()
    t.write(int(i*TDAYS/20), align='center', font=("Arial", 8, "bold"))
    t.pu()

map = ("未感染人数","潜伏期人数","已发病人数","有抗体人数","已死亡人数")
color = ("blue","orange","red","green","black")
for i in range(0,5):
    t.color(color[i])
    t.pu()
    t.goto(TWIDTH/2,THEIGHT/2+80-20*i)
    t.pd()
    t.write(map[i], font=("微软雅黑", 10, "normal"))

t.pensize(2)
time.sleep(2)
for i in range(0, INIT_INFECTED_COUNT):
    human.append([1, 0, False, random.random() * WIDTH, random.random() * HEIGHT,
                  (int)(random.random()*(MAX_LATENCY-MIN_LATENCY)+MIN_LATENCY),-1])
for i in range(INIT_INFECTED_COUNT, POPULATION):
    human.append([0, -1, False, random.random() * WIDTH, random.random() * HEIGHT,
                  -1,-1])

while True:
    if day >= TDAYS:
        break
    day += 1
    for i in range(0,POPULATION):
        if human[i][0] == -1:
            continue;
        elif human[i][0] == 3:
            if human[i][6] <= day:
                potential_count += 1
                cure_count -= 1
                human[i][0] = 0
                human[i][6] = -1
            travel(i)
        elif human[i][0] == 2:
            if human[i][5] + CURE_DAY == day:
                if human[i][2]:
                    in_hospital_count -= 1
                    human[i][2] = False
                sick_count -= 1
                cure_count += 1
                human[i][0] = 3
                human[i][6] = day+IMMUNIZED_PERIOD
                continue
            if human[i][5] + DEATH_DAY == day:
                destiny = random.random()
                if human[i][2] and destiny < DEATH_RATE_IN_HOSPITAL:
                    in_hospital_count -= 1
                    sick_count -= 1
                    death_count += 1
                    human[i][0] = -1
                    human[i][2] = False
                elif not human[i][2] and destiny < DEATH_RATE_OUTSIDE:
                    sick_count -= 1
                    death_count += 1
                    human[i][0] = -1
            elif not human[i][2] and in_hospital_count < HOSPITAL_CAPACITY:
                in_hospital_count += 1
                human[i][2] = True
            elif not IS_SICK_ISOLATED and not human[i][2]:
                travel(i)
                count = infect(i)
                potential_count -= count
                incubation_count += count
        elif human[i][0] == 1:
            travel(i)
            if not human[i][1] == day:
                count = infect(i)
                potential_count -= count
                incubation_count += count
            if human[i][5] == day:
                incubation_count -= 1
                sick_count += 1
                human[i][0] = 2
        elif human[i][0] == 0:
            travel(i)
    img = np.ones((int(HEIGHT*PPORTION), int(WIDTH*PPORTION), 3), np.uint8)
    img *= 255
    point_size = 1
    point_color = [] # BGR
    thickness = 2
    points_list = []
    for i in human:
        points_list.append((int(i[3]*PPORTION),int(i[4]*PPORTION)))
        if(i[0]==0):
            point_color.append((255,0,0))
        elif(i[0]==1):
            point_color.append((0, 165, 255 ))
        elif(i[0]==2):
            point_color.append((0, 0, 255 ))
        elif(i[0]==3):
            point_color.append((0, 255, 0 ))
        elif(i[0]==-1):
            point_color.append((0, 0, 0 ))

    for point,color in zip(points_list,point_color):
        cv2.circle(img, point, point_size, color, thickness)
    cv2.imshow('image', img)
    map = (potential_count,incubation_count,sick_count,cure_count,death_count)
    color = ("blue","orange","red","green","black")
    for i in range(0,5):
        t.color(color[i])
        t.pu()
        t.goto(pos[i][0],pos[i][1])
        t.pd()
        t.goto(pos[i][0]+TWIDTH/TDAYS,-THEIGHT/2+map[i]/POPULATION*THEIGHT)
        if day%(TDAYS/20) == 0:
            t.write(map[i], font=("宋体", 10, "normal"))
        pos[i] = (pos[i][0]+TWIDTH/TDAYS,-THEIGHT/2+map[i]/POPULATION*THEIGHT)

    print("未感染人数： "+str(potential_count))
    print("潜伏期人数： " + str(incubation_count))
    print("发病人数： " + str(sick_count))
    print("死亡人数： " + str(death_count))
    print("治愈人数： " + str(cure_count))
    print("医院内人数/医院可容纳人数： " + str(in_hospital_count) + "/" + str(HOSPITAL_CAPACITY))
t.done()
