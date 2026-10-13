
import os

import sublime
import sublime_plugin

# support

# log

# Log files in Sublime Text's cache folder, set by plugin_loaded().
logfile = None
lastlogfile = None


def plugin_loaded():
  global logfile, lastlogfile
  folder = os.path.join(sublime.cache_path(), 'cmd-caller')
  os.makedirs(folder, exist_ok=True)
  logfile = os.path.join(folder, 'logs.txt')
  lastlogfile = os.path.join(folder, 'logs.last.txt')
  if os.path.exists(lastlogfile):
    os.remove(lastlogfile)
  if os.path.exists(logfile):
    os.rename(logfile, lastlogfile)


def log(message):
  if logfile is None:
    return
  with open(logfile, 'ab') as f:
    f.write(f'{message}\n'.encode('utf-8'))

# load text content to a new sheet
class LoadText(sublime_plugin.TextCommand):

  # load text file
  def load_text(self, edit, title, filename, syntax=None):
    log(f'{self.__class__.__name__}#load_text')
    f = self.view.window().new_file()
    f.set_name(title)
    f.settings().set('gutter', False)
    try:
      if os.path.isabs(filename):
        with open(filename, 'rb') as file:
          content = file.read().decode('utf-8')
      else:
        content = sublime.load_resource(f'Packages/cmd-caller/{filename}')
    except OSError:
      content = '\n\n\n--- No Content Available ---\n\n\n'
    f.insert(edit, 0, content)
    if syntax:
      f.set_syntax_file(syntax)
    f.set_read_only(True)
    f.set_scratch(True)


class LoadPluginFile(LoadText):

  # load logs
  def load_logs(self, edit, file):
    log(f'{self.__class__.__name__}#load_logs')
    super().load_text(edit, 'Cmd Caller - Logs', file)


# load current logs
class CmdCallerLoadLogsCommand(LoadPluginFile):
  def run(self, edit):
    log(self.__class__.__name__)
    super().load_logs(edit, logfile)


# load last logs
class CmdCallerLoadLastLogsCommand(LoadPluginFile):
  def run(self, edit):
    log(self.__class__.__name__)
    super().load_logs(edit, lastlogfile)
