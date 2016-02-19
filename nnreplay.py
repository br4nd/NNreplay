#!/usr/local/bin/python
import numpy as np
import scipy.linalg as linalg
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.widgets import Button
import Tkinter, tkFileDialog
import time
import collections

import getopt
import pdb
from pprint import pprint as pp

import os, sys
from os import path

sys.path.insert(0,os.path.abspath('..'))
import lib
import solvers

axisLimits = [] # autoscale
#axisLimits = [-20, 25, -5, 40]
wpLabelList = [1,2,3,4]
figSize = [10,10]
RECORD_MOVIE = True  # Easy way to turn it on/off
PLOT_WAYPOINTS = False
EKF_PY = False
MOBILE_UNDER_TEST = 112
KBHIT = True
#KBHIT = False

def main(argv) :

    pn = '/Volumes/Transcend/Data/NavNet'
    # fn = 'Lobby_DOP_Tests/Lobby_DOP_Low_001.csv'
    # fn = 'Lobby_DOP_Tests/Lobby_DOP_SweetSpot_000.csv'
    # fn = 'Lobby_DOP_Tests/Lobby_DOP_Zero_002.csv'
    # fn = 'Lobby_DOP_Tests/Lobby_DOP2_BasdSpot2_005.csv'
    fn = 'Lobby_DOP_Tests/Lobby_DOP3_BasdSpot_001.csv'
    ffn_in = os.path.join(pn,fn)


#    ffn_in = '/Volumes/Transcend/Data/NavNet/Lobby_Debug_BadSpot/Lobby_Debug_BadSpot_30ms_004.csv'
#    ffn_in = []  # uncomment this to query the user
    if not 'ffn_in' in locals() or not ffn_in :  # if empty
        ffn_in = lib.query_file()
#    pdb.set_trace()

    [pn,fn] = os.path.split(ffn_in)
    fnNoExt = os.path.splitext(fn)[0]
    ffn_noext = os.path.join(pn,fnNoExt)
    gui = gui2D(ffn_in, axisLimits, trailLen=10, rescaleFlag=False)
    movie = lib.moviewriter(gui.fig, ffn_noext, enabled=RECORD_MOVIE, fps=15, dpi=200)

    map = LMAP()
    gameInfo = []
    ekf = []

    if KBHIT :
        kb = lib.kbhit()

    Tstart = []
    Tsaved = []
#    lee_saved = []
#    dt_saved = []
#    t_prev = []

    anc_buf_len = 4
    ancID_buf = collections.deque(maxlen=anc_buf_len)
    ancLoc_buf = collections.deque(maxlen=anc_buf_len)
    dop_saved = []
    doppy_saved = []
    innovation_saved = []
    msgid = 999999
    nRanges = 0
    nLocs = 0
    STEP = False
    with open(ffn_in,'r') as f:
        iline = 0

        while True:
            line = f.readline()
            if not line :  break
            if len(line) < 3 :  continue
            iline += 1

            # if iline >= 44 and iline < 500 :
            #     continue
#            pdb.set_trace()

            print '%d: %s' % (iline,line[0:-1])
