musurgia is a library of different (personal) tools for computer aided music composition.

python 3.7

**DEPENDENCIES:**  
quicktions == 1.9
musicscore == 1.0.1
prettytable == 0.7.2
fpdf2 == 2.0.3
diff-pdf-visually == 1.4.1
 
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

v 1.6.0  
Tree().get_leaves(): modified to return \[self\] if no children exist  
FractalTree().generate_children(): added

v 1.6.1  
FractalTree()._reduce(): bug fix (/ instead of Fraction)

v 1.7.0
FractalTree().change_value()
FractalMusic().quarter_duration: modified to Fraction
FractalMusic().change_quarter_duration(): added
FractalMusic().quantize_children(): added
FractalMusic().quantize_leaves(): optimised
FractalMusic().round_leaves(): optimised
FractalMusic().get_root_score(): deleted
FractalMusic().get_children_score(): added

v 1.7.1  
FractalTree().val: Fraction
FractalTree().change_value(): bug fix (children duration)
FractalMusic().get_children_score(): bug fix: gets score of each child with max layers of all children 

v 1.8.0  
setup.py install_requires: musicscore 1.0.1
FractalMusic().get_score_template(): subtitle changed to have one decimal place for seconds
FractalMusic().find_best_tempo(): renamed to: find_best_tempo_in_range()
FractalMusic().find_best_tempi_in_list(): added
FractalTree().generate_children(): added argument mode in ['reduce','merge'] and argument merge_index

v 1.8.1
Module().write_square_infos(): renamed to  write_info
Square().write_infos(): renamed to write_info 







