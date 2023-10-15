# BMI 수치 구하기

w = float(input("몸무게 입력(kg): "))
h = float(input("키 입력(m): "))


bmi = w/(h*h)

print("BMI 지수: ",round(bmi,2))
