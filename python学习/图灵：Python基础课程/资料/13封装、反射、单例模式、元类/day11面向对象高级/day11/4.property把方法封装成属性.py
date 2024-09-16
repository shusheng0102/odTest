'''
property是一种特殊的属性，访问它时会执行一段功能（函数）然后返回值  *****
例：BMI指数（bmi是计算而来的，但很明显它听起来像是一个属性而非方法，如果我们将其做成一个属性，更便于理解）
成人的BMI数值：
过轻：低于18.5
正常：18.5-23.9
过重：24-27
肥胖：28-32
非常肥胖, 高于32
　　体质指数（BMI）=体重（kg）÷身高^2（m）
'''
class People:
    def __init__(self,name,weight,height):
        self.name = name
        self.weight = weight
        self.height = height
    @property
    def bmi(self):
        return self.weight/(self.height**2)
obj = People('大海',70,1.75)
# print(obj.bmi())
# 把方法变成属性调用
print(obj.bmi)



