#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
# 파일 불러오기
file_name = input("Enter a file name : ")
if os.path.exists(file_name) == False:
    print("존재하지 않는 파일입니다.")
else:
    fr = open(file_name, "r")
    A = []
    C = []
    lines = fr.readlines()
    for i in range(len(lines)):
        A.append(lines[i].split())
# Calculation
    for i in A:
# Avg
        avg = (int(i[3]) + int(i[4]))/2
# Grade
        if avg > 90:
            grade = 'A'
        elif avg > 80:
            grade = 'B'
        elif avg > 70:
            grade = 'C'
        elif avg > 60:
            grade = 'D'
        else: 
            grade = 'F'
        i.append(avg)
        i.append(grade)
# Rename
        i[1] = i[1] + ' ' + i[2]
        i.remove(i[2])


# In[9]:


index = ['Student', 'Name', 'Midterm', "Final", 'Average', 'Grade']

def show(A):
    # Index 출력
    for i in range(len(index)):
        print("{0:^13}".format(index[i]), end=' ')
    print()
    # 구분선 출력
    print('--'*40)
    # 등급 기준 오름차순 정렬
    I_sorted = sorted(A, key = lambda x: x[5])
    # 학생들의 성적 출력
    for I in I_sorted:
        for i in range(len(I)):
            print("{0:^13}".format(I[i]), end=' ')
        print()
        
    
def search(ID):
    global A
    ID_list = []
    for I in A:
        ID_list.append(I[0])
    if ID not in ID_list:
        print('NO SUCH PERSON')
    else:
        # Index 출력
        for i in range(len(index)):
            print("{0:^13}".format(index[i]), end=' ')
        print()
        # 구분선 출력
        print('--'*40)
        # 해당 학생 성적 출력
        a = ID_list.index(ID)
        for i in range(len(A[a])):
            print("{0:^13}".format(A[a][i]), end=' ')
        print()

def changescore(ID):
    global A
    ID_list = []
    for I in A:
        ID_list.append(I[0])
    if ID not in ID_list:
        return print('NO SUCH PERSON')
    else:
        a = ID_list.index(ID)
    B = A
    mid_final = input("Mid/Final? ").lower()
    if mid_final == 'mid':
        new_score1 = int(input("# Input new score: "))
        if (new_score1 > 100) or (new_score1 < 0):
            print('Wrong')
        else:
            B[a][2] = new_score1
    elif mid_final == 'final':
        new_score2 = int(input())
        if (new_score2 > 100) or (new_score2 < 0):
            print('Wrong')
        else:
            B[a][3] = new_score2
    else: 
        return print('Wrong')

    # index 출력
    for i in range(len(index)):
        print("{0:^13}".format(index[i]), end=' ')
    print()
    # 구분선 출력
    print('--'*40)
    # 수정 전 출력
    a = ID_list.index(ID)
    for i in range(len(A[a])):
        print("{0:^13}".format(A[a][i]), end=' ')
    print()
    # Score changed
    print('Score changed.')
    # Avg
    avg = (int(A[a][2]) + int(A[a][3]))/2
    # Grade
    if avg > 90:
        grade = 'A'
    elif avg > 80:
        grade = 'B'
    elif avg > 70:
        grade = 'C'
    elif avg > 60:
        grade = 'D'
    else: 
        grade = 'F'
    A[a][4:6] = [avg, grade]
    # 수정 후 출력
    for i in range(len(B[a])):
        print("{0:^13}".format(B[a][i]), end=' ')
    print()
    A = B

def add(ID):
    ID_list = []
    for I in A:
        ID_list.append(str(I[0]))
    if ID not in ID_list:
        Name = input("Name: ")
        print('Name : ', end = ' ')
        Mid_score = int(input("Midterm Score: "))
        print('{0}'.format(Mid_score, end = '\n'))
        Final_score = int(input("Final Score: "))
        print('{0}'.format(Final_score, end = '\n'))
        print('Student added')
        # average
        avg = (Mid_score + Final_score)/2
        # grade
        if avg > 90:
            grade = 'A'
        elif avg > 80:
            grade = 'B'
        elif avg > 70:
            grade = 'C'
        elif avg > 60:
            grade = 'D'
        else: 
            grade = 'F'
        new_student = [ID, Name, Mid_score, Final_score, avg, grade]
        A.append(new_student)
    else:
        print('ALREADY EXISTS')

def searchgrade(grade):
    defalut = ['A', 'B', 'C', 'D', 'F']
    grade_list = []
    count_list = []
    for I in A:
        grade_list.append(str(I[-1]))
        if grade == I[-1]:
            count_list.append(I)
    count = grade_list.count(str(grade))
    if grade in defalut:
        if count == 0:
            print('NO RESULTS')
        else:
            # index 출력
            for i in range(len(index)):
                print("{0:^13}".format(index[i]), end=' ')
            print()
            # 구분선 출력
            print('--'*40)
            # 해당 성적의 학생 출력
            for I in count_list:
                for i in range(len(I)):
                    print("{0:^13}".format(I[i]), end=' ')
                print()
    else:
        return print('')
    
    
def remove(ID):
    if len(A) == 0:
        print('List is empty')
    else:
        ID_list = []
        for I in A:
            ID_list.append(str(I[0]))
        if ID not in ID_list:
            print('NO SUCH PERSON')
        else:
            del A[ID_list.index(ID)]
            print('Student removed.')
                
    

def quit():
    defalut = ['yes', 'no']
    save = input('Save data?[yes/no] ')
    if save in defalut:
        if save == 'yes':
            print('File name: ', end = ' ')
            name = input()
            Final_list = []
            A_sorted = sorted(A, key = lambda x: x[4])
    #         for I in A:
    #             Final_list.append(str(I[3]))
            fs = open(name, "w")
            for I in A_sorted:
                I_cut = I[0:3]
                d1 = "{0}".format(I[0])
                d2 = "{0}".format(I[1])
                d3 = "{0}".format(I[2])
                d4 = "{0}".format(I[3])
                data = "{0}\t{1}\t{2}\t{3}\n".format(d1, d2, d3, d4)
                fs.write(data)
            fs.close()
        else:
            pass
    else:
        return print('Wrong input!')


# In[10]:


while True:
    command = input("# ")
    if command == "show":
        show(A)
    elif command == "search":
        ID_input = input("Student ID: ")
        search(ID_input)
    elif command == 'changescore':
        ID_input = input("Student ID: ")
        changescore(ID_input)
    elif command == 'add':
        ID_input = input("Student ID: ")
        add(ID_input)
    elif command == 'searchgrade':
        Grade_input = input("Grade to search: ")
        searchgrade(Grade_input)
    elif command == 'remove':
        ID_input = input("Student ID: ")
        remove(ID_input)
    elif command == "quit":
        quit()
        break
    else:
        print("wrong input!")

