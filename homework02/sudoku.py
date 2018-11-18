import random

def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    m=[[j-i for j in range(n)] for i in range(n)]  #Генерациия непустого списка
    c=0
    for i in range(n):
        for j in range(n):
            m[i][j]=values[c]
            c+=1
    return m


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    i=int(pos[0])
    row=list(values[i])
    return row


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    j=pos[1]
    col=[]
    for i in range(len(values)):
        col.append(values[i][j])
    return col


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block=[]
    i=pos[0]
    j=pos[1]
    if i<3:
        for m in range(3):
            if j<3:
                for n in range(3):
                    block.append(values[m][n])
            elif j<6:
                for n in range(3, 6):
                    block.append(values[m][n])
            elif j<9:
                for n in range(6, 9):
                    block.append(values[m][n])
    elif i<6:
        for m in range(3, 6):
            if j<3:
                for n in range(3):
                    block.append(values[m][n])
            elif j<6:
                for n in range(3, 6):
                    block.append(values[m][n])
            elif j<9:
                for n in range(6, 9):
                    block.append(values[m][n])
    elif i<9:
        for m in range(6, 9):
            if j<3:
                for n in range(3):
                    block.append(values[m][n])
            elif j<6:
                for n in range(3, 6):
                    block.append(values[m][n])
            elif j<9:
                for n in range(6, 9):
                    block.append(values[m][n])
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    m=-1
    n=-1
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]=='.':
                m=i
                n=j
                break
        if m>=0 and n>=0:
            break
    return (m, n)



def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values=['1', '2', '3', '4', '5', '6', '7', '8', '9']
    pos_val=[]
    row=get_row(grid, pos)
    col=get_col(grid, pos)
    block=get_block(grid, pos)
    for i in values:
        if i in row:
            continue
        elif i in col:
            continue
        elif i in block:
            continue
        else:
            pos_val.append(i)
    a=set(pos_val)
    return a


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos=find_empty_positions(grid)
    if pos[0]==-1:
        return grid
    i,j=pos
    pos_val=find_possible_values(grid, pos)
    for a in pos_val:
        grid[i][j]=a
        solution=solve(grid)
        if solution:
            return solution
    grid[i][j]='.'
    return None


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    p=set('123456789')
    for i in range(len(solution)):
        row=set(get_row(solution,(i,0)))
        if row!=p:
            return False
    for j in range(len(solution)):
        col=set(get_col(solution,(0,j)))
        if col!=p:
            return False
    for m in range(0, 9, 3):
        for n in range(0, 9, 3):
            block=set(get_block(solution, (m,n)))
            if block!=p:
                return False
    return True


def generate_sudoku(n):
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid=[]
    for i in range(9):
        grid.append(['.'] * 9)
    sgrid=solve(grid)
    n=81-min(81,max(0, n))
    while n:
        i=random.randint(0, 8)
        j=random.randint(0, 8)
        if grid[i][j]!='.':
            grid[i][j]='.'
            n-=1
    return sgrid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
