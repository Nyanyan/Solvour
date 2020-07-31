import ray
import time

# ray.init() のように明示的に指定しなかった場合自動的にリソース数が決定されます
ray.init(num_cpus=4)

# 時間計測をより正確にする都合上Rayの起動を少し待つ
time.sleep(1)

@ray.remote
def func(x):
    time.sleep(3)
    return x

begin_time = time.time()
res1, res2 = func.remote(1), func.remote(2)
print(res1) # 出力例: ObjectID(45b9....) 

print(ray.get(res1), ray.get(res2)) # 出力: 1 2

# ray.getはリストを受けとることもできる
print(ray.get([res1, res2])) # 出力: [1, 2]

end_time = time.time()
print(end_time - begin_time) # 3秒ぐらい