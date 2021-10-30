import random
dept = ["csb", "eeb", "meb", "mcb", "ceb", "chb", "mmb"]
cou = ["cs" ,"me", "ge", "ce", "ch", "hs"]
letter = "abcdefghijklmnopqrstuvwxyz"
def generateStudentId(dept, batch):
    roll = random.randint(1000, 9999)
    return batch+dept  + str(roll)


def generateRandomName():
    length = random.randint(3, 10)
    s = ""
    for i in range(length):
        s+= letter[random.randint(0, 25)]
    return s
def student(n): 
    for i in range(n):
        dep = random.choice(dept)
        batch = str(random.randint(2008, 2020))
        id = generateStudentId(dep, batch)
        name = generateRandomName()
        print("INSERT INTO students(id, name, dept, batch) VALUES ("+ id + "," + name + "," + dep + "," + batch + ");")



def instructor(n):
    for i in range(n):
        id = i+1
        name = generateRandomName()
        dep = random.choice(dept)
        print("INSERT INTO instructor(id, name, dep) VALUES ("+ id + "," + name + "," + dep + ");")

course = []
def courses(n):
    for i in range(n):
        course_id = ''
        while(1):
            course_id = random.choice(cou) + str(random.randint(1, 5))+ '0'+str(random.randint(1, 5))
            if(course_id not in course):
                break
        course.append(course_id)
        title = generateRandomName()
        T = str(random.randint(1, 4))
        P = str(random.randint(1, 4))
        S = str(random.randint(1, 4))
        C = str(random.randint(1, 4))
        L = str(random.randint(1, 4))
        print("INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ("+ course_id + "," + title + "," + L + ',' + T+ "," + P + ',' + S + ',' + C + ");")

courses(20)
preReqs = []

for i in range(len(course)):
    for j in range(i+1, len(course)):
        a = []
        try:
            if(random.randint(1, 1000)%15 == 0):
                a = random.sample(range(i+1, len(course)), 2)
            elif(random.randint(1, 1000)%15 == 0):
                a = random.sample(range(i+1, len(course)), 1)
            
        except ValueError:
            a = []
        for j in a:
            preReqs.append((i, j))



preReqs = list(set(preReqs))

def prereq():
    for i in preReqs:
        print("INSERT INTO prereq(course_id, prereq_id) VALUES ("+ str(course[i[0]]) + ',' + str(course[i[1]]) + ");")

prereq()

students(50)
instructor(10)