musurgia is a library of different (personal) tools for computer aided music composition.

**VERSIONS** 

v 1.0.1 
\__init\__.py added

v 1.1.0  
reading_direction (vertical) added to:  
permutation  
LimitedPermutation  
FractalTree  

v 1.1.1  
reading_direction (vertical) added to:  
Square()
pdf function deleted in Square() and Module() 

v 1.2.1 (1.2.0 was corrupt)  
FractalTree()
value can only be changed for the root without children
FractalMusic()
delete module_tempo, score_tempo
add tempo
quarter_duration only changes duration
children can have different tempi
tempo can only be set once
set_non_tempi()
FractalTree() and FractalMusic()
changes needed in merge, reduce, quantize, round
Square() and TimeLine()
minor changes needed

v 1.2.2  
Square()
write_infos() module duration decimal changed to 1

v 1.2.3  
FractalMusic().quarter_duration: bug fix

v 1.2.4  
FractalMusic().quarter_duration: bug fix

v 1.3.0
Module().change_duration(): deleted
Module().change_quarter_duration(): deleted
Square().change_module_duration(): attribute mode (module_duration or score_duration) deleted
Row().change_duration(): added
Row().change_quarter_duration(): added

v 1.4.0  
FractalMusic().quarter_duration: bug fix (float instead of fraction)
FractalMusic().find_best_tempo(): function added
FractalMusic().duration: bug fix (no type change to fraction)
FractalTree().round_leaves() : deleted
FractalMusic().round_leaves() : added

v 1.4.1  
FractalTree().\__deepcopy\__(): optimize
FractalMusic().\__deepcopy\__(): optimize

v 1.4.2
FractalTree().size: added

v 1.5.0
testcomparefiles: renamed to agtestunit
TestCompareFiles(): renames to AGTestCase
TestCompareFiles().assertTemplate(file_path=pdf_path): changed to: self.assertCompareFiles(actual_file_path=pdf_path)
file_path: renamed tp actual_path
template_path: renamed to expected_path
Tests:
if comparing files is needed use Test(AGTestCase)
_template.* renamed to _expected.*

v 1.5.1
setup.py: install_requires: added diff-pdf-visually == 1.4.1





