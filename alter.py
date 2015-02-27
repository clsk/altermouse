from Cocoa import *
from Foundation import *
from Quartz import *
from PyObjCTools import AppHelper
from time import *


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSMouseMovedMask, self.mouseMoved)
        self.v = CGPointMake(0.0, 0.0)
        self.p = CGPointMake(0.0, 0.0)
        self.t = time()

    def setScreenBounds(self, screenBounds):
        self.screenBounds = screenBounds

    def timeElapsed(t0, t1):
        return t0 - t1

    def calcAcceleration(delta, k=1):
        return CGPointMake(delta.x*k, delta.y*k)

    def calcVelocity(v0, a):
        return CGPointMake(v0.x + a.x, v0.y + a.y)

    def calcPosition(p0, v, t):
        return CGPointMake(p0.x + (v.x*t), p0.y + (v.y*t))

    def switchYOrigin(self, point):
        return CGPointMake(point.x, self.screenBounds.size.height - point.y)

    def mouseMoved(self, event):
        #print dir(event)
        if self.p.x == 0 and self.p.y == 0:
            self.p = self.switchYOrigin(event.locationInWindow())
        print self.switchYOrigin(event.locationInWindow())
        #print "delta D: (%d, %d)" % (event.deltaX(), event.deltaY())
        self.v = self.calcVelocity(self.v, self.calcAcceleration(CGPointMake(event.deltaX(), event.deltaY())))
        #self.moveMouse(CGPointMake(event.deltaX(), event.deltaY()))

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
