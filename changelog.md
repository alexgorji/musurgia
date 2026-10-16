# Unreleased

- Relative musical trees expose their specific chord factory types through
  `get_chord_factory()`. Replacement factories must inherit from the tree's
  `DEFAULT_TREE_CHORD_FACTORY`; incompatible replacements raise `TypeError`.
- Fractal relative chord factories expose a `FractalDirectionIterator`.
  Assigning another iterator type raises `TypeError`; assigning `None` resets
  the iterator to inherited/default directions when next accessed.