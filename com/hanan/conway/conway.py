import logging
import os
from tempfile import gettempdir
import uuid


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
    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.x, self.y))

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
        for point in self.locations_dict.keys():
            yield point
    def __getitem__(self, key): 
        return self.locations_dict[key]


class Universe(object):
    def __init__(self, universe_id, universe_metadata, live_cells, gen_num=0):
        self.universe_id = universe_id
        self.universe_metadata = universe_metadata
        self._live_cells = live_cells
        self.gen_num = gen_num
    def get_gen_num(self):
        return self.gen_num
    def get_biomass_coordinates(self):
        return list(self._live_cells.live_cell_coordinates())
    def next_generation(self):
        self._do_next_generation()
        self.gen_num += 1
    @staticmethod
    def _neighbours(point, included=False):
        for j in range(point.y-1,point.y+2):
            for i in range(point.x-1,point.x+2):
                if not included and i == point.x and j == point.y:
                    continue
                yield Point(i,j)
                    
    def _is_alive(self,point):
        try:
            return self._live_cells[point].alive
        except KeyError:
            return False
            
    def _do_next_generation(self):
        next_gen_points = list()
        process_set = set()
        for point in self._live_cells.live_cell_coordinates():
            for nbr in Universe._neighbours(point, included=True):
                process_set.add(nbr)
        for point in process_set:
            num_live_nbrs = 0
            for nbr_point in Universe._neighbours(point, included=False):
                if self._is_alive(nbr_point):
                    num_live_nbrs += 1
            processed_cell_alive= self._is_alive(point)
            next_gen_alive = Universe._apply_rules(processed_cell_alive, num_live_nbrs)
            if next_gen_alive:
                next_gen_points.append(point)
        self._live_cells = LiveCells(next_gen_points)
    @staticmethod
    def _apply_rules(alive, num_live_nbrs):
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

class UniverseMetadata(object):
    def __init__(self, universe_name=''):
        self.universe_name = universe_name
    
class UniverseView(object):
    def refresh(self, i_viewable_universe):
        raise NotImplementedError()
    def __init__(self):
        self.listeners = list()
    def register(self, i_universe_controller):
        self.listeners.append(i_universe_controller)
    def unregister(self, i_universe_controller):
        self.listeners.remove(i_universe_controller)
    def on_next_generation(self):
        for l in self.listeners:
            l.next_generation()
            
        
class IUniverseController(object):
    def next_generation(self):
        raise NotImplementedError('THIS IS AN INTERFACE')
    
class UniverseController(object):
    def __init__(self, i_universe, i_universe_views ):
        self.i_universe = i_universe
        self.i_universe_views = i_universe_views
        for _view in self.i_universe_views:
            _view.register(self)
    def start(self):
        for _view in self.i_universe_views:
            _view.refresh(self.i_universe)
    def next_generation(self):
        self.i_universe.next_generation()
        for _view in self.i_universe_views:
            _view.refresh(self.i_universe)
        
                    
        