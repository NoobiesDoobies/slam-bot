# slam-bot

Cara menjalankan program:


## 1. Clone and Build Project
```
cd ~
mkdir -p ros2_ws/src
cd ros2_ws/src
git clone git@github.com:NoobiesDoobies/slam-bot.git
cd .. && colcon build --symlink-install
source install/setup.bash
```

# 2. Clone Differential Drive Controller

[Controller](https://github.com/joshnewans/diffdrive_arduino)

```
cd ~/ros2_ws/src
git clone git@github.com:joshnewans/diffdrive_arduino.git
cd diffdrive_arduino
git checkout humble
cd .. && colcon build --symlink-install
source install/setup.bash
```

