import concurrent.futures
from multiprocessing import Pool    
import time
# import list_of_stocks as lst



def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
#     time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

''' Start all your main processing here [for windows]'''
if __name__ == '__main__':
    start = time.perf_counter()

# Method  2 #
    p = Pool(5)
    secs = [5, 4, 3, 2, 1]
    results = p.map(do_something, [5, 4, 3, 2, 1])
    for result in results:
        print(result)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')

# Method  1 #
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         secs = [5, 4, 3, 2, 1]
#         results = executor.map(do_something, [5, 4, 3, 2, 1])
#     for result in results:
#         print(result)
#     finish = time.perf_counter()
#     print(f'Finished in {round(finish-start, 2)} second(s)')



# img_names = [
#     'photo-1516117172878-fd2c41f4a759.jpg',
#     'photo-1532009324734-20a7a5813719.jpg',
#     'photo-1504198453319-5ce911bafcde.jpg',
#     'photo-1530122037265-a5f1f91d3b99.jpg',
#     'photo-1516972810927-80185027ca84.jpg',
#     'photo-1550439062-609e1531270e.jpg',
#     'photo-1549692520-acc6669e2f0c.jpg'
# ]
# 
# t1 = time.perf_counter()
# 
# def process_image(img_name):
#     print(f'{img_name} was processed...')
# 
# 
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(process_image, img_names)
#     
# t2 = time.perf_counter()
# 
# print(f'Finished in {t2-t1} seconds')