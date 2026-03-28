door_number = 100000000
def solve_door():
    doors = [False] * door_number 

    for i in range(door_number ):
        for j in range(i , door_number  , i+1):
            doors[j] = not doors[j]
    
    return doors

final_door = solve_door()

for idx, open_state in enumerate(final_door):
    status = "open" if open_state else "closed"
    if open_state:(1)
    #     print(f"Doors {idx+1}: {status}")
