from timeit import default_timer as timer
from datetime import timedelta

start_time = timer()

for i in range(0, 100000):
    print("Ok")

end_time = timer()

time_for_backup = str(timedelta(seconds=end_time - start_time))
time_for_backup = time_for_backup[:7]

print(f"Выполнено за {time_for_backup}")
