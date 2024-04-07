## Running

`python3 main.py`

## Testing

`python3 -m unittest discover tests`

## Structure

- `main.py`: The main entry point.
- `src/`: Source code directory.
  - `app.py`: Defines the main window and tab view, into which the three visible tabs are packed.
  - `utils.py`: Loading and saving data, configuration.
  - `frames/`:
    - `pomodoro_frame.py`: Entire timer functionality + storing data + communicating with Rich Presence.
    - `settings_frame.py`: Updates config.
    - `stats_frame.py`: Displays stats and graphs.
  - `reusable/`: Reusable UI components.
  - `logic/`: Logic separate from customtkinter.
    - `richpresence.py`: The Discord Rich Presence integration - editable, but if you change function args go to pomodoro_frame.py update_rpc.
    - `graphs.py`: matplotlib plots using data collected.
  - `assets/`
    - `sounds/`: Beep.
    - `themes/`: Responsible for all colors in the GUI. Theme is loaded on launch in run.py.
- `tests/`: Basic tests. Ignore ResourceWarnings.

## File Dependencies

- `main.py` imports and uses `src/app.py`.
- `src/app.py` imports and uses `src/frames/*` and `src/utils.py`.
- `src/frames/pomodoro_frame.py` imports and uses `src/utils.py` and `src/logic/richpresence.py`.
- `src/frames/settings_frame.py` imports and uses `src/components/entry_frame.py` and `src/utils.py`.
- `src/frames/stats_frame.py` imports and uses `src/components/statistic_display.py`, `src/utils.py`, and `src/logic/graphs.py`.

