
import re
'''
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update valid region < (x=0,
y=75, w=480, h=2229); >
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update invalid region < (x=0,
y=2304, w=480, h=256); >
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update old valid region < (x=0,
y=75, w=480, h=2229); >
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update stale region < >
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update view transform
(0,-8.52237) zoom 1.000000 abort 0
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update transformed compositor
bounds (x=0.000000, y=807.522339, w=480.000000, h=809.000000)
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update final coherency rect
(x=0, y=807, w=480, h=810)
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update final paint region <
(x=0, y=2304, w=480, h=256); >
I/Gecko   ( 3219): TILING 0xadc23000: Progressive update computed paint region <
(x=288, y=2304, w=192, h=256); > repeat 0

I/Gecko   ( 3219): TILING 0xadc23000: Found scrollAncestor 0xadc23000,
displayPortAncestor 0xadc23000, transform 0
I/Gecko   ( 3219): TILING 0xadc23000: Critical displayport (x=0, y=0, w=480,
    h=2560)
I/Gecko   ( 3219): TILING 0xadc23000: Resolution 1.5
I/Gecko   ( 3219): TILING 0xadc23000: Composition bounds (x=0.000000,
    y=928.000000, w=480.000000, h=809.000000)
I/Gecko   ( 3219): TILING 0xadc23000: Scroll offset (0,928)
I/Gecko   ( 3219): TILING 0xadc23000: First-transaction valid region < (x=0,
    y=75, w=480, h=2485); >
I/Gecko   ( 3219): TILING 0xadc23000: First-transaction invalid region < >
I/Gecko   ( 3219): TILING 0xadc23000: Low-precision invalid region < >
I/Gecko   ( 3219): TILING 0xadc23000: Paint finished
I/Gecko   ( 3219): TILING 0xaed72000: Initial visible region < (x=0, y=0, w=480,
    h=75); >
I/Gecko   ( 3219): TILING 0xaed72000: Initial valid region < (x=0, y=0, w=480,
    h=75); >
I/Gecko   ( 3219): TILING 0xaed72000: Initial low-precision valid region < >
I/Gecko   ( 3219): TILING 0xaed72000: Paint finished
I/Gecko   ( 3219): TILING 0xadc23000: Initial visible region < (x=0, y=75, w=480,
    h=2814); >
I/Gecko   ( 3219): TILING 0xadc23000: Initial valid region < (x=0, y=75, w=480,
    h=2485); >
I/Gecko   ( 3219): TILING 0xadc23000: Initial low-precision valid region < (x=0,
    y=2048, w=1152, h=1024); >
I/Gecko   ( 3219): TILING 0xadc23000: Found scrollAncestor 0xadc23000,
displayPortAncestor 0xadc23000, transform 0
I/Gecko   ( 3219): TILING 0xadc23000: Critical displayport (x=0, y=0, w=480,
    h=2560)
I/Gecko   ( 3219): TILING 0xadc23000: Resolution 1.5
I/Gecko   ( 3219): TILING 0xadc23000: Composition bounds (x=0.000000,
    y=928.000000, w=480.000000, h=809.000000)
I/Gecko   ( 3219): TILING 0xadc23000: Scroll offset (0,928)
I/Gecko   ( 3219): TILING 0xadc23000: First-transaction valid region < (x=0,
    y=75, w=480, h=2485); >
I/Gecko   ( 3219): TILING 0xadc23000: First-transaction invalid region < >
I/Gecko   ( 3219): TILING 0xadc23000: Low-precision invalid region < >
I/Gecko   ( 3219): TILING 0xadc23000: Paint finished

validRegionP =
scollOffsetP =
paintEndP=
'''

class PaintSession(dict):
  def __init__(self):
    self.layers = {}

  def getLayer(self, layer):
    if layer not in self.layers:
      self.layers[layer] = {}
      # High resolution
      self.layers[layer]['High'] = []
      # Low resolution
      self.layers[layer]['Low'] = []

    return self.layers[layer]

