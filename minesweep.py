import random
size = 5
# Create a list of zeros
board = [0] * size**2

# Select 10 unique random indices to replace with -1
bombs = random.sample(range(len(board)), size+1)

# Replace selected indices with -1
for index in bombs:
    board[index] = -1

for index in range(len(board)):
    if board[index] == -1:
        if index < size: # Check if its top
            print("Top element")
            #Downward
            if board[index+size] != -1:
                board[index+size] += 1
            if index % size - 1 != 0: # Top Right
                #Left
                if board[index-1] != -1:
                    board[index-1] += 1
                #Downward Left
                if board[index-1+size] != -1:
                    board[index-1+size] += 1

            elif index % size == 0: # Top Left
                #Right
                if board[index+1] != -1:
                    board[index+1] += 1
                #Downward right
                if board[index+1+size] != -1:
                    board[index+1+size] += 1
            
        elif (index + size >= 24): # Check if its bottom
            print("Bottom Element")
            #Upward
            if board[index-size] != -1:
                board[index-size] += 1
            if index % size - 1 != 0: # Bottom Right
                #Left
                if board[index-1] != -1:
                    board[index-1] += 1
                #Upward Left
                if board[index-1-size] != -1:
                    board[index-1-size] += 1

            elif index % size == 0: # Bottom Left
                #Right
                if board[index+1] != -1:
                    board[index+1] += 1
                #Upward right
                if board[index+1-size] != -1:
                    board[index+1-size] += 1
        else:
            print("middle")
            #Downward
            if board[index+size] != -1:
                board[index+size] += 1  
            #Left
                if board[index-1] != -1:
                    board[index-1] += 1
            #Right
                if board[index+1] != -1:
                    board[index+1] += 1
            #Upward
            if board[index-size] != -1:
                board[index-size] += 1
            #Upward right
            if board[index+1-size] != -1:
                    board[index+1-size] += 1
            #Upward Left
            if board[index-1-size] != -1:
                    board[index-1-size] += 1
            #Downward right
            if board[index+1+size] != -1:
                    board[index+1+size] += 1
            #Downward Left
            if board[index-1+size] != -1:
                    board[index-1+size] += 1

print(board)
boardString = ""
for i in range(0, len(board)):
    if i % size == 0:
        boardString += "\n"
    boardString += " " + str(board[i])
print(boardString)