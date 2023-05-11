import os

# Calculate Estimate running time based on history logs.
def calculateRunningTime(itemNum):
    if not os.path.exists('running_time_history.txt'):
        open('running_time_history.txt', 'a')
    try:
        f = open('running_time_history.txt', 'r')
    except:
        print("History log file IO error ")
        return
    logs = f.readlines()
    coCount = 0
    coTime = 0
    bfCount = 0
    bfTime = 0
    for log in logs:
        log_str = log.split(',')
        if log_str[0] == '1' and log_str[1] == str(itemNum):
            coCount += 1
            coTime += float(log_str[2])
        if log_str[0] == '2' and log_str[1] == str(itemNum):
            bfCount += 1
            bfTime += float(log_str[2])
    if bfCount == 0 or coCount == 0:
        return

    print(f'Duration time estimation: \nIn this loop of {itemNum} locations to drop by, estimated running time will be \n{(coTime/coCount)}s using Carts Order algorithm, \n{bfTime/bfCount}s using Brute Froce Algorithm.')

def log(choice, itemNum, duration):
    with open('running_time_history.txt', 'a') as file:
        file.write(f'{choice},{itemNum},{duration}\n')