#            print line[0:-1]

            msg = lib.parse_msg(line)

            if not msg : # msg is empty
                continue

            if 'RcmGetStatusInfoConfirm' == msg['msgType'] :
                rcmStatus = msg

            elif 'RcmP3XXConfig' == msg['msgType'] :
                rcmConfig = msg
                thisNodeID = rcmConfig['NodeId']
                radioType = 'P3XX'

            elif 'RcmConfig' == msg['msgType'] :
                rcmConfig = msg
                thisNodeID = rcmConfig['NodeID']
                radioType = 'P4XX'

            elif 'RnGetConfigConfirm' == msg['msgType'] :
                rnConfig = msg

            elif 'RnGetAlohaConfigConfirm' == msg['msgType'] :
                rnAlohaConfig = msg

            elif 'NnConfig' == msg['msgType'] :
                nnConfig = msg

            elif 'NnLocationMapEntry' == msg['msgType'] :
                map.add(msg['NodeID'],msg['NodeType'],msg['X'],msg['Y'],msg['Z'])

                if msg['NodeType'] == 'Anchor' :
                    gui.drawAnchor(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                elif msg['NodeType'] == 'Origin' :
                    gui.drawAnchor(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                elif msg['NodeType'] == '-X' :
                    gui.drawAnchor(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                elif msg['NodeType'] == '+Y' :
                    gui.drawAnchor(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                elif msg['NodeType'] == 'Z' :
                    gui.drawAnchor(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                elif msg['NodeType'] == 'Mobile' :
                    # TODO support all mobiles
                    if MOBILE_UNDER_TEST == msg['NodeID'] :
                        gui.drawMobile(0,msg['NodeID'],msg['X'],msg['Y'],msg['Z'],0,'r')
                else :
                    print 'Invalid NodeType: ', msg['NodeType']
                    pdb.set_trace()
                    pass

            elif 'NnWaypointEntry' == msg['msgType'] :
                # update lmap and plot
                if PLOT_WAYPOINTS :
                    map.add(msg['ID'],msg['NodeType'],msg['X'],msg['Y'],msg['Z'])
                    gui.drawWaypoint(msg['ID'],msg['X'],msg['Y'],msg['Z'],wpLabelList)

            elif 'RcmRangeInfo' == msg['msgType'] or ('RcmEchoedRangeInfo' == msg['msgType'] and MOBILE_UNDER_TEST == msg['RequesterID']) :
                # TODO support all mobiles
                rangeInfo = msg

                nRanges += 1
                if 'RcmRangeInfo'== msg['msgType'] :
                    rangeInfo['RequesterID'] = thisNodeID
                if not Tstart :
                    Tstart = rangeInfo['Timestamp']
                Tsaved.append(rangeInfo['Timestamp']-Tstart)

                # if rangeInfo['RangeStatus'] != 0 :
                #     anchorID_buf.append(anchorID_buf[-1])
                #     anchorLoc_buf.append(anchorLoc_buf[-1])

                # Moved this to NnLocInfo for alignment in time
                #gui.drawRangeLine(rangeInfo['RequesterID'],rangeInfo['ResponderID'],map)

                # timestamp = rangeInfo['Timestamp']
                # rMeas = rangeInfo['PrecisionRange']
                # ree = rangeInfo['PrecisionRangeErrEst']
                # rspLoc = map.getLoc(rangeInfo['ResponderID'])

            elif ('NnLocationInfo' == msg['msgType'] or 'NnEchoLastLocationExInfo' == msg['msgType'] or 'NnEchoedLocationInfo' == msg['msgType']) and MOBILE_UNDER_TEST == msg['NodeID'] :
                locInfo = msg
                print '   SolverStage(%d), SolverError(%d), x(%.3f), y(%.3f), DOP(%.3f), nAnchors(%d), xvar(%.5f), yvar(%.5f), xycov(%.5f)' %\
                    (locInfo['SolverStage'],locInfo['SolverError'],locInfo['X'],locInfo['Y'],locInfo['DOP'],locInfo['NumAnchors'],
                     locInfo['XVariance'],locInfo['YVariance'],locInfo['XYCovariance'])
                nLocs += 1
                map.update(msg['NodeID'],msg['X'],msg['Y'],msg['Z'])

                dop_saved.append((locInfo['MessageID'],locInfo['DOP'],locInfo['NumAnchors']))

                if locInfo['SolverStage'] == 0 :
                    mobColor = 'red'
                elif locInfo['SolverStage'] == 1 :
                    mobColor = 'orange'
                elif locInfo['SolverStage'] == 2 :
                    mobColor = 'blue'
                elif locInfo['SolverStage'] == 3 :
                    mobColor = 'green'
                else :
                    pdb.set_trace()
                #    mobColor = 'gray'

                # if rangeInfo['PrecisionRangeErrEst'] == .056 :
                #     pdb.set_trace()

                # Update anchor buffer for GDOP
                if rangeInfo['PrecisionRangeErrEst'] < 0.056 :
                    ancID = rangeInfo['ResponderID']
                else :
                    ancID = ancID_buf[-1]
                ancID_buf.append(ancID)
                ancLoc = map.getLoc(ancID)
                ancLoc_buf.append(ancLoc)

                # First time through fill it up with repeats
                if len(ancID_buf) == 1 :
                    for _ in range(3) :
                        ancID_buf.append(ancID)
                        ancLoc_buf.append(ancLoc)

                A0 = ancLoc_buf[0];
                A1 = ancLoc_buf[1];
                A2 = ancLoc_buf[2];
                A3 = ancLoc_buf[3]
                M = [locInfo['X'],locInfo['Y'],locInfo['Z']]
                doppy = solvers.gdop4_2D( M, A0, A1, A2, A3 )
                #dop = solvers.gdop3_2D( M, A0, A1, A2 )
                nApy = len(np.unique(ancID_buf))
                print '   doppy: %5.3f, nApy: %d anchorIDs: %d %d %d %d'\
                        % (doppy,nApy,ancID_buf[0],ancID_buf[1],ancID_buf[2],ancID_buf[3])
                doppy_saved.append((locInfo['MessageID'],doppy,nApy))

                if debugMsg['dbgMsgType'] == 'KS2dM' :
                    innovation = debugMsg['range'] - debugMsg['predictedRange']
                    innovation_saved.append((locInfo['MessageID'], innovation))

                #pdb.set_trace()
                label = '  node%d: stage:%d, err:%d,\n  dop:  % 5.2f, nA:  %d,\n  doppy:% 4.2f, nApy:%d,\n  A[%d,%d,%d,%d],\n  rspID:%d, rng:%5.3f, ree:%d'\
                    % (locInfo['NodeID'],locInfo['SolverStage'],locInfo['SolverError'],
                    locInfo['DOP'], locInfo['NumAnchors'], doppy, nApy,
                    ancID_buf[0], ancID_buf[1], ancID_buf[2], ancID_buf[3],
                    rangeInfo['ResponderID'], rangeInfo['PrecisionRange'],int(1000*rangeInfo['PrecisionRangeErrEst']))

                P = np.array([[locInfo['XVariance'], locInfo['XYCovariance']],
                              [locInfo['XYCovariance'], locInfo['YVariance']]])
                gui.drawMobile(msg['MessageID'],msg['NodeID'],msg['X'],msg['Y'],msg['Z'],label,color=mobColor,covariance=P)

                linecolor = 'k'
                if rangeInfo['RangeStatus'] != 0 or rangeInfo['PrecisionRangeErrEst'] > 0.1 :
                    linecolor = 'r'
#                    pdb.set_trace()
                gui.drawRangeLine(rangeInfo['RequesterID'],rangeInfo['ResponderID'],map,linecolor)

                if rangeInfo['RangeStatus'] != 0 :
                    pdb.set_trace()
                    pass

                movie.update()

                #----------------------PY EKF
                if EKF_PY and locInfo['SolverStage'] == 3 and debugMsg['dbgMsgType'] == 'KS2dM' :
                    if not ekf :
                        x = debugMsg['state'][0]
                        xd = debugMsg['state'][2]
                        y = debugMsg['state'][1]
                        yd = debugMsg['state'][3]
                        X = [x, xd, y, yd]
                        P = []
                        z = debugMsg['m_localZHeight']
                        aee = debugMsg['sigmaAccel']

                        ekf = solvers.ekf_2d(X, P, aee=aee, zFixed=z)

                        t_emb_prev = rangeInfo['EmbeddedTimestamp']

                    else :
                        dt_range = rangeInfo['EmbeddedTimestamp'] - t_emb_prev
                        t_emb_prev = rangeInfo['EmbeddedTimestamp']

                        ekf.predict( dt=dt_range, aee=aee)

                        r_meas = rangeInfo['PrecisionRange']
                        ree = rangeInfo['PrecisionRangeErrEst']
                        refLoc = debugMsg['anchorLoc']

                        ekf.update( r_meas, ree, refLoc )

                    gui.draw_mobpy(ekf.X[0],ekf.X[2])

                #-------------- Stop on MSGID
                # if locInfo['SolverStage'] < 3 :
                #     STEP = True
                #     print '  SOLVER REBIRTH: msgid(%d), doppy(%4.2f), nApy(%d)' %\
                #         (locInfo['MessageID'],doppy,nApy)
                # if STEP :
                #     pdb.set_trace()

                # if 6915 <= locInfo['MessageID'] :
                #     pdb.set_trace()

                if gameInfo :
                    gameInfo['elapsedTime'] = msg['Timestamp'] - gameInfo['startTime']
                    gui.updateTime(gameInfo['elapsedTime'])

            elif 'RcmInternalDebugInfo' == msg['msgType'] :
                debugMsg = msg
                pass

            elif 'GameConfig' == msg['msgType'] :
                gameInfo = msg
                gameInfo['mobileID'] = 112
                gameInfo['wpList'] = [msg['Waypoint1'],msg['Waypoint2'],msg['Waypoint3']]
                gameInfo['errors'] = [0, 0, 0]
                gameInfo['markerCount'] = 0
                gameInfo['startTime'] = msg['Timestamp']
                gameInfo['elapsedTime'] = 0
                gameInfo['elapsedTime_prev'] = gameInfo['elapsedTime']
                gameInfo['timestamps'] = [msg['Timestamp'], 0, 0, 0]
                print 'GAME CONFIG: Walker: %s, Caller: %s Waypoints: [%d,%d,%d]' % (msg['WalkerInitials'],msg['CallerInitials'],msg['Waypoint1'],msg['Waypoint2'],msg['Waypoint3'])
                gui.markWaypoints(gameInfo['wpList'],map)

            elif 'LogfileMarker' == msg['msgType'] :
                #print 'LogfileMarker - Compute and store slant range error here'
                wpIndex = msg['markerNum']-1
                wpID = gameInfo['wpList'][wpIndex]
                mobID = gameInfo['mobileID']
                wpLoc = np.array(map.getLoc(wpID))
                mobLoc = np.array(map.getLoc(mobID))
                plt.plot(mobLoc[0],mobLoc[1],'*',markersize=10,markerfacecolor='k',hold=True)
                slantErr = np.linalg.norm(wpLoc-mobLoc)
                gameInfo['errors'][wpIndex] = slantErr
                gameInfo['markerCount'] += 1
                gameInfo['elapsedTime'] = msg['Timestamp'] - gameInfo['startTime']
                gameInfo['splitTime'] = gameInfo['elapsedTime'] - gameInfo['elapsedTime_prev']
                gameInfo['elapsedTime_prev'] = gameInfo['elapsedTime']
                gameInfo['timestamps'][wpIndex+1] = msg['Timestamp']
                plt.text(mobLoc[0]+1.,mobLoc[1]+1.5,'Split Time: %5.3f s' % gameInfo['splitTime'],fontsize=14)
                plt.text(mobLoc[0]+1.,mobLoc[1]+0.5,'Split Error: %5.3f m' % slantErr,fontsize=14)
                if gameInfo['markerCount'] == 3 :
                    # game over
                    totalTime = msg['Timestamp'] - gameInfo['startTime']
                    totalError = sum(gameInfo['errors'])
                    meanError = np.mean(gameInfo['errors'])
                    plt.text(mobLoc[0]+1.,mobLoc[1]-1.0,'Total Time: %5.2f s' % totalTime,fontsize=14)
                    plt.text(mobLoc[0]+1.,mobLoc[1]-2.0,'Total Error: %5.3f m' % totalError,fontsize=14)
                    plt.text(mobLoc[0]+1.,mobLoc[1]-3.0,'Mean Error: %5.3f m' % meanError,fontsize=14)
                    print 'Total time = %5.3f' % totalTime
                    print 'Total error (m) = %6.4f' % totalError
                    print 'Mean error (m) = %6.4f' % meanError
                    response = raw_input("Press 'c' to continue, any other key to exit >>> ")

                    if not response or response[0] != 'c' :
                        return

            else :
                print 'UNKNOWN UNPROCESSED MESSAGE: ', msg['msgType']

            if KBHIT :
                if kb.kbhit():
                    c = kb.getch()
                    kb.set_normal_term()
                    break

            # if STEP == True:
            #     break

            if iline > 1000 :
                pass
                #break

            # if msg :
            #     if msg['msgType'] == 'NnEchoLastLocationExInfo' :
            #         if msg['MessageID'] > 700 :
            #             break

#            time.sleep(.1)

    movie.finish()  # Internally checks for SAVE_MOVIE flag
#    pdb.set_trace()
    dT = msg['Timestamp'] - Tstart
    rangeRate = nRanges/dT
    locRate = nLocs/dT
    print 'nRanges=%d, nLocs=%d, dT=%.3f, rangeRate=%.3f, locRate=%.3f' % (nRanges,nLocs,dT,rangeRate,locRate)
    dTvec = np.diff(Tsaved)
    fig_dT = plt.figure()

    plt.subplot(211)
    dop_saved = np.array(dop_saved,dtype=[('msgid','i4'),('dop','f4'),('nA','i4')])
    plt.plot(dop_saved['msgid'],dop_saved['dop'],'g.-')
    doppy_saved = np.array(doppy_saved,dtype=[('msgid','i4'),('doppy','f4'),('nApy','f4')])
    plt.plot(doppy_saved['msgid'],doppy_saved['doppy'],'m.-')
    plt.ylabel('hdop')
#    plt.tick_params(labelbottom='off')
    plt.grid(True)

    plt.subplot(212)
    plt.plot(dop_saved['msgid'],dop_saved['nA'],'g.-')
    plt.plot(doppy_saved['msgid'],doppy_saved['nApy'],'m.-')
    plt.ylabel('nAnchors')
#    plt.tick_params(labelbottom='off')
    plt.yticks([0,1,2,3,4,5])
    plt.grid(True)

    # plt.subplot(313)
    # innovation_saved = np.array(innovation_saved,dtype=[('msgid','i4'),('innov','f4')])
    # plt.plot(innovation_saved['msgid'],np.abs(innovation_saved['innov']),'c.-')
    # plt.ylabel('innovation')
    # plt.grid(True)
    # plt.xlabel('MessageID')

    plt.draw()

    print 'DONE! (press cntl-d to exit)'
    pdb.set_trace()


class gui2D :
    mob = []
    mobpy = []
    rline = []
    msgID = []
    ancColor = 'b'

    def __init__(self,ffn,axisLimits,trailLen=20,rescaleFlag=True) :

        [pn,fn] = os.path.split(ffn)
        self.fn = os.path.splitext(fn)[0]

        plt.ion()
        self.fig = plt.figure(figsize=figSize)
        self.ax = self.fig.add_subplot(111)

        if any(axisLimits) :
            self.rescaleFlag = rescaleFlag
            plt.axis(axisLimits)
            self.axisLimits = axisLimits
        else :
            self.rescaleFlag = rescaleFlag
            self.axisLimits = [np.inf, -np.inf, np.inf, -np.inf]
            plt.axis('equal')

        A = np.array([(np.nan, np.nan, 'k')],dtype=[('x','f4'),('y','f4'),('color','S10')])
        self.trail = np.repeat([A],trailLen,axis=0)
        self.trailLen = trailLen
        self.trailH = []
        for i in range(trailLen) :
            self.trailH.extend(plt.plot(0,0,'dk',visible=False))

        self.textH = plt.text(0,0,'',visible=False)

        plt.grid(True)
        plt.title('%s' % self.fn)

    def rescaleAxis(self,x,y) :
        if not self.rescaleFlag :
            return
        if abs(x) > 100 :
            return
        if abs(y) > 100 :
            return
        if self.axisLimits[0] > x :
            self.axisLimits[0] = x
        if self.axisLimits[1] < x :
            self.axisLimits[1] = x
        if self.axisLimits[2] > y :
            self.axisLimits[2] = y
        if self.axisLimits[3] < y :
            self.axisLimits[3] = y
        plt.xlim(self.axisLimits[0]-1,self.axisLimits[1]+1)
        plt.ylim(self.axisLimits[2]-1,self.axisLimits[3]+1)
        plt.axis('equal')

    def drawAnchor(self,nodeID,x,y,z) :
        plt.plot(x,y,'o',markersize=8,markerfacecolor=self.ancColor,hold=True)
        plt.text(x,y,nodeID,verticalalignment='top')
        if self.rescaleFlag :
            self.rescaleAxis(x,y)
        plt.draw()

    def drawWaypoint(self,nodeID,x,y,z,wpLabelList) :
        # plt.plot(x,y,'o',markersize=16,markerfacecolor='none',hold=True)
        circle = plt.Circle((x,y),.5,color='.5',fill=False)
        plt.gcf().gca().add_artist(circle)
        if nodeID in wpLabelList :
            plt.text(x+.4,y-.4,nodeID,verticalalignment='top',color='.5')
        if self.rescaleFlag :
            self.rescaleAxis(x,y)
        plt.draw()

    def drawErrorEllipse(self,mean,covariance,stdGain,color) :
        deviations = stdGain
        P = covariance
        U,s,v = linalg.svd(P)
        orientation = math.atan2(U[1,0],U[0,0])
        width  = deviations*math.sqrt(s[0])
        height = deviations*math.sqrt(s[1])
        ellipse = (orientation, width, height)

        angle = np.degrees(ellipse[0])
        width = ellipse[1] * 2.
        height = ellipse[2] * 2.

        if self.ellipse :
            self.ellipse.remove()

        self.ellipse = Ellipse(xy=mean,width=width,height=height,angle=angle,fill=False,ec=color,lw=1,ls='solid')
        self.ax.add_patch(self.ellipse)

    def drawMobile(self,msgID,nodeID,x,y,z,label,color,covariance=np.zeros((2,2))) :

        self.updateMsgID(msgID)

        if not self.mob :
            self.locPrev = (x,y,z)
            self.mob, = plt.plot(x,y,'d',markersize=8,markerfacecolor=color)
            self.colorPrev = color

            self.txt = plt.text(x,y,label,verticalalignment='top')

            self.ellipse = []
            if covariance.any() :
                self.drawErrorEllipse(mean=(x,y),covariance=covariance,stdGain=1,color=color)
        else :

            self.mob.set_xdata(x)
            self.mob.set_ydata(y)
            self.mob.set_markerfacecolor(color)
            self.drawErrorEllipse((x,y),covariance,1,color)

            plt.plot([x,self.locPrev[0]],[y,self.locPrev[1]],':.',markersize=5,color=self.colorPrev)
            self.locPrev = (x,y,z)
            self.colorPrev = color

            self.txt.set_x(x)
            self.txt.set_y(y)

        self.txt.set_text(label)
        self.txt.set_color(color)

        plt.draw()

    def draw_mobpy(self,x,y) :
        if not self.mobpy :
            self.mobpy, = plt.plot(x,y,'s',markersize=8,markerfacecolor='orange',hold=True)
        else :
            self.mobpy.set_data(x,y)
        plt.draw()

    def markWaypoints(self,wpList,map) :
        for iWP in range(0,len(wpList)) :
            wpIndex = map.nodeIDs.index(wpList[iWP])
            nodeID = map.nodeIDs[wpIndex]
            x = map.X[wpIndex]
            y = map.Y[wpIndex]
            #z = map.Z[iWP]
            plt.plot(x,y,'o',markersize=20,linewidth=5,markerfacecolor='g',hold=True)
            plt.plot(x,y,'o',markersize=15,linewidth=5,markerfacecolor='w',hold=True)
            plt.text(x-.03,y-.06,nodeID)
        plt.draw()

    def drawRangeLine(self,fromID,toID,map,color) :
        fromLoc = map.getLoc(fromID)
        toLoc = map.getLoc(toID)
        if not self.rline :
            self.rline, = self.ax.plot([fromLoc[0],toLoc[0]],[fromLoc[1],toLoc[1]],ls='--',lw=2,color=color)
        else :
            self.rline.set_xdata([fromLoc[0],toLoc[0]])
            self.rline.set_ydata([fromLoc[1],toLoc[1]])
            self.rline.set_color(color)

        plt.draw()

    def updateMsgID(self,msgID) :
        xmin,xmax = self.ax.get_xlim()
        ymin,ymax = self.ax.get_ylim()
        if not self.msgID :
            self.msgID = plt.text(xmax-.1,ymax-.1,('MsgID: %d' % msgID),ha='right',va='top',fontsize=14)
        else :
            self.msgID.set_text(('MsgID: %d' % msgID))
        plt.draw()


class LMAP :
    map = []
    nodeIDs = []
    nodeTypes = []
    X = []
    Y = []
    Z = []
    nEntries = 0

    def __init__(self) :
        pass

    def add(self,nodeID,nodeType,x,y,z) :
        self.map.append([nodeID,nodeType,x,y,z])
        self.nodeIDs.append(nodeID)
        self.nodeTypes.append(nodeType)
        self.X.append(x)
        self.Y.append(y)
        self.Z.append(z)
        self.nEntries += 1

    def update(self,nodeID,x,y,z) :
        index = self.nodeIDs.index(nodeID)
        self.map[index][2:] = [x, y, z]
        self.X[index] = x
        self.Y[index] = y
        self.Z[index] = z

    def pprint(self) :
        print 'LMAP: %d nodes\n%5s %5s %5s %9s %9s' % (self.nEntries,'NodeID','Type','X','Y','Z')
        for k in range(0,self.nEntries-1) :
            print '%5d %9s %9.3f %9.3f %9.3f' % (self.nodeIDs[k],self.nodeTypes[k],self.X[k],self.Y[k],self.Z[k])

    def getLoc(self,nodeID) :
        nodeIndex = self.nodeIDs.index(nodeID)
        return [self.X[nodeIndex],self.Y[nodeIndex],self.Z[nodeIndex]]


def queryUser() :
    root = Tkinter.Tk()
    root.withdraw() # don't want a full GUI
    root.update()
    ffn = tkFileDialog.askopenfilename(parent=root,title="Choose an input file",filetypes=[("Log files","*.csv")])
    return ffn


if __name__ == "__main__" :
    main(sys.argv[1:])
