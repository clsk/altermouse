from Cocoa import *
from Foundation import *
from Quartz import *
from PyObjCTools import AppHelper
from objc import *
from time import *

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSMouseMovedMask, self.mouseMoved)
        self.v = CGPointMake(0.0, 0.0)
        self.p = CGPointMake(0.0, 0.0)
        self.t = time()
        self.setTimer()

    def setScreenBounds(self, screenBounds):
        self.screenBounds = screenBounds

    def timeElapsed(self, t0, t1):
        return t0 - t1

    def calcAcceleration(self, delta, k=1):
        return CGPointMake(delta.x*k, delta.y*k)

    def calcVelocity(self, v0, a):
        return CGPointMake(v0.x + a.x, v0.y + a.y)

    def calcPosition(self, p0, v, t):
        return CGPointMake(p0.x + (v.x*t), p0.y + (v.y*t))

    def switchYOrigin(self, point):
        return CGPointMake(point.x, self.screenBounds.size.height - point.y)

    def mouseMoved(self, event):
        #print dir(event)
        if self.p.x == 0 and self.p.y == 0:
            self.p = self.switchYOrigin(event.locationInWindow())
        #print self.switchYOrigin(event.locationInWindow())
        #print "delta D: (%d, %d)" % (event.deltaX(), event.deltaY())
        delta = CGPointMake(event.deltaX(), event.deltaY())
        a = self.calcAcceleration(delta)
        self.v = self.calcVelocity(self.v, a)

    def setTimer(self):
        sel = objc.selector(self.updateCursor,signature='v@:')
        self.timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(0.2,self,sel,None,True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(
                self.timer, NSDefaultRunLoopMode)

    def updateCursor(self):
        t1 = time()
        te = self.timeElapsed(self.t, t1)
        self.p = self.calcPosition(self.p, self.v, te)
        self.moveMouse(self.p)
        print 'updated cursor to ' + repr(self.p)

    def moveMouse(self, to):
        evsrc = CGEventSourceCreate(kCGEventSourceStateCombinedSessionState);
        CGEventSourceSetLocalEventsSuppressionInterval(evsrc, 0.0);
        CGAssociateMouseAndMouseCursorPosition (0);
        CGWarpMouseCursorPosition(to);
        CGAssociateMouseAndMouseCursorPosition (1);

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    delegate.setScreenBounds(CGDisplayBounds(CGMainDisplayID()))
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()


if __name__ == '__main__':
   main()
