from serial import Serial
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as anim
import time

TIME_STEP = 1.0
T_OS = 28
T_HIST = 26
MAX_VALS = 60
PROPLOT_STYLESHEET = r'C:\Users\lnick\Documents\Personal\Programming\Python\Resources\proplot_style.mplstyle'

plt.style.use(PROPLOT_STYLESHEET)


def read_last_temp(frame: int):

    data = str(s.readline())

    while 'Measurement' not in data:
        time.sleep(TIME_STEP / 1000)
        data = str(s.readline())
    else:
        temp = float(data.split('Temperature = ')[-1].split(r'\r')[0])
        print(f'T = {temp} \t\t t = {dt.datetime.now()} \t\t frame = {frame}')
        return temp


def animate(frame: int, xs: list[float], ys: list[float]):

    last_temp = round(read_last_temp(frame), 3)

    times.append(dt.datetime.now().strftime('%H:%M:%S'))
    temps.append(last_temp)

    xs = xs[-1 * MAX_VALS :]
    ys = ys[-1 * MAX_VALS :]

    plt.cla()

    plt.title('Temperature Sensor')
    plt.xlabel('Time / hr min sec ')
    plt.ylabel('Temperature / $ ^{\circ} C $ ')
    plt.xticks(rotation=30)
    plt.gca().xaxis.set_major_locator(MaxNLocator(15))

    plt.plot(xs, [T_OS] * len(xs),
        label=r'$ T_{OS} = $' + f'{T_OS}' + r'$ ^{\circ} C $', color='red', linestyle='dashed')
    plt.plot(xs, [T_HIST] * len(xs),
        label=r'$ T_{hist} = $' + f'{T_HIST}' + r'$ ^{\circ} C $', color='green', linestyle='dashed')

    plt.plot(xs, ys, label=f'Last temp = {last_temp}' + r' $ ^{\circ} C $')
    plt.legend(loc='upper left')


times = []
temps = []
fig = plt.figure()

with Serial('COM9', 9600, timeout=1) as s:
    ani = anim.FuncAnimation(fig, animate, fargs=(times, temps), interval=TIME_STEP * 1000)
    plt.show()
