import collections
import logging
import os
from tempfile import gettempdir
import uuid
import json
from os import listdir
from os.path import isfile, join


log = logging.getLogger('conway')
file_handler = logging.FileHandler(os.path.join(gettempdir(), 'conway.log'), mode='w')
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)

class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    
class TranslationReference(Point):
    def TranslationReference(self):
        Point.__init__(self, 0, 0)
    def __add__(self, point):
        self._x += point.x
        self._y += point.y
    def translate(self, point):
        return Point(self.x + point.x, self.y + point.y)
        

class Cell(object):
    def __init__(self, alive=True):
        self._alive = alive
    @property
    def alive(self):
        return self._alive
    
class LiveCells(object):
    def __init__(self, points):
        self.locations_dict = dict()
        for point in points:
            self.locations_dict[point] = Cell(True)
    def live_cell_coordinates(self):
        for point, cell in self.locations_dict.iteritems():
            if cell.alive:
                yield point

class IViewableUniverse(object):
    def get_gen_num(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def get_biomass_coordinates(self):
        pass

class BiomassOverflow(Exception):
    pass
    
class IUniverse(object):
    def __init__(self, universe_id, universe_metadata, live_cells, gen_num=0):
        self.universe_id = universe_id
        self.universe_metadata = universe_metadata
        self._live_cells = live_cells
        self.gen_num = gen_num
    
    def _do_next_generation(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
        
    def next_generation(self):
        self._do_next_generation()
        self.gen_num += 1
    
class Universe(IUniverse, IViewableUniverse):
    def __init__(self, universe_id, universe_metadata, live_cells, gen_num=0):
        IUniverse.__init__(self, universe_id, universe_metadata, live_cells, gen_num)
    @staticmethod
    def get_gen_num(self):
        return self.gen_num
    def get_biomass_coordinates(self):
        return list(self._live_cells.live_cell_coordinates())
    def translate(self, translation_reference):
        translated_cells_point = list()
        for point in self._live_cells.keys():
            translated_cells_point.append(translation_reference.translate(point))
        self._live_cells = LiveCells(translated_cells_point)
    @staticmethod
    def neighbours(point, included=False):
        for j in range(point.y-1,point.y+2):
            for i in range(point.x-1,point.x+2):
                if not included and i == point.x and j == point.y:
                    continue
                yield (i,j)
                    
    def is_alive(self,point):
        alive = False
        try:
            alive = self._live_cells[point].alive
        except KeyError:
            pass
        return alive
    
    def _do_next_generation(self):
        next_gen_points = list()
        process_set = set()
        for point in self._live_cells.live_cell_coordinates():
            for nbr in Conway.neighbours(point, included=True):
                process_set.add(nbr)
        for point in process_set:
            num_live_nbrs = 0
            for nbr_point in Conway.neighbours(point, included=False):
                if self.is_alive(point):
                    num_live_nbrs += 1
            processed_cell_alive= self.is_alive(point)
            next_gen_alive = Conway.apply_rules(processed_cell_alive, num_live_nbrs)
            if next_gen_alive:
                next_gen_points.append(point)
        self._live_cells = LiveCells(next_gen_points)

class Translatable(object):
    def translate(self, translation_reference):
        raise NotImplementedError('THIS IS AN INTERFACE')
            
class Translator(object):
    def __init__(self):
        self.current_translation = TranslationReference()
    def extend_translation(self, point):
        self.current_translation += point
    def translate(self, translatable):
        translatable.translate(self.current_translation)
        
# class UniverseView(object):

class ManangerControls(object):
    def load(self, universe_id):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def create_new_universe(self, live_cells, universe_name=None):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def quit(self):
        raise NotImplementedError('THIS IS AN INTERFACE')

class UniverseMetadata(object):
    def __init__(self, universe_name=''):
        self.universe_name = universe_name

class Manager(object):
    def __init__(self, manager_controls):
        self.manager_view = manager_controls
        self.multiverse = dict()
        self.persistence = self.FilePersistence()
    @staticmethod
    def _make_random_universe_id():
        return uuid.uuid4()
    def on_create_new_universe(self, live_cells, universe_name=None):
        if universe_name is None:
            universe_name = ''
        universe_metadata = UniverseMetadata(universe_name)
        universe_id = self._make_random_universe_id()
        self.multiverse[universe_id] = Universe(universe_id, universe_metadata, live_cells)
    def on_load(self, universe_id):
        self.multiverse[universe_id] = self.persistence.load(universe_id)
        return self.multiverse[universe_id]
    def on_quit(self):
        for universe_id, universe in self.multiverse.iteritems():
            self.persistence.persist(universe_id, universe)
    class IPersistence(object):
        def persist(self, universe_id, universe):
            pass
        def get_persisted_multiverse(self):
            pass
        def load(self, universe_id): 
            pass
    class FilePersistence(IPersistence):
        def __init__(self):
            self.folder = os.path.join( gettempdir(), 'conway_universe_files')
        def persist(self, universe_id, universe):
            universe_data = dict()
            universe_data['gen_num'] = universe.get_gen_num()
            universe_data['live_cells'] = universe.get_biomass_coordinates()
            j = json.dumps(universe_data)
            with open(os.path.join(self.folder, universe_id), mode='w') as wfd:
                wfd.write(j)
        def get_persisted_multiverse(self):
            return [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
        def load(self, universe_id): 
            j =''
            with open(os.path.join(self.folder, universe_id), mode='r') as rfd:
                j = rfd.read()
            universe_data = json.loads(j)
            gen_num = universe_data['gen_num']
            biomass_coordinates = universe_data['live_cells']
            return Universe.load(gen_num, biomass_coordinates)  
            
        
        
        
    

        

class IGameListener(object):
    def on_play(self):    
    
class IGameControls(object):
    def __init__(self):
        self.listeners = list()
    def register(self, listener):
        self.listeners.append(listener)
    def unregister(self, listener):
        self.listeners.remove(listener)
    def play(self, univereId):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def load(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def new_universe(self, live_cells, universe_dimensions=None):
        raise NotImplementedError('THIS IS AN INTERFACE')
    def quit(self):
        raise NotImplementedError('THIS IS AN INTERFACE')

    
class Cell:
    def __init__(self, x, y, alive=True):
        self.x = x
        self.y = y
        self.alive = alive
    
class Conway(IConwayGame, IConwayView):
    def __init__(self, live_cells):
        self.gen_num = 0
        self.current_live_cells = dict()
        for c in live_cells:
            self.current_live_cells[(c.x,c.y)] = c
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
            alive = self.current_live_cells[(x,y)].alive
        except KeyError:
            pass
        return alive
    
    def play(self):
        next_gen = dict()
        process_set = set()
        for (x,y) in self.current_live_cells.keys():
            for nbr in Conway.neighbours(x,y, included=True):
                process_set.add(nbr)
        for (x,y) in process_set:
            num_live_nbrs = 0
            for (nbrx, nbry) in Conway.neighbours(x,y):
                if self.is_alive(nbrx,nbry):
                    num_live_nbrs += 1
            processed_cell_alive= self.is_alive(x,y)
            next_gen_alive = Conway.apply_rules(processed_cell_alive, num_live_nbrs)
            if next_gen_alive:
                next_gen[(x,y)] = Cell(x,y, next_gen_alive)
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
    def __init__(self, conway_manager):
        pass
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
        