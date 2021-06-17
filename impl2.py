from collections import Counter
# q grams
def qgram(word):
    word=word.lower()
    bigram=list()
    for i in range(0,len(word)-1):
        bigr=word[i]+word[i+1]
        bigram.append(bigr)
    return bigram

def dist(listA,listB):
    diff_list1 = list((Counter(listA) - Counter(listB)).elements())
    diff_list2 = list((Counter(listB) - Counter(listA)).elements())
    fin=diff_list1+diff_list2
    return len(fin)

def maxm(x):
    max_val = x[0] 
    for check in x: 
        if check > max_val: 
            max_val = check 
    return max_val

def minm(x):
    min_val = x[0] 
    for check in x: 
        if check < min_val: 
            min_val = check 
    return min_val

def calc_dist(ip1,ip2):
    if len(ip1)>len(ip2):
        word1=ip2
        word2=ip1 #longer
    else:
        word1=ip1
        word2=ip2

    lx=len(word1)
    ly=len(word2)
    sub=list()

    for i in range(ly-lx+1):
        s=word2[i:i+lx]
        sub.append(s)
    #print(sub)

    distances=list()
    for d in sub:
        distances.append(dist(qgram(d),qgram(word1)))

    md=2*(ly-lx+1)*(lx-1)
    t3=sum(distances)/md
    t1=minm(distances)
    t2=(ly-lx)/lx
    return t1+t2+t3

# print(calc_dist("Bhaskaracharya","Aryabhatta"))
def selsort(A):
    for i in range(len(A)):
        min_idx = i
        for j in range(i+1, len(A)):
            if A[min_idx][2] < A[j][2]:
                min_idx = j    
        A[i], A[min_idx] = A[min_idx], A[i]

    return A 

def exec(data,searchq):
    dists=list()
    prob=list()
    for item in data:
        ans=calc_dist(item[0],searchq)
        dists.append(ans)
    max_dist=maxm(dists)
    min_dist=minm(dists)

    for d in range(len(dists)):
        p=1-(dists[d]-min_dist)/(max_dist-min_dist)
        temp=(data[d][0],dists[d],round(p,4))
        prob.append(temp)
    prob=selsort(prob)
    return prob