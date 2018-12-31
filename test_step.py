from Step_Motor import Step_Motor
import time

step = Step_Motor().start()

step.update(0)
time.sleep(1)

step.update(1)
time.sleep(1)

step.update(2)
time.sleep(1)

step.update(3)
time.sleep(1)

step.update(4)
time.sleep(1)

step.stop()