class TilingLogParser(object):
  def __init__(self):
    self.highResolution = True
    self.patterns = {}

    # Pattern for parsing region log.
    self.patterns['region'] =\
      re.compile(('.*\(x=(?P<x>[0-9]*), '
                  'y=(?P<y>[0-9]*), '
                  'w=(?P<w>[0-9]*), '
                  'h=(?P<h>[0-9]*)\);'))

    self.patterns['visibleRegion'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): ' # TILING log prefix.
                  'Initial visible region ' # Log category.
                  '<.*>'))

    self.patterns['paintFinished'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): ' # TILING log prefix.
                  'Paint finished'))

    self.patterns['lowPrecision'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Initial low-precision region '
                  '<.*>'))

    self.patterns['highResolution'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update with old valid region '
                  '<.*>'))
    self.patterns['lowResolution'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive paint: low-precision invalid region is '
                  '<.*>'))
    # Log patterns in ClientTiledLayerBuffer::ProgressiveUpdate
    self.patterns['puValid'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update valid region '
                  '<.*>'))
    self.patterns['puInvalid'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update invalid region '
                  '<.*>'))
    self.patterns['puOldValid'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update old valid region '
                  '<.*>'))
    self.patterns['puFinalValid'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update final valid region '
                  '<.*>'))
    self.patterns['puFinalInvalid'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update final invalid region '
                  '<.*>'))
    self.patterns['puPaintRegion'] =\
      re.compile(('.* TILING 0x(?P<layer>[^:]*): '
                  'Progressive update computed paint region '
                  '<.*> repeat (?P<repeat>[0-9]*)'))
    #  TILING_LOG("TILING %p: Progressive update computed paint region %s repeat
    #      %d\n", mPaintedLayer, Stringify(regionToPaint).c_str(), repeat);
    self.paints = []

  def parse(self, log):
    self.paints.append(PaintSession())
    with open(log, 'r') as fhandle:
      for line in fhandle:
        matched = re.match(self.patterns['paintFinished'], line)
        if matched:
          self.paints.append(PaintSession())

        session = self.paints[len(self.paints) - 1]
        self._resolution(session, line)
        self._progressiveUpdate(session, line)
    
    # Always pop up the first element. The first element is the one we get before
    # the 1st "Paint Finished" log.
    # The last one is usless as well.
    self.paints.pop(0)
    self.paints.pop()

  ''' Dump self.paints onto console.
  '''
  def dump(self):
    print "Total sessions: %s" % (len(self.paints),)
    for index, session in enumerate(self.paints):
      print "Session %s" % (index, )
      for key in session.layers:
        print "Layer ID = %s" % key
        print "Layer content = %s" % (session.layers[key], )

  def dumpPaintRegion(self):
    print "Total sessions: %s" % (len(self.paints),)
    for index, session in enumerate(self.paints):
      for key in session.layers:
        layer = session.layers[key];
        print "Frame #%s" % (index, )
        print "Layer ID = 0x%s" % key

        for prog in layer['High']:
          self._dumpProg(prog, 'High')
        for prog in layer['Low']:
          self._dumpProg(prog, 'Low')

  def _dumpProg(self, prog, resolution):
    if 'puValid' in prog.keys():
      print resolution + " - valid region = %s" % (prog['puValid'],)
    if 'puInvalid' in prog.keys():
      print resolution + " - invalid region = %s" % (prog['puInvalid'],)
    if 'puOldValid' in prog.keys():
      print resolution + " - old valid region = %s" % (prog['puOldValid'],)
    if 'puPaintRegion' in prog.keys():
      print resolution + " - progressive paint = %s" % (prog['puPaintRegion'],)
    if 'puFinalValid' in prog.keys():
      print resolution + " - final valid = %s" % (prog['puFinalValid'],)
    if 'puFinalInvalid' in prog.keys():
      print resolution + " - final invalid = %s" % (prog['puFinalInvalid'],)

  def _resolution(self, session, line):
    matched = re.match(self.patterns['highResolution'], line)
    if matched:
      print "HIGH RESOLUTION!!!!"
      self.highResolution = True
      return
    matched = re.match(self.patterns['lowResolution'], line)
    if matched:
      print "LOW RESOLUTION!!!!"
      self.highResolution = False
      return

  def _progressiveUpdate(self, session, line):
    resolution = ('High' if self.highResolution else 'Low')

    # puValid is the 1st log in ProgressiveUpaate.
    matched = re.match(self.patterns['puValid'], line)
    if matched:
      layer = matched.group('layer')
      print resolution + ' pu valid region - layer = ' + layer
      layer = session.getLayer(layer)
      layer[resolution].append({})
      prog = layer[resolution][len(layer[resolution]) - 1]
      self._parseRegion(prog, line, 'puValid')
      return

    if self._readPULog(session, line, 'puInvalid', resolution) == True:
      return
    if self._readPULog(session, line, 'puOldValid', resolution) == True:
      return
    if self._readPULog(session, line, 'puPaintRegion', resolution) == True:
      return
    if self._readPULog(session, line, 'puFinalValid', resolution) == True:
      return
    if self._readPULog(session, line, 'puFinalInvalid', resolution) == True:
      return

  def _readPULog(self, session, log, pattern, resolution):
    matched = re.match(self.patterns[pattern], log)
    if matched:
      layer = matched.group('layer')
      print "layer = " + layer + ' - ' + pattern
      layer = session.getLayer(layer)
      prog = layer[resolution][len(layer[resolution]) - 1]
      self._parseRegion(prog, log, pattern)
      return True

    return False

  def _parseRegion(self, prog, log, pattern):
    matched = re.match(self.patterns['region'], log)

    if matched:
      if pattern not in prog.keys():
        prog[pattern] = []

      prog[pattern].append((matched.group('x'),
                            matched.group('y'),
                            matched.group('w'),
                            matched.group('h')))

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
    print "Positional parameter 1: log file."
    raise SystemExit(1)

  parser = TilingLogParser()
  parser.parse(sys.argv[1])
  #parser.dump()
  parser.dumpPaintRegion()

