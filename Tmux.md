# TMUX
`Ctrl+B` is the prefix used before every binding.

## Commands
|Command                |Notes                                  |
|-----------------------|---------------------------------------|
|tmux new -s `name`     |New named session                      |
|tmux a -t `name/num`   |Attach to session by name or number    |
|tmux ls                |List tmux sessions                     |

## Copy / Paste
`[` to enter copy mode then navigate to start of selection with arrow keys / PgUp/PgDn (you can search in this mode with `Ctrl+S`

`Ctrl+Space` to start selection, move to extend

`Alt+W` to copy and leave copy mode.

`Ctrl+Shift+V` to paste

## Sessions

|-----|-----------------------|
| Key | Notes                 |
|-----|-----------------------|
| `d` | `Detach` from session |
| `s` | `Session picker`      |
| `$` | `Rename` session      |
|-----|-----------------------|

## Panes

|---------------|---------------------------------------------------------|
| Key           | Notes                                                   |
|---------------|---------------------------------------------------------|
| `%`           | `split` left / right                                    |
| `"`           | `split` top / bottom                                    |
| `←↓↑→`        | `navigate` between panes                                |
| `Ctrl`+`←↓↑→` | `resize` current pane (small increments)                |
| `Alt`+`←↓↑→`  | `resize` current pane (large increments)                |
| `x`           | `Close` pane                                            |
| `space`       | `cycle` different layouts                               |
| `z`           | `Zoom` cycle (toggle current pane to full window / back |
| `{` / `}`     | `Swap` panes around                                     |
|---------------|---------------------------------------------------------|

## Windows

|----------------|------------------------------------------------------------|
| Key            | Notes                                                      |
|----------------|------------------------------------------------------------|
| `c`            | `Create` new window                                        |
| `n`/`p`        | Go to `next` or `previous` window                          |
| `0 to 9`       | Go to window by `number`                                   |
| `w`            | Open a tree `picker` of sessions and windows to chose from |
| `,`(comma)     | `Rename` the current window                                |
| `&`            | `Close` the current window                                 |
| `.`(full-stop) | Move the window the a new index                            |
|----------------|------------------------------------------------------------|
