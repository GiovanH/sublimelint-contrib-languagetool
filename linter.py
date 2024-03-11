from SublimeLinter.lint import Linter  # type: ignore[import]
import sublime  # type: ignore[import]
import json
import traceback

# from typing import *

from urllib.parse import urlencode
from urllib.request import urlopen

def getResponse(server, text, language, ignored_ids):
    try:
        payload = {
            'language': language,
            'text': text.encode('utf8'),
            'User-Agent': 'sublime',
            'disabledRules': ','.join(ignored_ids)
        }
    except Exception:
        print(repr(ignored_ids))
        raise
    # print(payload)
    content = _post(server, payload)
    if content:
        j = json.loads(content.decode('utf-8'))
        return j['matches']
    else:
        return None

# internal functions:


def _post(server, payload):
    data = urlencode(payload).encode('utf8')
    # try:
    content = urlopen(server, data).read()
    return content
    # except IOError:
    #     return None


# def load_ignored_rules():
#     ignored_rules_file = 'LanguageToolUser.sublime-settings'
#     settings = sublime.load_settings(ignored_rules_file)
#     return settings.get('ignored', [])


class LanguageTool(Linter):
    linefmt = "{line}\t{code}\t{col}\t{error_type}\t{end_col}\t{message}"
    regex = linefmt.format(
        line=r"(?P<line>.+?)",
        code=r"(?P<code>.+?)",
        # near=r"(?P<near>.+?)",
        col=r"(?P<col>.+?)",
        end_col=r"(?P<end_col>.+?)",
        message=r"(?P<message>.+?)",
        error_type=r"(?P<error_type>.+?)"
    ) + r"$"

    multiline = False
    defaults = {
        'selector': 'meta.paragraph',
        'ignored_ids': [],
        'debug': False
    }

    line_col_base = (0, 0)

    cmd = None

    def run(self, cmd, code):
        server_url = self.settings.get('server_url', "http://localhost:8081/v2/check")
        language = "en-US"
        ignored_ids = self.settings.get("ignored_ids", [])  # [rule['id'] for rule in load_ignored_rules()]
        matches = getResponse(
            server_url,
            code,
            language,
            ignored_ids
        )
        for m in matches:
            m['lines'] = [("%s\n" % line) for line in code.split('\n')]
            m['computed_line'] = code[:m['offset']].count('\n')
            m['rel_offset'] = m['offset'] - sum(len(line) for line in m['lines'][:m['computed_line']])
            m['replacements_fmt'] = [r['value'] for r in m.get('replacements', [])]

        if self.settings.get('debug'):
            print(server_url, language, ignored_ids, matches)

        return '\n'.join([
            self.linefmt.format(
                line=match['computed_line'],  # match['context']['offset'],
                col=match['rel_offset'],
                end_col=match['rel_offset'] + match['length'],
                error_type="warning",
                message=("%s %s" % (match['message'], match['replacements_fmt'])),
                code=match['rule']['id']  #  + '|' + match['type']['typeName'],
                # near=match['sentence'].strip().split('\n')[0]
            )
            for match in matches
        ])
