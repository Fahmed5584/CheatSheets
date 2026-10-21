# tmux
`Ctrl+B` is the prefix used before every binding.

## Commands
| Command                  | Notes                                                        |
|--------------------------|--------------------------------------------------------------|
| `tmux new -s name`       | New named session                                            |
| `tmux a -t name/num`     | Attach to session by name or number                          |
| `tmux ls`                | List tmux sessions                                           |
| `tmux splitw -fv`        | Split a new pane across the `full width` at the bottom       |
| `tmux splitw -fh`        | Split a new pane across the `full height` on the right       |

The `splitw` commands can also be typed at the tmux command prompt (`:`) without the `tmux` part (e.g. `:splitw -fv`). Add `-l 30%` to set the new pane's size.

## Help
| Key | Notes                                |
|-----|--------------------------------------|
| `?` | `List` all key bindings (searchable) |
| `:` | Open the tmux `command prompt`       |

## Copy / Paste
`[` to enter copy mode then navigate to start of selection with arrow keys / PgUp/PgDn (you can search in this mode with `Ctrl+S`)

`Ctrl+Space` to start selection, move to extend

`Alt+W` to copy and leave copy mode.

`]` to paste (tmux's own paste buffer)

`Ctrl+Shift+V` to paste (terminal paste from the system clipboard)

### More Copy Mode Keys
Used inside copy mode, without the prefix (except `PgUp`).

| Key                  | Notes                                       |
|----------------------|---------------------------------------------|
| `PgUp` (with prefix) | `Enter` copy mode and scroll up in one step |
| `Ctrl+R`             | Search `upwards`                            |
| `n` / `N`            | `Next` / `previous` search match            |
| `Alt+<` / `Alt+>`    | Jump to the `top` / `bottom` of the history |
| `g`                  | `Go` to a line number                       |
| `q` or `Esc`         | `Exit` copy mode without copying            |

## Sessions
| Key | Notes                 |
|-----|-----------------------|
| `d` | `Detach` from session |
| `s` | `Session picker`      |
| `$` | `Rename` session      |

## Panes
| Key           | Notes                                                    |
|---------------|----------------------------------------------------------|
| `%`           | `Split` left / right                                     |
| `"`           | `Split` top / bottom                                     |
| `←↓↑→`        | `Navigate` between panes                                 |
| `Ctrl`+`←↓↑→` | `Resize` current pane (small increments)                 |
| `Alt`+`←↓↑→`  | `Resize` current pane (large increments)                 |
| `x`           | `Close` pane                                             |
| `Space`       | `Cycle` different layouts                                |
| `z`           | `Zoom` cycle (toggle current pane to full window / back) |
| `{` / `}`     | `Swap` panes around                                      |

## Windows
| Key             | Notes                                                       |
|-----------------|-------------------------------------------------------------|
| `c`             | `Create` new window                                         |
| `n`/`p`         | Go to `next` or `previous` window                           |
| `0`–`9`         | Go to window by `number`                                    |
| `w`             | Open a tree `picker` of sessions and windows to choose from |
| `,` (comma)     | `Rename` the current window                                 |
| `&`             | `Close` the current window                                  |
| `.` (full-stop) | `Move` the window to a new index                            |
