#!/usr/bin/env python
# coding: utf-8

# # 데이터 선택

# ## 넘파이 실습

# In[17]:


# 라이브러리 로딩
import numpy as np # import로 라이브러리 불러오고 as로 별칭 지정


# In[2]:


# 파이썬 리스트에서 넘파이로 변환
a = [1, 3.14, True, 'hello'] #리스트
b = np.array(a)


# In[3]:


# 리스트 원소 데이터 타입 확인
print(a)
for element in a:
    print('Data type of {} : {}'.format(element, type(element)))


# In[5]:


# 넘파이 배열 원소확인
print(b)
for element in b:
    print('Data type of {} : {}'.format(element, type(element)))


# In[6]:


# 중첩 리스트 생성
a = [[1, 2, 3], [4, 5, 6]]
print(a)


# In[7]:


# 중첩 리스트 데이터 타입 확인
type(a)


# In[8]:


# 중첩리스트를 넘파이 배열로 변환 => 2차원 행렬로 변환
b = np.array(a)
print(b)


# In[9]:


# 행렬 데이터 타입 확인
type(b)


# In[11]:


# 배열의 shape 확인
b.shape


# In[12]:


# 배열의 차원 확인
b.ndim


# In[13]:


# 배열내 총 원소 개수 확인
b.size


# In[14]:


# 2x3 행렬을 3x2 행렬로 변환
print(b.reshape(3, 2))


# In[15]:


# 배열 요소 데이터타입 변경: 정수 -> 실수
b = np.array(a, dtype=np.float64) #dtype 인수 설정
print(b)


# In[16]:


# 배열 요소 데이터 타입 변경: 실수 -> 정수
b = b.astype(np.int64) # 사후 변경 시 astype 메서드로 변경
print(b)


# ## 넘파이 배열 인덱싱

# In[18]:


# 새로운 배열 arr 생성
arr = np.array([1, 2, 3, 4, 5])


# In[19]:


print(arr)


# In[20]:


# 배열 첫번째 원소 가져오기
print(arr[0])


# In[23]:


# 배열 네번째 원소 가져오기
print(arr[3])


# In[22]:


# 배열 마지막 원소 가져오기
print(arr[-1])


# ### 2차원 배열 인덱싱

# In[27]:


# 2차원 배열 생성 : 괄호로 묶어줘야 함
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])


# In[28]:


# 1행 1열 원소 가져오기 -> arr[행, 열]로 명시하여 원한는 위치와 데이터에 접근 가능
arr_2d[0, 0]


# In[29]:


# 2행 3열 원소 가져오기
arr_2d[1, 2]


# ### 배열 슬라이싱

# In[30]:


# arrange 메서드를 이용해 넘파일 배열 생성
arr_2 = np.arange(1, 7).reshape(2, 3)   # arange(시작 숫자, 끝 숫자) : 시작 숫자부터 끝숫자-1 까지의 번호가 나열되어 저장된다.
                                        # reshape(행, 열) : 원소 개수에 맞춰 reshape을 활용하면 배열의 크기를 바꿀 수 있다.
print(arr_2d)


# In[32]:


# 첫번째 행 전체 가져오기
print(arr_2d[0, :])


# In[33]:


# 세번째 열 전체 출력
print(arr_2d[:,2])


# In[37]:


# 전체 행 두번째 열까지 모두 출력
print(arr_2d[:,:2])


# ## 판다스 <span style="background-color:#F1F8FF">pandas</span> 소개

# ### <span style="background-color:#F1F8FF">pandas</span> 라이브러리 로딩

# In[38]:


import pandas as pd


# In[39]:


# 실습에 사용할 샘플 딕셔너리 생성

data = {
    '이름': ['아이유', '김연아', '홍길동', '장범준', '강감찬'],
    '학과': ['국문학', '수학', '컴퓨터', '철학', '경영학'],
    '성적': [3.0, 1.0, 3.5, 2.7, 4.0]
}


# In[40]:


data


# In[42]:


# 딕셔너리 타입인 data를 pd.DataFrame() 인자에 대입하면 됩니다.
df=pd.DataFrame(data)
display(df)


# ## 데이터 <span style="background-color:#F1F8FF">csv</span>로 저장하기

