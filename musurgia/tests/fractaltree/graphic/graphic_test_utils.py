from musurgia.fractal import FractalTree


def create_test_fractal_tree():
    ft = FractalTree(value=10, proportions=(1, 2, 3, 4), main_permutation_order=(3, 1, 4, 2),
                     permutation_index=(1, 1))
    ft.add_layer()

    ft.add_layer(lambda node: node.get_fractal_order() > 1)
    ft.add_layer(lambda node: node.get_fractal_order() > 2)
    return ft


def add_infos(ft, gt):
    for index, (gn, fn) in enumerate(zip(gt.traverse(), ft.traverse())):
        if gn.get_distance() == 1:
            gn.get_segment().start_mark_line.add_text_label(f'value:{round(fn.get_value(), 2)}', font_size=10,
                                                            bottom_margin=1)
        gn.get_segment().start_mark_line.add_text_label(f'{fn.get_fractal_order()}', font_size=9,
                                                        bottom_margin=1)

        position_in_tree_label = gn.get_segment().start_mark_line.add_text_label(f'{fn.get_position_in_tree()}',
                                                                                 font_size=8, placement='below',
                                                                                 top_margin=1)
        if gn.get_distance() == 3:
            if fn.up.up.get_position_in_tree() == '4':
                if gn.up.get_children().index(gn) % 4 == 1:
                    position_in_tree_label.top_margin = 3
                elif gn.up.get_children().index(gn) % 4 == 2:
                    position_in_tree_label.top_margin = 5
                elif gn.up.get_children().index(gn) % 4 == 3:
                    position_in_tree_label.top_margin = 7
            else:
                if gn.up.get_children().index(gn) % 2 == 1:
                    position_in_tree_label.top_margin = 3
