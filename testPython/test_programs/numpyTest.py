import numpy as np

'''############################################################'''
def print_arr(arr):
    print('----------------\n {}'.format(arr)) 
    for idx, x in np.ndenumerate(arr):
        print(idx, x) 
'''############################################################'''
def t_simple ():
    print("----------------------------------------------------------")
    arr = np.array([1, 2, 3, 4, 5])
    print(arr)
    print(type(arr))
    print("----------------------------------------------------------")
'''############################################################'''
def t_itr_index ():
    arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    for x in np.nditer(arr):
        print(x)
    for idx, x in np.ndenumerate(arr):
        print(idx, x)  
    print("----------------------------------------------------------")  
'''############################################################'''  
def t_concat ():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[5, 6], [7, 8]])
    print_arr(arr1)
    print_arr(arr2)
    print_arr(np.concatenate((arr1, arr2), axis=0)) 
    print_arr(np.concatenate((arr1, arr2), axis=1)) 
    print("----------------------------------------------------------")  

def t_stack ():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[5, 6], [7, 8]])
    print_arr(np.stack((arr1, arr2), axis=0)) # this is default  
    #print_arr(np.stack((arr1, arr2), axis=1)) 
    print_arr(np.hstack((arr1, arr2)))  # hstack doesnt increase dimension
    print_arr(np.dstack((arr1, arr2)))
    print("----------------------------------------------------------")  

def t_std ():
    speed = [32,1110,138,28,59,77,77,28,28,97]
    x = np.var(speed)
    y = np.std(speed)
    print (speed ,"\n================================")
    print('var {:10.2f} \nstd {:5.2f} \nmean {:.2f} \nPercentile - 77 : {:.2f}'
          .format(np.var(speed),
                  np.std(speed),
                  np.mean(speed),
                  np.percentile(speed,77)
                  ))
    #print (x , "std [%.2f] [%.2f]" %(y,x))
    
t_std()












