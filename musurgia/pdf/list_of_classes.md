drawobject.py

* DrawObject(ABC, Positioned, Margined)
* ClippingArea

font.py

* Font

labeled.py
x
* Labeled(PositionMaster)

line.py

* StraightLine(Slave, DrawObject, Labeled)
* MarkLine(StraightLine)
* LineSegment(Master, DrawObject)
* HorizontalLineSegment(LineSegment)
* VerticalLineSegment(LineSegment)
* AbstractSegmentedLine(DrawObjectContainer)
* HorizontalSegmentedLine(AbstractSegmentedLine, DrawObjectRow)
* VerticalSegmentedLine(AbstractSegmentedLine, DrawObjectColumn)
* AbstractRuler(AbstractSegmentedLine)
* HorizontalRuler(AbstractRuler, HorizontalSegmentedLine)
* VerticalRuler(AbstractRuler, VerticalSegmentedLine)

margined.py

* Margined

markline.py

* MarkLine(DrawObject, Labeled)

masterslave.py

* _GetSlavePositionMixIn(ABC)
* _GetSlaveMarginMixIn(ABC)
* _SetSlavePositionMixIn
* _SetSlaveMarginMixIn
* _Named
* PositionMaster(_GetSlavePositionMixIn):
* MarginMaster(_GetSlaveMarginMixIn):
* Master(_GetSlavePositionMixIn, _GetSlaveMarginMixIn):
* PositionSlave(_Named, _SetSlavePositionMixIn):
* MarginSlave(_Named, _SetSlaveMarginMixIn):
* Slave(_Named, _SetSlavePositionMixIn, _SetSlaveMarginMixIn):

named.py

* Named
* NameLabel(TextLabel)

pdf.py

* SavedState
* PrepareDrawObject
* Pdf(FPDF)

pdfunit.py

* PdfUnit

positioned.py

* Positioned

rowcolumn.py

* DrawObjectContainer
* DrawObjectRow(DrawObjectContainer)
* DrawObjectColumn(DrawObjectContainer)

scene.py

* Scene(DrawObject)

segmentedline.py

* MarkLine(DrawObject, Labeled)
* LineSegment(DrawObject, Labeled, Named)
* SegmentedLine(DrawObject, Labeled, Named)

table.py

* Cell(DrawObject)
* Table(DrawObject)

text.py

* Text(DrawObject)
* TextLabel(PositionSlave, Text)
* PageText(Text)