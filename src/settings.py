
import sublime
import sublime_plugin

from .support import log

# settings

def get(key, default=None):
  log(f'settings.get:\n\tkey: {key}\n\tdefault: {default}')
  settings = sublime.load_settings('cmd_caller.sublime-settings')
  # No block for this platform (e.g. "osx"): fall back to the default.
  platform_settings = settings.get(sublime.platform()) or {}
  if key in platform_settings:
    log(f'\tget: {platform_settings[key]}')
    return platform_settings[key]
  log('\tget: default')
  return default


class CmdCallerEditSettingsCommand(sublime_plugin.WindowCommand):
  def run(self):
    log(self.__class__.__name__)
    base_file = '${packages}/cmd-caller/settings/cmd_caller.sublime-settings'
    default = f'{{\n\t"{sublime.platform()}": {{\n\t\t$0\n\t}}\n}}'
    self.window.run_command('edit_settings', {"base_file": base_file, "default": default})


class CmdCallerEditKeyBindingsCommand(sublime_plugin.WindowCommand):
  def run(self):
    log(self.__class__.__name__)
    platform = sublime.platform().capitalize()
    relpath = f'cmd-caller/keybinds/Default ({platform}).sublime-keymap'
    base_file = f'${{packages}}/{relpath}'
    default = sublime.load_resource(f'Packages/{relpath}')
    self.window.run_command('edit_settings', {"base_file": base_file, "default": default})
