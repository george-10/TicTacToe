import pygame
pygame.init()
width_proportion= 0.5
width = 1100
height =600
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
grid = [['-','-','-'],['-','-','-'],['-','-','-']]     
x=[width_proportion*width-0.2*height,width_proportion*width,width_proportion*width+0.2*height]
y=[0.3*height,0.5*height,0.7*height]
def drawX(screen,x,y):
    Dx= (height/1000)*65  
    Dy= (height/1000)*65
    pygame.draw.line(screen,'black',(x-Dx,y-Dy),(x+Dx,y+Dy),7)
    pygame.draw.line(screen,'black',(x-Dx,y+Dy),(x+Dx,y-Dy),7)
run = True
player = [0,0]
first_player=True #True if X first, False if O first
f = pygame.font.Font(None,36)

stop = True
#def evalFunction(grid):
    
def checkWin(grid):
    for i in range(0,3):
        if grid[i][0] == grid[i][1] == grid[i][2] != '-':
            return grid[i][0]  
        if grid[0][i] == grid[1][i] == grid[2][i] != '-':
            return grid[0][i]
    if grid[0][0] == grid[1][1] == grid[2][2] != '-':
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != '-':
        return grid[0][2] 

    for row in grid:
        if '-' in row:
            return "con" 
    return 'D'
def genX(grid, alpha, beta):
    current = v = -2
    c=checkWin(grid)
    x1=3
    x2=3
    if c== "con":
        for i in range(0,3):
            for j in range(0,3):
                if (grid[i][j]=='-'):
                    grid[i][j]='X'
                    tmp= genO(grid, alpha, beta)
                    tmp=tmp[0]
                    v=max(v,tmp)
                    if(v>current):
                        current=v
                        x1=i
                        x2=j                        
                    grid[i][j]='-'                    
                    if v >=beta :
                        return v,x1,x2
                    alpha= max(alpha,v)          
        return v , x1,x2   
    elif c=='D':
        return 0 ,x1,x2
    elif c=='X':
        return 1 ,x1,x2
    else :
        return -1 ,x1,x2
    
#depth limited search/ evaluation function
#alpha beta prunning
#value function  
def genO(grid, alpha, beta):
    o1=3
    o2=3 
    current=v=2
    c=checkWin(grid)

    if c== "con":
        for i in range(0,3):
            for j in range(0,3):
                if(grid[i][j]=='-'):
                    grid[i][j]='O'
                    tmp = genX(grid, alpha, beta)
                    tmp=tmp[0]
                    v=min(v,tmp)
                    if v<current:
                        current=v
                        o1=i
                        o2=j
                    grid[i][j]='-'                     
                    if v <= alpha:
                        return v ,o1,o2
                    beta = min(beta,v)           
        return v ,o1,o2
    elif c == 'D':
        return 0 ,o1,o2
    elif c== 'X':
        return 1 ,o1,o2
    else:
        return -1 ,o1,o2



while (run):

    screen.fill('#e4e4e4')
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            run = False
        elif event.type == pygame.KEYDOWN and event.key == 114:
            grid = [['-','-','-'],['-','-','-'],['-','-','-']]
            first_player=True
            stop=True  
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and stop:
            pos = event.pos
            if(pos[0]<width_proportion*width-0.1*height):
                player[0]=0
            elif(pos[0]<width_proportion*width+0.1*height):
                player[0]=1
            elif(pos[0]>width_proportion*width+0.1*height):
                player[0]=2
                
                
            if(pos[1]<0.4*height):
                player[1]=0
            elif(pos[1]<0.6*height):
                player[1]=1
            elif(pos[1]>0.6*height):
                player[1]=2
                
                
            if(grid[player[1]][player[0]]=='-'):
                if (first_player):
                    grid[player[1]][player[0]]='X' # X
                    first_player=False
                else:
                    grid[player[1]][player[0]]='O'# 0
                    first_player=True
        elif event.type == pygame.VIDEORESIZE:
            width = event.size[0]
            height = event.size[1]
            if width<1.2*height:
                width=1.2*height
            x=[width_proportion*width-0.2*height,width_proportion*width,width_proportion*width+0.2*height]
            y=[0.3*height,0.5*height,0.7*height]
            screen = pygame.display.set_mode((width,height),pygame.RESIZABLE) 
    
    
    pygame.draw.line(screen,"black",(width_proportion*width-0.30*height,0.4*height),(width_proportion*width+0.30*height,0.40*height),5)#a
    pygame.draw.line(screen,"black",(width_proportion*width-0.30*height,0.6*height),(width_proportion*width+0.30*height,0.6*height),5)#b
    pygame.draw.line(screen,"black",(width_proportion*width-0.1*height,0.2*height),(width_proportion*width-0.1*height,0.8*height),5)#c
    pygame.draw.line(screen,"black",(width_proportion*width+0.1*height,0.2*height),(width_proportion*width+0.1*height,0.8*height),5)#d
    for i in range(0,3):
        for j in range(0,3):
            if (grid[i][j]=='X'):
                drawX(screen,x[j],y[i])
            elif(grid[i][j]=='O'):
                pygame.draw.circle(screen,"black",(x[j],y[i]),(height/1000)*75,5)
    
    result = checkWin(grid)
    
    if result == "con":


        if first_player == False:
            
            p,o1,o2 = genO(grid,-2,2)
            grid[o1][o2]='O'
            first_player = True


    else:
        if(result=='X'):
            text = f.render("X Wins the game!!",True,(0,0,0))
            screen.blit(text,(width/2-width*0.11,height*0.05))
            stop=False
        elif(result=='O'):
            text = f.render("O Wins the game!!",True,(0,0,0))
            screen.blit(text,(width/2-width*0.11,height*0.05))
            stop=False
        elif(result=='D'):
            text = f.render("It's a Draw :(",True,(0,0,0))
            screen.blit(text,(width/2-width*0.11,height*0.05))
            stop=False
          
    
    pygame.display.update()

