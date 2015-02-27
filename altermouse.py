import Quartz

currentPoint = Quartz.CGPointMake(0,0)

def mouseMoved(proxy, t, event, refcon):
    # Do some sanity check.
    #if t != Quartz.kCGEventMouseMoved:
        #return event;

    global currentPoint
    print "before (%f, %f)" % (currentPoint.x, currentPoint.y);
    # The incoming mouse position.
    currentPoint = Quartz.CGEventGetLocation(event);

    # We can change aspects of the mouse event.
    # For example, we can use CGEventSetLoction(event, newLocation).
    # Here, we just print the location.
    print "after (%f, %f)" % (currentPoint.x, currentPoint.y);
    x = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGTabletEventPointX)
    y = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGTabletEventPointY)
    print "TabletEvent (%d, %d)" % (x, y)

    #moveMouse(CGPointMake(currentPoint.x+5, currentPoint.y+5));

    # We must return the event for it to be useful.
    return event

def timerCalled(timer, refcon):
    print 'timer Called'
    moveMouse(Quartz.CGPointMake(currentPoint.x+1, currentPoint.y+1))

def moveMouse(to):
    evsrc = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateCombinedSessionState);
    Quartz.CGEventSourceSetLocalEventsSuppressionInterval(evsrc, 0.0);
    Quartz.CGAssociateMouseAndMouseCursorPosition (0);
    Quartz.CGWarpMouseCursorPosition(to);
    Quartz.CGAssociateMouseAndMouseCursorPosition (1);


screenBounds = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
print 'the main screen is (%d, %d)' % (screenBounds.size.width, screenBounds.size.height)
#eventMask = (1 << Quartz.kCGEventMouseMoved)
#eventMask = (1 << Quartz.kCGEventMaskForAllEvents)

eventTap = Quartz.CGEventTapCreate(Quartz.kCGSessionEventTap, Quartz.kCGHeadInsertEventTap,
                            0, Quartz.kCGEventMaskForAllEvents, mouseMoved, None)
if eventTap is None:
    print 'Failed to create tap event'


runLoopSource = Quartz.CFMachPortCreateRunLoopSource(
                    Quartz.kCFAllocatorDefault, eventTap, 0)

# Add to the current run loop.
Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), runLoopSource,
                   Quartz.kCFRunLoopCommonModes);

timerEvent = Quartz.CFRunLoopTimerCreate(None, Quartz.CFAbsoluteTimeGetCurrent(), 0.3, 0, 0, timerCalled, None)
if timerEvent is None:
    print 'timerEvent is None'

Quartz.CFRunLoopAddTimer(Quartz.CFRunLoopGetCurrent(), timerEvent, Quartz.kCFRunLoopCommonModes)

# Enable the event tap.
Quartz.CGEventTapEnable(eventTap, True);

# Set it all running.
Quartz.CFRunLoopRun();


