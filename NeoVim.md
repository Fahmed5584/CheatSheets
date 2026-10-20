# NeoVim Cheat Sheet

## Mode Switching
| Key          | Action                                                  |
| -----------  | ------------------------------------------------------- |
| `Esc`        | Switch to `normal` mode                                 |
| `i`/`a`      | Switch to insert mode `before`/`after` cursor           |
| `I`/`A`      | Switch to insert mode at `start` / `end` of line        |
| `o`/`O`      | Switch to insert mode `below` / `above` current line    |
| `v`/`V`      | Switch to `visual` / `Visual Line` mode                 |
| `Ctrl`+`V`   | Switch to `visual block` mode                           |
| `<leader>tm` | Switch to `table mode` (my leader key = space)          |

## Navigation
| Key            | Action                                                                     |
|----------------|----------------------------------------------------------------------------|
| `w`/`W`        | Move to the next `word`/`WORD`                                             |
| `e`/`E`        | Move to the end of `word`/`WORD`                                           |
| `gg`/`G`       | Move cursor to `top`/`bottom` line                                         |
| `zt`/`zb`/`zz` | Scroll view to put the cursor at the `top`/`bottom`/`middle` of the screen |
| `Ctrl`+`d`/`u` | Scroll half a page `down`/`up`                                             |
| `{n}gg`        | Move cursor to line number `{n}` (e.g. `42gg`)                             |

## Tabs
| Key                | Action                                                                |
| ------------------ | --------------------------------------------------------------------- |
| `:tabnew` [file]   | Open a `new tab`, specify the filename of the file you wish to open   |
| `gt`/`gT`          | Go to the `Next` / `Previous` tab                                     |
| `{n}gt`            | Go to a specified number tab (e.g. `2gt`)                             |
| `:tabs`            | `List` tabs                                                           |
| `:tabc`            | `Close` the current tab                                               |
| `:tabo`            | `Close All Other` tabs                                                |

## Buffers
Every file you open stays loaded as a buffer, even when it isn't on screen.

| Key         | Action                                         |
|-------------|------------------------------------------------|
| `:ls`       | `List` open buffers                            |
| `:bn`/`:bp` | Go to the `next`/`previous` buffer             |
| `:b{n}`     | Go to a buffer by number (e.g. `:b3`)          |
| `Ctrl`+`^`  | Toggle between the `current` and `last` buffer |
| `:bd`       | `Close` (delete) the current buffer            |

## Operate between Delimiters
Text objects allow you to operate on a portion of text between different types of delimiters (e.g. `(` `<` `[` `{`).

The commands take the format: `<operator> <i|a> <delimiter>`

`i` = inside the delimiter

`a` = around (including) the delimiter

### Operators
| Operator | Meaning                                   |
|----------|-------------------------------------------|
| `c`      | change (delete, then enter Insert mode)   |
| `d`      | delete                                    |
| `y`      | yank (copy)                               |
| `v`      | visually `highlight` (useful for preview) |

### Delimiters
| Delimiter                | Notes                                      |
|--------------------------|--------------------------------------------|
| `(` or `<` or `[` or `{` | Different types of `brackets`              |
| `"` or `'` or `` ` ``    | `quotes` or `back tick`                    |
| `w` or `s` or `p` or `t` | `word` or `sentence` or `paragraph` or tag |

### Examples
| Command | Notes                                                                                  |
|---------|----------------------------------------------------------------------------------------|
| `ci{`   | `changes` (deletes + `insert` mode) text `inside` the `{` `}` brackets                 |
| `ca(`   | `changes` (deletes + `insert` mode) text `around` (including) the `(` and `)` brackets |
| `di<`   | `deletes` text `inside` the `<` `>` brackets                                           |
| `yi{`   | `yank` (copy) `inside` the `{` `}`                                                     |

## Counts
A number before a command repeats it.

| Key       | Action                         |
|-----------|--------------------------------|
| `5j`/`5k` | Move `down`/`up` 5 lines       |
| `3w`      | Move forward 3 words           |
| `3dd`     | Delete 3 lines                 |
| `2yy`     | Yank (copy) 2 lines            |
| `d3w`     | Delete the next 3 words        |
| `4.`      | Repeat the last change 4 times |

## Search and Replace
| Key             | Action                                       |
|-----------------|----------------------------------------------|
| `/text`         | Search `forward` for `text`                  |
| `n`/`N`         | Go to the `next`/`previous` match            |
| `*`             | Search for the word under the cursor         |
| `:%s/old/new/g` | Replace every `old` with `new` in the file   |
| `:noh`          | Clear search highlighting                    |

## My Custom Mappings
Mappings set in `~/.config/nvim/init.lua` (leader key = `Space`).

| Key          | Mode   | My Mapping                   | Stock Neovim                         |
|--------------|--------|------------------------------|--------------------------------------|
| `jj`         | Insert | `Esc` (back to normal mode)  | `Esc` or `Ctrl`+`[`                  |
| `<leader>ff` | Normal | fzf: find files              | `:find **/{name}` or `:e {path}`     |
| `<leader>fg` | Normal | fzf: search text in files    | `:vimgrep /text/ **` then `:copen`   |
| `<leader>fb` | Normal | fzf: open buffers            | `:ls` then `:b{n}`                   |
| `<leader>fr` | Normal | fzf: recent files            | `:browse oldfiles`                   |
| `<leader>tm` | Normal | Toggle table mode (plugin)   | N/A                                  |
| `gd`         | Normal | LSP: go to definition        | `Ctrl`+`]` (when an LSP is attached) |
| `gD`         | Normal | LSP: go to declaration       | N/A                                  |
| `<leader>e`  | Normal | LSP: show error under cursor | `Ctrl`+`w` then `d`                  |
| `:Game`      | Cmd    | Play Vim-Be-Good             | N/A                                  |

`gd`, `gD` and `<leader>e` only apply in buffers with an LSP attached. The stock fzf alternatives have no fuzzy matching.
