from Cocoa import *
from Foundation import *
from Quartz import *
from PyObjCTools import AppHelper
from objc import *
from time import *

class AppDelegate(NSObject):
    # applicationDidFinishLaunching_ Inicializa las variable del objeto.
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSMouseMovedMask, self.mouseMoved)
        self.d = CGPointMake(0.0, 0.0)
        self.a = CGPointMake(0.0, 0.0)
        self.v = CGPointMake(0.0, 0.0)
        self.p = CGPointMake(400.0,0.0)
        self.t = time()
        self.setTimer()

    #setScreenBounds 
    def setScreenBounds(self, screenBounds):
        self.screenBounds = screenBounds

    #timeElapsed Calcula la diferencia de dos tiempos.
    def timeElapsed(self, t0, t1):
        return t0 - t1

    #calcAcceleration devuelve la aceleracion del cursor en pantalla. 
    #delta: Es una variable de tipo CGPointMake que se utiliza como
    #un vector de velocidad
    #k: Es un escalar que multiplica el vector. 

    def calcAcceleration(self, delta, k=1):
        #return CGPointMake(delta.x*k, delta.y*k)
        return CGPointMake(0, delta.y*k)

    #calcVelocity calcula la velocidad del cursor en pantalla.
    #v0 es la velocidad al momento del calculo del cursor en pantalla
    #a es la aceleracion del cursor en pantalla

    def calcVelocity(self, v0, a):
        #return CGPointMake(v0.x + a.x, v0.y + a.y)
        return CGPointMake(v0.x, v0.y + a.y)
        
    #calcPosition devuelve la posicion del cursor en pantalla
    #p0 es la posicion inicial del cursor
    #v la velocidad actual del cursor en pantalla
    #t no tengo idea de que es? y no tengo idea de por que es tan grande
    def calcPosition(self, p0, v, t):
       # return CGPointMake(p0.x + (v.x*t), p0.y + (v.y*t))
        return CGPointMake(p0.x, p0.y + (v.y))

    #switchYOrigin 

    def switchYOrigin(self, point):
        return CGPointMake(point.x, self.screenBounds.size.height - point.y)

    #mouseMoved es una metodo de la clase AppDelegate que sera administrada por el sistema
    #el metodo tomara el movimiento relativo del trackpad y lo grabara en una variable
    #con esta variable se calculara la aceleracion del cursor en pantalla.
    #con la aceleracion del cursor en pantalla se calculara la velocidad del cursor en pantalla
    def mouseMoved(self, event):
        #print dir(event)
        #if self.p.x == 0 and self.p.y == 0:
            #self.p = self.switchYOrigin(event.locationInWindow())
        #print "delta D: (%d, %d)" % (event.deltaX(), event.deltaY())
        self.d = CGPointMake(event.deltaX(), event.deltaY())
        

    #setTimer 
    def setTimer(self):
        sel = objc.selector(self.updateCursor,signature='v@:')
        self.timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(0.2,self,sel,None,True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(
                self.timer, NSDefaultRunLoopMode)

    #updateCursor  
    def updateCursor(self):
        t1 = time()
        te = self.timeElapsed(self.t, t1)
        self.a = self.calcAcceleration(self.d)
        self.v = self.calcVelocity(self.v, self.a)
        self.p = self.calcPosition(self.p, self.v, te)
        self.moveMouse(self.p)
        print 'Delt='+ repr(self.d) + '\t\tAcel= '+ repr(self.a) + '\t\tVel = ' + repr(self.v) + '\t\ttime =' + repr(self.t) + '\t\tCurrentPos = ' + repr(self.p)
        self.d = CGPointMake(0.0,0.0)

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
