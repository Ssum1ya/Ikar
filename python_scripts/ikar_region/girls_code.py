from pioneer_sdk import Pioneer
import time

"""
Код на икаре который пролетел нормально
"""

mini = Pioneer()

def land_takeoff():
    mini.go_to_local_point_body_fixed(0, 0, -0.2, 0)
    time.sleep(2)
    mini.go_to_local_point_body_fixed(0, 0, 0.2, 0)
    time.sleep(2)

def go_to_point(x, y):
    time.sleep(2)
    mini.go_to_local_point_body_fixed(x, y, 0, 0)
    time.sleep(3)

mini.arm()
time.sleep(2)
mini.takeoff()
time.sleep(2)

mini.go_to_local_point_body_fixed(0,0, -0.2, 0) # опустить его на 20 см от takeoff

go_to_point(-0.6, 0)
go_to_point(0, 2.1)
time.sleep(2)
go_to_point(0.45, 0)
 # первый магнит

go_to_point(-0.45, 0)
go_to_point(0, -2.1)
go_to_point(0.6, 0)
 # вернуться на старт

go_to_point(-0.6, 0)
go_to_point(0, 2.1)
time.sleep(2)
go_to_point(-0.45, 0)
 # второй магнит

go_to_point(0.45, 0)
go_to_point(0, -2.1)
go_to_point(0.6, 0) # вернуться на старт

go_to_point(-0.6, 0)
go_to_point(0, 1.6)
go_to_point(-0.6, 0)
# третий магнит
1
go_to_point(0.6, 0)
go_to_point(0, -1.6)
go_to_point(0.6, 0) # вернуться на старт

mini.land()





# go_to_point(0, 2) # вперед на 2
# land_takeoff() # присел, взлетел
# go_to_point(0, -2) # вернулся в начальную
# land_takeoff() # присел, взлетел
#
# go_to_point(0, 1.75) # вперед (ко 2)
# go_to_point(0.65, 0) # вправо на 2
# land_takeoff() # присел, взлетел
# go_to_point(-0.65, 0) # влево на 2
# go_to_point(0, -1.75) # вернулся в начальную
# land_takeoff() # присел, взлетел
#
# go_to_point(0, 1.75) # вперед (ко 3)
# go_to_point(1.75, 0) # вправо на 3
# land_takeoff() # присел, взлетел
# go_to_point(-1.75, 0) # влево на 3
# go_to_point(0, -1.75) # вернулся в начальную
# land_takeoff() # присел, взлетел