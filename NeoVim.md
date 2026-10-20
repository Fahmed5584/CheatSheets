# NeoVim Cheat Sheet

## Mode Switching
| Key         | Action                                                  |
| ----------- | ------------------------------------------------------- |
| `Esc`       | Switch to `normal` mode                                 |
| `i`/`a`     | Switch to insert mode `before`/`after` cursor           |
| `I`/`A`     | Switch to insert mode at `start` / `end` of line        |
| `o`/`O`     | Switch to insert mode `below` / `above` current line    |
| `v`/`V`     | Switch to `visual` / `Visual Line` mode                 |
| `Ctrl`+`V`  | Switch to `visual block` mode                           |
| `\tm`       | Switch to `table mode`                                  |

## Navigation
| Key            | Action                                                                     |
|----------------+----------------------------------------------------------------------------|
| `w`/`W`        | Move to the next `word`/`WORD`                                             |
| `e`/`E`        | Move to the end of `word`/`WORD`                                           |
| `gg`/`G`       | Move cursor to `top`/`bottom` line                                         |
| `zt`/`zb`/`zz` | Scroll view to put the cursor at the `top`/`bottom`/`middle` of the screen |
| `#gg`          | Move cursor to exact line number where `#` is the line number to go to     |

## Tabs
| Key                | Action                                                                |
| ------------------ | --------------------------------------------------------------------- |
| `:tabnew` [file]   | Open a `new tab`, specify the filename of the file you wish to open   |
| `gt`/`gT`          | Go to the `Next` / `Previous` tab                                     |
| `#gt`              | Go to a specified number tab (e.g. 2gt)                               |
| `:tabs`            | `List` tabs                                                           |
| `:tabc`            | `Close` the current tab                                               |
| `:tabo`            | `Close All Other` tabs                                                |

## Operate between Delimiters.
Text objects allow you to operate on a portion of text between different types of delimiters (e.g `(` `<` `[` `{`).

The commands take the format : <operator> <i|a> <delimiter>

`i` = inside the delimiter
`a` = around (including) the delimiter

### Operators
| Operator | Meaning                                    |
|----------+--------------------------------------------|
| `c`      | change (delete, then enter Insert mode)    |
| `d`      | delete.                                    |
| `y`      | yank (copy)                                |
| `v`      | visually `highlight` (userful for preview) |
|----------+--------------------------------------------|

### Delimiters
|--------------------------+--------------------------------------------|
| Delimiter                | Notes                                      |
| `(` or `<` or `[` or `{` | Different types of `brackets`              |
| `"` or `'` or `/``       | `quotes` or `back tick`                    |
| `w` or `s` or `p` or `t` | `word` or `sentence` or `paragraph` or XML |
|--------------------------+--------------------------------------------|

### Examples
|---------+--------------------------------------------------------------------------------------|
| Command | Notes                                                                                |
|---------+--------------------------------------------------------------------------------------|
| ci{     | `changes` (delets + `insert` mode) text `inside` the `{` `}` brackets                |
| ca(     | `changes` (delete + `insert` mode) text `around`(including) the `(` and `)` brackets |
| di<     | `deletes` text `inside` the `<` `>` brackets                                         |
| yi{     | `yank` (copy) `inside` the `{` `}`                                                   |
|---------+--------------------------------------------------------------------------------------|

