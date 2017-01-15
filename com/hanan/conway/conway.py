import collections
import logging

log = logging.getLogger('conway')
file_handler = logging.FileHandler('conway.log', mode='w')
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)


class IConwayView(object):
    def is_alive(self, x, y):
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
        log.debug('Conway __init__')
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
        log.debug('play starts')
#         log.debug('oscil: {}'.format(self.osc))
        next_gen = dict()
        process_set = set()
        for (x,y) in self.current_live_cells.keys():
            log.debug('checking out live cell ({},{})'.format(x,y))
            nbr_set = set([nbr for nbr in Conway.neighbours(x,y, included=True)])
            log.debug('neighbours set:')
            for _nbr in nbr_set:
                log.debug(_nbr)
            process_set = process_set.union(nbr_set)
            log.debug('united set : {}'.format(nbr_set))
#             print('process_set')
#             print(process_set)
        log.debug('process set : {}'.format(process_set))                        
        for (x,y) in process_set:
            log.debug('checking cell in ({},{})'.format(x,y))
#             x,y =_pair.x, _pair.y
            num_live_nbrs = 0
            for (nbrx, nbry) in Conway.neighbours(x,y):
                if self.is_alive(nbrx,nbry):
                    num_live_nbrs += 1
                    log.debug('neighbour ({},{}) is alive'.format(nbrx,nbry))
            processed_cell_alive= self.is_alive(x,y)
            log.debug('determine state for {} cell ({},{}) with {} lively lovely neighbours'.format(
                'Live' if processed_cell_alive else 'Dead', x,y, num_live_nbrs))
            next_gen_alive = Conway.apply_rules(processed_cell_alive, num_live_nbrs)
            log.debug('({},{}) will be {} in the next generation'.format(x,y, 'Live' if next_gen_alive else 'Dead'))
            if next_gen_alive:
                next_gen[(x,y)] = next_gen_alive
        self.current_live_cells = next_gen
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
    def __init__(self, conway_game):
        self.conway_game = conway_game
        self.oscil = 0
    def play(self):
        pass
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
    def __init__(self, conway_game):
        ConwayUi.__init__(self, conway_game)
    def show(self):
        while True:
            self.print_header()
            self.print_board()
            try:
                x = input('Press any key for next round, Ctrl+C to quit')
                self.conway_game.play()
                self.oscil += 1                    
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
        print('Conway\'s Game of Life')
        print('Oscillation {:0>10}'.format(self.oscil))
        print(self.HEADER_CHAR*(self.HIGHER_VER - self.LOWER_VER))
        print('\n')
                    
                
            
            
            
        
if __name__ == "__main__":
    
    glider = 
    '''
     *
      *
    ***
    '''
    
    
    
     
    live_cells = list()
    live_cells.append(Cell(0,0))
    live_cells.append(Cell(1,0))
    live_cells.append(Cell(2,0))
    live_cells.append(Cell(2,-1))
    live_cells.append(Cell(1,-2))
    conway = Conway(glider)
    conwayUi = ConsoleUi(conway)
    conwayUi.show()
        
    
    
        
    
        