# In[43]:


# 데이터프레임을 csv로 저장 --> to_csv 메소드 이용
df.to_csv('C:/Users/qctum/PycharmProjects/pythonProject/student.csv', sep=',', index=False)
# to_csv(저장 경로와 파일 이름 저장, sep=콤마로 구분, index=False 저장시 인덱스 제외)


# ## 데이터 불러오기

# In[44]:


# 데이터 로딩은 pandas의 read_csv를 활용하면 됨
df = pd.read_csv('C:/Users/qctum/PycharmProjects/pythonProject/student.csv') # 경로 설정만 해주면 끝!
display(df)


# ## <span style="background-color:#F1F8FF">pandas</span> 원하는 데이터 선택하기

# ### 1) 슬라이싱(slicing)

# In[45]:


# 데이터 슬라이싱
df[1:5] # 데이터의 1번 행부터 4번 행까지 선택


# In[46]:


df[0:3] # 첫번째부터 세번째까지 접근


# In[47]:


df[0:] # 모든 행 접근


# ### 2) 인덱싱(indexing)

# In[48]:


# df[1]   Key error가 발생. 데이터 프레임에서는 할 수 없는 인덱싱


# In[49]:


# 단순 인덱싱 (fancy도 boolean도 아님)
# 컴럼명을 주어 단순 인덱싱
df['이름']


# In[50]:


# 마찬가지로 다른 컴럼명을 주어 단순 인덱싱
# 여기서는 Series형식으로 출력됨
df['학과']


# #### Fancy Indexing

# In[51]:


# 인덱싱 시 리스트로 값을 주면 됨
# '이름'과 '학과' 열에만 접근 시
df[['이름', '학과']]


# In[52]:


fancy_list = ['이름', '학과'] # 원하는 컬럼만 리스트로 선택

# fancy 인덱싱
df[ fancy_list ]


# In[53]:


# 컬럼 입력 시 순서는 중요하지 않음
df[['학과', '이름']] # 컴럼의 순서가 바뀌어도 작동


# #### 슬라이싱 + 인덱싱

# In[54]:


df[1:3][['학과', '이름']]


# In[65]:


df[['학과', '이름']][1:3]


# #### Boolean indexing
# (연산자를 이용하여 인덱싱 수행 e.g. <span style="background-color:#F1F8FF">==</span>, <span style="background-color:#F1F8FF">!=</span>, <span style="background-color:#F1F8FF">></span>, etc)

# In[66]:


# 수학과 소속인 학생의 데이터만 추출
df[df['학과'] == '수학']


# 이렇듯 <span style="background-color:#F1F8FF">df[ 불리언 리스트 ]</span>로 작동함(참/거짓 판단)

# In[67]:


# 성적이 0.5로 나누어지는 행에 접근
df[df['성적'] % 0.5 == 0]


# In[68]:


df['성적'] % 0.5 == 0


# ## pandas 고급 인덱싱 <span style="background-color:#F1F8FF">loc</span> & <span style="background-color:#F1F8FF">iloc</span> 인덱서

# In[71]:


# 한 개의 행에 대해서만 loc indexing
df.loc[3]


# In[72]:


# 데이터 타입
type(df.loc[3])


# In[73]:


# 행에 대해서 fancy indexing
df.loc[ [1, 3, 4] ]  # loc 인덱서에 리스트로 값을 부여


# In[74]:


# 행에 대해서 fancy indexing과 컬럼 슬라이싱
df.loc[ [1, 3, 4], :]


# In[75]:


# 행에 대해서 fancy indexing과 원하는 컬럼 슬라이싱
df.loc[ [1, 3, 4], '이름':'성적']


# In[77]:


# 행에 대해서 fancy indexing과 원하는 컬럼 슬라이싱
df.loc[ [1, 3, 4], ['이름','성적']]


# In[78]:


# iloc 인덱서 사용 시
df.iloc[[1, 3, 4], 0:2] # loc는 컴럼명 명시, iloc는 컴럼의 순서를 명시


# In[81]:


# loc + boolean indexing
df.loc[ df['성적'] % 2 != 0, ['이름', '학과', '성적']]

