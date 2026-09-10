# IRCTC Playwright Structured Automation

Refactored from the supplied single-file Patchright automation into a page-object structure.

## Run

1. Install dependencies:
   `pip install -r requirements.txt`

2. Install/use Patchright's supported browser setup as required by your environment.

3. Edit:
   - `config/config.json`
   - `config/credentials.json`
   - `config/passengers.json`

4. Run:
   `python main.py`

## Structure

- `main.py` - orchestration only
- `config/` - runtime configuration and credentials
- `pages/` - page-object classes
- `utils/` - configuration loading, validation, and station helper

## Notes

The existing flow, selectors, retry behavior, availability polling, confirmation handling,
passenger entry, review validation, and payment selection are retained as closely as
possible from the supplied script.

The original script imports `extract_station_name` from an existing `utils` module.
A small compatibility implementation is included in `utils/station_utils.py`; replace it
with your existing implementation if that helper has more specific parsing behavior.
