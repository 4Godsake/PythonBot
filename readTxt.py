class User:
    def __init__(self, usn, psw, email):
        self.username = usn
        self.password = psw
        self.email = email


f=open('./user.txt')
list = f.readlines()
userList = []
for i in range(len(list)):
    userInfo = list[i].split(',')
    user = User(userInfo[0],userInfo[1],userInfo[2])
    userList.append(user)
print(userList[1].username)

