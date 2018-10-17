'''
Methods for simple math visualizations using the Bokeh interactive graphics library.
'''
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead, grids
import numpy as np
import random
output_notebook()

class LinearAlgebra:
    '''
    Method offers simple visualizations in R2 space using Bokeh.
    Class generated for instruction purposes.
    '''
    def __init__(self,
                 origin=np.array([0,0]),
                 basis=np.array([[1,0],
                                 [0,1]])):
        self.color = ['blue','red','green','orange','purple',
                      'steelblue','darkred','darkgreen']
        self.basis = basis
        self.origin = self.basis.dot(origin)
        self.vectors = []


    def grid_line(self,unit_vector=np.array([1,0]),
          scale=1,basis=None,
          y_nudge=0,x_nudge=0,
          alpha=1,lwd=1):
        '''Generate grid lines on plot
        '''
        axis = scale*unit_vector.dot(basis)
        self.plot.line([-1*axis[0]+y_nudge,axis[0]+y_nudge],
                  [-1*axis[1]+x_nudge,axis[1]+x_nudge],line_width=lwd,
                  color='black',alpha=alpha)

    def graph(self,extent = 5,dim=400,grid=False):
        '''Generate 2D graph

        Arguments:

            - extent: the unit size the graph should be.
        '''
        self.plot = figure(plot_width=dim,
                          plot_height=dim,
                          tools = "wheel_zoom,pan,reset",
                          x_range=(-extent*.7, extent*.7),
                          y_range=(-extent*.7, extent*.7))

        if grid:
            self.grid_line(np.array([0,1]),scale=extent,basis=self.basis,lwd=2)
            self.grid_line(np.array([1,0]),scale=extent,basis=self.basis,lwd=2)

            # Plot grid lines
            for i in range(-(extent*2),(extent*2)+1):
                self.grid_line(np.array([0,1]),scale=extent,basis=self.basis,y_nudge=i,alpha=.5)
                self.grid_line(np.array([1,0]),scale=extent,basis=self.basis,x_nudge=i,alpha=.5)

        else:
            self.grid_line(np.array([0,1]),scale=extent,basis=self.basis,lwd=1.5)
            self.grid_line(np.array([1,0]),scale=extent,basis=self.basis,lwd=1.5)


    def change_origin(self,new_origin):
        '''
        Change the origin of the coordinate system
        '''
        self.origin = new_origin

    def std_origin(self):
        '''
        Converts back to the standard origin (0 vector) of
        the coordinate system
        '''
        self.origin = self.basis.dot(np.array([0,0]))

    def change_basis(self,new_basis):
        '''
        Change the basis of the coordinate system
        '''
        self.basis = new_basis

    def vector(self,vector=None,add_color=None,alpha=1,lwd=3):
        '''
        Visualize a vector in R2.

        Arguments:
            - vector: numpy array with two elements.

            - add_color: provide a string value for a specific colorself.
            Default is None. If None, a color from a specified (bu finite)
            assortment is drawn from.
        '''
        if add_color is None:
            color = self.color.pop(0) # Draw a new color from the selection
        elif isinstance(add_color,str):
            color = add_color
        else:
            color = "black"

        # Apply the vector to our standard coordinate system
        new_vector = self.basis.dot(vector)
        self.vectors.append(new_vector) # store vector

        # Alter if origin is different
        if np.count_nonzero(self.origin)!=0:
            new_vector = new_vector + self.origin


        # Plot vector
        self.plot.add_layout(Arrow(end=NormalHead(fill_color=color,fill_alpha=alpha,
                                                  size=10,line_color=color,
                                                  line_alpha=alpha),
                       x_start=self.origin[0], y_start=self.origin[1],
                                   line_color=color,line_alpha=alpha,
                       x_end=new_vector[0], y_end=new_vector[1],line_width=lwd))


    def dump_vecs(self,vectors,alpha=.3):
        '''
        Plot many two dimensional vectors in R2.

        Arguments:
            vectors: Matrix must be a vector of 2XN.
        '''
        for vector in vectors:
               self.vector(vector,add_color=False,alpha=alpha)


    def add_vectors(self,vec_1=None,vec_2=None):
        '''Visualize adding two vectors

        Arguments:
            - vec_1: 2d numpy array
            - vec_2: 2d numpy array
        '''
        # Add the two input vectors
        v3 = vec_1+ vec_2

        self.vector(vector=vec_1)
        self.vector(vector=vec_2,)
        hold_origin = self.origin
        self.change_origin(vec_1) # Temporarily reset the origin
        self.vector(vector=vec_2,add_color = 'red',alpha=.3)
        self.change_origin(hold_origin) # return back to original location


    def subtract_vectors(self,vec_1=None,vec_2=None):
        '''Visualize subtracting between two vectors

        Arguments:
            - vec_1: 2d numpy array
            - vec_2: 2d numpy array
        '''
        v3 = vec_1 - vec_2

        self.vector(vector=vec_1)
        self.vector(vector=vec_2)
        hold_origin = self.origin
        self.origin = vec_2 # Temporarily reset the origin
        self.vector(vector=v3,add_color = 'purple',alpha=.3)
        self.origin = hold_origin


    def projection(self,vec_1=None,vec_2=None):
        '''
        Visualize a projection of one vector onto another.
        '''
        self.vector(vec_1,alpha=.7)
        self.vector(vec_2,alpha=.7)

        # Generate projection scalar
        c = vec_1.dot(vec_2)/vec_1.dot(vec_1)

        shadow_vector = c*vec_1
        self.vector(shadow_vector,add_color="black",lwd=4)

        orth_vec = vec_2 - c*vec_1
        self.change_origin(vec_2)
        self.vector(-orth_vec,add_color="grey",alpha=.4)
        self.std_origin()

    def clear(self):
        '''
        Clear the existing plot
        '''
        del self.plot # dump plot
        self.basis = np.array([[1,0],[0,1]]) # revert back to standard basis
        self.std_origin()

        #restart the color scheme
        self.color = ['blue','red','green','orange','purple',
                      'steelblue','darkred','darkgreen']
        self.vectors = []
        return self



    def show(self):
        show(self.plot)
