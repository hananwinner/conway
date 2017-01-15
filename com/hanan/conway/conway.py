import collections
import logging
import os
from tempfile import gettempdir


log = logging.getLogger('conway')
file_handler = logging.FileHandler(os.path.join(gettempdir(), 'conway.log'), mode='w')
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)


class IConwayView(object):
    def is_alive(self, x, y):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def get_gen_num(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
    
class IConwayGame(object):
    def play(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
    
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Conway(IConwayGame, IConwayView):
    def __init__(self, live_cells):
        self.gen_num = 0
        self.current_live_cells = dict()
        for c in live_cells:
            self.current_live_cells[(c.x,c.y)] = True
        log.debug(self.current_live_cells)
            
    @staticmethod
    def neighbours(x,y, included=False):
        for j in range(y-1,y+2):
            for i in range(x-1,x+2):
                if not included and i == x and j == y:
                    continue
                yield (i,j)
                    
    def is_alive(self,x,y):
        alive = False
        try:
            alive = self.current_live_cells[(x,y)]
        except KeyError:
            pass
        return alive
    
    def play(self):
        next_gen = dict()
        process_set = set()
        for (x,y) in self.current_live_cells.keys():
            nbr_set = set([nbr for nbr in Conway.neighbours(x,y, included=True)])
            process_set = process_set.union(nbr_set)
        for (x,y) in process_set:
            num_live_nbrs = 0
            for (nbrx, nbry) in Conway.neighbours(x,y):
                if self.is_alive(nbrx,nbry):
                    num_live_nbrs += 1
            processed_cell_alive= self.is_alive(x,y)
            next_gen_alive = Conway.apply_rules(processed_cell_alive, num_live_nbrs)
            if next_gen_alive:
                next_gen[(x,y)] = next_gen_alive
        self.current_live_cells = next_gen
        self.gen_num += 1

    def get_gen_num(self):
        return self.gen_num
    
    @staticmethod
    def apply_rules(alive, num_live_nbrs):
        if alive:
            if num_live_nbrs < 2:
                return False
            elif num_live_nbrs > 3:
                return False
            else:
                return True             
        else:
            if num_live_nbrs == 3:
                return True
            else:
                return False
            
        
class ConwayUi(object):
    def __init__(self):
        pass
    def set_game(self, conway_game):
        self.conway_game = conway_game
    def show(self):
        pass
    
class ConsoleUi(ConwayUi):
    DIAMETER = 10
    LOWER_HOR = -DIAMETER
    HIGHER_HOR = DIAMETER
    LOWER_VER = -DIAMETER
    HIGHER_VER = DIAMETER
    LIVE_CELL = '*'
    DEAD_CELL = ' '
    HEADER_CHAR = 'C'
       
    def __init__(self):
        ConwayUi.__init__(self)
        
    def show(self):
        while True:
            self.print_header()
            self.print_board()
            try:
                x = input('Press any key for next round, Ctrl+C to quit')
                self.conway_game.play()
            except KeyboardInterrupt:
                raise 
            
    def print_board(self):        
        for j in range(self.LOWER_VER, self.HIGHER_VER):
            cl = ''
            for i in range(self.LOWER_HOR, self.HIGHER_HOR):
                cl += self.LIVE_CELL if self.conway_game.is_alive(i,j) else self.DEAD_CELL
            print(cl)
            
    def print_header(self):
        print('\n')
        print(self.HEADER_CHAR*(self.HIGHER_VER - self.LOWER_VER))
        print('\n')
        print('Conway\'s Game of Life')
        print('\n')
        print('Generation {:0>10}'.format(self.conway_game.get_gen_num()))
        print('\n')
        print(self.HEADER_CHAR*(self.HIGHER_VER - self.LOWER_VER))
        print('\n')
        
class ConwayController(object):
    def __init__(self, conway_game, conway_ui):
        self.conway_ui = conway_ui
        self.conway_ui.set_game(conway_game)
    def start(self):
        self.conway_ui.show()
                    
if __name__ == "__main__":
    
#     glider = 
#     '''
#      *
#       *
#     ***
#     '''
    
    
    
     
    live_cells = list()
    live_cells.append(Cell(0,0))
    live_cells.append(Cell(1,0))
    live_cells.append(Cell(2,0))
    live_cells.append(Cell(2,-1))
    live_cells.append(Cell(1,-2))
    conway_ui = ConsoleUi()
    conway_game = Conway(live_cells)
    ctrlr = ConwayController(conway_game, conway_ui)
    ctrlr.start()
    
        
    
    
        
    
        