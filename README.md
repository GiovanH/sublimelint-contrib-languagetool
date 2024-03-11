# SublimeLinter-contrib-languagetool

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [languagetool](https://languagetool.org/dev). By default, it applies to text with the `meta.paragraph` selector, i.e. markdown text.

## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

You must provide an API url for the languagetool server, or run your own instance. See <https://languagetool.org/dev> for details.

## Settings

- SublimeLinter settings: <http://sublimelinter.readthedocs.org/en/latest/settings.html>
- Linter settings: <http://sublimelinter.readthedocs.org/en/latest/linter_settings.html>

Additional SublimeLinter-languagetool settings:

|Setting    |Description    |
|:----------|:--------------|
|server_url |API url for the languagetool server, e.g. `"http://localhost:8081/v2/check"`|
|debug      |Print extended debugging information    |
|ignored_ids|`disabledRules`, passed to LanguageTool.|
