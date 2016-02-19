#!/usr/local/bin/python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pdb
from pprint import pprint as pp

def triangleScore(P0,P1,P2) :

    x0 = P0[0]
    y0 = P0[1]
    z0 = P0[2]
    
    x1 = P1[0]
    y1 = P1[1]
    z1 = P1[2]

    x2 = P2[0]
    y2 = P2[1]
    z2 = P2[2]
        
    # Find the lengths of the edges
    len_a = np.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
    len_b = np.sqrt( (x0-x2)**2 + (y0-y2)**2 + (z0-z2)**2 )
    len_c = np.sqrt( (x0-x1)**2 + (y0-y1)**2 + (z0-z1)**2 )

    altitudeA = np.sqrt((len_b*len_c/(len_b+len_c)**2) *((len_b+len_c)**2-len_a**2));
    altitudeB = np.sqrt((len_a*len_c/(len_a+len_c)**2) *((len_a+len_c)**2-len_b**2));
    altitudeC = np.sqrt((len_a*len_b/(len_a+len_b)**2) *((len_a+len_b)**2-len_c**2));

    # High minimum height is best
    score = min([altitudeA, altitudeB, altitudeC])

#    pdb.set_trace()
    return score


if __name__ == "__main__" :

    # Start with some example triangle edge lengths
    a = 10.
    b = 10.
    c = 10.

    # Create the test coordinates
    xA = 0.
    yA = 0.
    zA = 0.
    
    xB = c
    yB = 0.
    zB = 0.

    angA = np.arccos((-a**2 + b**2 + c**2)/(2*b*c))
    angA_deg = angA*180./np.pi
    
    #angB = acos((-bh^2 + ah^2 + ch^2)/(2*ah*ch)); angleB_deg = angB*180/pi
    #angC = acos((-ch^2 + ah^2 + bh^2)/(2*ah*bh)); angleC_deg = angC*180/pi

    xC = b*np.cos(angA)
    yC = b*np.sin(angA)
    zC = 0.
    
    P0 = [xA,yA,zA]
    P1 = [xB,yB,zB]
    P2 = [xC,yC,zC]
    
    P0 = np.array([17862, 199, 2589])/1000.
    P1 = np.array([13679, 10648, 2544])/1000.
    P2 = np.array([17831, 10575, 2557])/1000.
    
    # Gut check
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot([P0[0],P1[0],P2[0],P0[0]], [P0[1],P1[1],P2[1],P0[1]],[P0[2],P1[2],P2[2],P0[2]], '.-');
    ax.text(P0[0],P1[0],P2[0],'A')
    ax.text(P0[1],P1[1],P2[1],'B')
    ax.text(P0[2],P1[2],P2[2],'C')

#    ax.axis('equal')
#    ax.axis([-5 15 15 
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    plt.draw()

    # Anchor Array
    Xvec = [xA, xB, xC]
    Yvec = [yA, yB, yC]

    AA = [Xvec,Yvec]

    # find score
    score = triangleScore(P0,P1,P2)
    print 'X = [%7.3f, %7.3f, %7.3f]' % (Xvec[0],Xvec[1],Xvec[2])
    print 'Y = [%7.3f, %7.3f, %7.3f]' % (Yvec[0],Yvec[1],Yvec[2])
    print 'score = %f\n' % score
    pdb.set_trace()

