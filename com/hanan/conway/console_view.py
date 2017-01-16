import sys
sys.path.append('.')
from conway import *
class ConsoleUi(UniverseView):
    DIAMETER = 10
    LOWER_HOR = -DIAMETER
    HIGHER_HOR = DIAMETER
    LOWER_VER = -DIAMETER
    HIGHER_VER = DIAMETER
    LIVE_CELL = '*'
    DEAD_CELL = ' '
    HEADER_CHAR = 'C'
    
    def refresh(self, i_viewable_universe):
        self.print_header(i_viewable_universe)
        self.print_board(i_viewable_universe)
        try:
            x = input('Press any key for next generation, Ctrl+C to quit')
#                 self.conway_game.play()
            self.on_next_generation()
        except KeyboardInterrupt:
            raise    
       
    def print_board(self, i_viewable_universe):
        matrix = [[self.DEAD_CELL for _ in range(self.LOWER_HOR, self.HIGHER_HOR)] 
                  for _ in range(self.LOWER_VER, self.HIGHER_VER)]
        for point in i_viewable_universe.get_biomass_coordinates():
            matrix[point.x-self.LOWER_HOR][point.y-self.LOWER_VER] = self.LIVE_CELL
        for j in range(self.HIGHER_VER -self.LOWER_VER):
            horizontal_line_at_j = ''
            for i in range(self.HIGHER_HOR - self.LOWER_HOR):
                horizontal_line_at_j += matrix[i][j]
            print(horizontal_line_at_j)
             
    def print_header(self, i_viewable_universe):
        print('\n')
        print(self.HEADER_CHAR*(self.HIGHER_VER - self.LOWER_VER))
        print('\n')
        print('Conway\'s Game of Life')
        print('\n')
        print('Generation {:0>10}'.format(i_viewable_universe.get_gen_num()))
        print('\n')
        print(self.HEADER_CHAR*(self.HIGHER_VER - self.LOWER_VER))
        print('\n')


if __name__ == "__main__":
    
#     glider = 
#     '''
#      *
#       *
#     ***
#     '''
    import uuid
    live_cell_points = list()
    live_cell_points.append(Point(0,0))
    live_cell_points.append(Point(1,0))
    live_cell_points.append(Point(2,0))
    live_cell_points.append(Point(2,-1))
    live_cell_points.append(Point(1,-2))
    i_universe_view = ConsoleUi()
    i_universe = Universe( uuid.uuid4(), 'my universe', LiveCells(live_cell_points))
    ctrlr = UniverseController(i_universe, list([i_universe_view]))
    ctrlr.start()
