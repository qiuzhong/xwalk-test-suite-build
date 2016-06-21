#!/usr/bin/env python3
import os
import sys
import json
import subprocess


class CordovaBuilder:

    def __init__(self, cts_dir, xwalk_branch, xwalk_version, mode, arch,
                commandline_only = False, putonotcqa = False):
        self.cts_dir = cts_dir
        self.xwalk_branch = xwalk_branch
        self.xwalk_version = xwalk_version
        self.mode = mode
        self.arch = arch
        self.jiajia_dir = None
        self.otcqa_dir = None
        self.commandline_only = commandline_only
        self.putonotcqa = putonotcqa


    def set_dest_dir(self):
        config_json = None
        try:
            with open('config.json') as f:
                config_json = json.load(f)
        except Exception:
            sys.stderr.write('Failed to read or load config.json!\n')
            return

        self.jiajia_dir = os.path.join(config_json.get('jiajia_dir_prefix'),
                                        self.xwalk_branch,
                                        self.xwalk_version,
                                        'cordova4.x-{mode}'.format(
                                                    mode = self.mode),
                                        self.arch)
        self.otcqa_dir = os.path.join(config_json.get('otcqa_dir_prefix'),
                                        self.xwalk_branch,
                                        self.xwalk_version,
                                        'cordova-{mode}'.format(
                                                    mode = self.mode),
                                        self.arch)


    def recovery_cordova_plugin_xwalk_webview(self):
        '''Recovery the xwalk.gradle in cordova plugin crosswalk webview'''
        cordova_plugin_xwalk_webivew_dir = os.path.join(self.cts_dir,
                                        'tools',
                                        'cordova_plugins',
                                        'cordova-plugin-crosswalk-webview')
        if self.commandline_only:
            print('cd {d}'.format(d = cordova_plugin_xwalk_webivew_dir))
        os.chdir(cordova_plugin_xwalk_webivew_dir)
        xwalk_gradle = 'platforms/android/xwalk.gradle'
        cmd = 'git checkout -- ' \
              '{xwalk_gradle}'.format(xwalk_gradle = xwalk_gradle)
        if self.commandline_only:
            print(cmd)
        else:
            os.system(cmd)


    def update_cordova_plugin_xwalk_webview(self, cca_build = False):

        xwalk_gradle = os.path.join(self.cts_dir,
                                    'tools',
                                    'cordova_plugins',
                                    'cordova-plugin-crosswalk-webview',
                                    'platforms',
                                    'android',
                                    'xwalk.gradle')
        if not os.path.exists(xwalk_gradle):
            sys.stderr.write('xwalk_gradle does not exists!\n')
            return False

        start_line = None
        end_line = None
        if self.xwalk_branch == 'canary' or self.xwalk_branch == 'master':
            # modify xwalk.gradle
            cmd = '/bin/sed -n ' + r'"/maven {/ ="' + \
                  ' {xwalk_gradle}'.format(xwalk_gradle = xwalk_gradle)
            p = subprocess.Popen(cmd,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.STDOUT,
                                shell = True)
            (output, _) = p.communicate()

            try:
                start_line = int(output.strip())
                end_line = start_line + 2
            except Exception:
                sys.stderr.write('Not found a line with the same string like ' \
                                '"maven {\n\turl xwalkMavenRepo\n}"\n')
                return False

            delete_cmd = 'sed -i "{start_line},{end_line} d" ' \
                         '{xwalk_gradle}'.format(
                            start_line = start_line,
                            end_line = end_line,
                            xwalk_gradle = xwalk_gradle)
            replace_cmd = 'sed -i "{start_line} i\      mavenLocal()" ' \
                          '{xwalk_gradle}'.format(
                            start_line = start_line,
                            xwalk_gradle = xwalk_gradle)
            if self.commandline_only:
                print(delete_cmd)
                print(replace_cmd)
            else:
                if os.system(delete_cmd) != 0 or os.system(replace_cmd) != 0:
                    sys.stderr.write('Failed to modify xwalk.gradle.')
                    return False

            if cca_build:
                update_cca_version_cmd = '/bin/sed -i ' \
                                         '"s|ext.xwalkVersion = ' \
                                         'getConfigPreference' \
                                         '(\\"xwalkVersion\\")' \
                                         '|ext.xwalkVersion = ' \
                                         '\\"{xwalk_version}\\"|g" ' \
                                         '{xwalk_gradle}'.format(
                                        xwalk_version = self.xwalk_version,
                                        xwalk_gradle = xwalk_gradle)
                if self.commandline_only:
                    print(update_cca_version_cmd)
                else:
                    os.system(update_cca_version_cmd)

        if self.xwalk_branch == 'beta':
            if cca_build:
                if self.mode == 'embedded':
                    mode = 'core'
                else:
                    mode = 'shared'
                update_cca_version_cmd = '/bin/sed -i ' \
                                         '"s|ext.xwalkVersion = ' \
                                         'getConfigPreference' \
                                         '(\\"xwalkVersion\\")' \
                                         '|ext.xwalkVersion = ' \
                                         '\\"org.xwalk:' \
                                         'xwalk_{mode}_library_beta:' \
                                         '{xwalk_version}\\"|g" ' \
                                         '{xwalk_gradle}'.format(
                                        xwalk_version = self.xwalk_version,
                                        mode = mode,
                                        xwalk_gradle = xwalk_gradle)
                if self.commandline_only:
                    print(update_cca_version_cmd)
                else:
                    os.system(update_cca_version_cmd)
        return True


    def check_cordova(self, name, build_type = 'apps'):
        '''Check if the cordova '''
        pass


    def build_cordova(self, name, build_type = 'apps'):
        if build_type == 'apps':
            build_cmd = 'cd {cts_dir}/tools/build;' \
                        './pack_cordova_sample.py ' \
                        '-n {app_name} ' \
                        '-a {arch} ' \
                        '-m {mode} '.format(
                        cts_dir = self.cts_dir,
                        app_name = name,
                        arch = self.arch,
                        mode = self.mode
                        )
            with open('cordova_app.json') as f:
                cordova_app_config = json.load(f)
            if name in cordova_app_config.get('special_app'):
                build_cmd += '-p {passwd}'.format(
                            passwd = cordova_app_config.get('host_password'))
            if self.commandline_only:
                print(build_cmd)
            else:
                os.system(build_cmd)

            mv_cmd = 'mv -fv {apk} {dest_dir}'.format(
                            apk = os.path.join(self.cts_dir,
                                                'tools', 'build',
                                                '{app_name}.apk'.format(
                                                app_name = name
                                                )),
                            dest_dir = self.jiajia_dir
            )
            if self.commandline_only:
                print(mv_cmd)
            else:
                os.system(mv_cmd)

            put_on_otcqa_cmd = 'cp -fv {jiajia_path} {otcqa_path}'.format(
                jiajia_path = os.path.join(self.jiajia_dir,
                                        '{app_name}.apk'.format(
                                        app_name = name)),
                otcqa_path = os.path.join(self.otcqa_dir,
                                        '{app_name}.apk'.format(
                                        app_name = name))
            )
            if self.putonotcqa:
                if self.commandline_only:
                    print(put_on_otcqa_cmd)
                else:
                    if not os.path.exists(self.otcqa_dir):
                        os.system('mkdir -pv {otcqa_dir}'.format(
                                    otcqa_dir = self.otcqa_dir))
                    os.system(put_on_otcqa_cmd)
        elif build_type == 'tc':
            build_cmd = 'cd {cts_dir}/{tc_name};' \
                        '../../tools/build/pack.py -t cordova ' \
                        '-a {arch} ' \
                        '-m {mode} ' \
                        '-d {dest_dir}'.format(
                        cts_dir = self.cts_dir,
                        tc_name = name,
                        arch = self.arch,
                        mode = self.mode,
                        dest_dir = self.jiajia_dir)
            if self.commandline_only:
                print(build_cmd)
            else:
                os.system(build_cmd)

            put_on_otcqa_cmd = 'cp -fv {jiajia_path} {otcqa_path}'.format(
                jiajia_path = os.path.join(self.jiajia_dir,
                                '{tc_name}-{version}-1.cordova.zip'.format(
                                    tc_name = name.split('/')[-1],
                                    version = self.xwalk_version
                                )),
                otcqa_path = os.path.join(self.otcqa_dir,
                                '{tc_name}-{version}-1.cordova.zip'.format(
                                    tc_name = name.split('/')[-1],
                                    version = self.xwalk_version
                                ))
            )
            if self.putonotcqa:
                if self.commandline_only:
                    print(put_on_otcqa_cmd)
                else:
                    if not os.path.exists(self.otcqa_dir):
                        os.system('mkdir -pv {otcqa_dir}'.format(
                                    otcqa_dir = self.otcqa_dir))
                    os.system(put_on_otcqa_cmd)
        else:
            sys.stderr.write('Unsupported cordova building type, ' \
                            'exit with 1\n')
            sys.exit(1)


# if __name__ == '__main__':
#     cts_dir = '/home/orange/00_jiajia/work_space/release/crosswalk-test-suite'
#     xwalk_branch = None
#     xwalk_version = None
#     mode = 'embedded'
#     arch = 'x86'
#
#     version_json = None
#     with open(os.path.join(cts_dir, 'VERSION')) as f:
#         version_json = json.load(f)
#
#     xwalk_branch = version_json.get('crosswalk-branch')
#     xwalk_version = version_json.get('main-version')
#
#     helloworld = CordovaBuilder(cts_dir,
#                                 xwalk_branch,
#                                 xwalk_version,
#                                 mode,
#                                 arch)
#     helloworld.recovery_cordova_plugin_xwalk_webview()
#     helloworld.update_cordova_plugin_xwalk_webview()
#     helloworld.build_cordova('spacedodge', 'apps')
