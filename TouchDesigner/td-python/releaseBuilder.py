'''
Package TOX for Release Class
Authors | matthew ragan
matthewragan.com
'''

import webbrowser
import json

popupMsg = '''Your file is saved as | {name}
Save Location | {location}'''


class PackageTOX:
    '''
    This class is designed to operate as a general helper extension. 

    When sharing a TOX it's often difficult to ensure that it's correctly 
    packaged in a uniform and consistent manner that will ensure it's immediately usable by a 
    third party. This TOX aims to simplify some of that process by automating the prep and 
    packaging of a TOX in a consistent and reliable manner.
    ---------------

    '''

    def __init__(self, ownerOp):
        ''' 
        '''
        self.OwnerOp = ownerOp
        self.Release_target_op = ownerOp.par.Targetoperator
        self.Release_version = ownerOp.par.Releaseversion
        self.Reset_color = (0.545, 0.545, 0.545)
        self.Format_ready_save_loc = '{loc}/{name}.tox'
        self.Save_dir = ownerOp.par.Savelocation
        self.Tox_Name = ownerOp.par.Toxname
        self.Destroy_tags = ownerOp.par.Destroytags
        self.Ext_file_tags = ownerOp.par.Externalfiletags

        self.saveBuffer = ownerOp.op("base_saveBuffer")

        self.GithubLink = "https://github.com/raganmd/touchdesigner-tox-prep-for-release"
        print("PackageTOX Initialized")
        return

    def copyToSaveBuffer(self, targetOp):
        quiteCopy = self.saveBuffer.copy(targetOp)
        return quiteCopy

    def Package(self):
        msg = "Packing TOX"
        self._log_release_event(msg=msg)
        location = self.Save_tox()
        msg = popupMsg.format(location=location, name=self.Tox_Name)

        # if running just a build, force quit
        if self.OwnerOp.par.Quitafterpackaging:
            run(self._force_quit, delayFrames=10)

        op('base_popup/container_popup/text_body').text = msg
        op('base_popup/window1').par.winopen.pulse()

    def Save_tox(self):
        # format the save location for the tox
        save_loc = self.Format_ready_save_loc.format(
            loc=self.Save_dir, name=self.Tox_Name)
        target_op = self.copyToSaveBuffer(self.Release_target_op.eval())

        # set version
        target_op.par.Version = self.Release_version
        target_op.par.Version.readOnly = True

        # clean-up external files - disable loading, remove paths
        ext_file_tags = self.Ext_file_tags.val.split(',')
        ops_to_prep = [each_op for each_op in target_op.findChildren(
            type=DAT) if each_op.par['file'] != '']
        self.Disable_external_file(ops_to_prep)

        # ensure target tox doesn't have a file path
        target_op.par.externaltox = ''

        # reset target tox color to be default
        target_op.color = self.Reset_color

        # lock the tox icon
        # target_op.op('null_icon').lock = True

        # destory ops used for Dev
        destroy_tags = self.Destroy_tags.val.split(',')
        ops_to_destroy = target_op.findChildren(tags=destroy_tags)
        self.Destroy_ops(ops_to_destroy)

        # set all custom pars but about page to defaults
        self.SetCustomDefaults(target_op)

        # set parent shortcut par to be read only
        target_op.par.parentshortcut.readOnly = True

        # set bg top to be read read only
        target_op.par.opviewer.readOnly = True

        # hide ops
        self.HideOps(target_op)

        # add privacy
        self.AddPrivacy(target_op)

        # save TOX in target location
        target_op.save(save_loc)

        # destroy the buffer copy
        target_op.destroy()

        return save_loc

    def HideOps(self, targetOp):
        # hides ops from view
        hideTargets = targetOp.findChildren(tags=['HIDE'])
        if self.OwnerOp.par.Hideops.eval():
            for eachOp in hideTargets:
                eachOp.expose = False
                msg = f"Hiding op {eachOp.path}"
                self._log_release_event(msg=msg)

        pass

    def SetCustomDefaults(self, targetOp):
        '''Set Custom Defaults

        Skip all custom pars on about page
        All other custom pars, set to default vals
        '''
        for eachPar in targetOp.pars():
            if eachPar.isCustom and eachPar.page != 'About':
                eachPar.val = eachPar.default
                msg = f"Setting default for par {eachPar.name}"
                self._log_release_event(msg=msg)
            else:
                pass

    def AddPrivacy(self, targetOp):
        # find all ops tagged for privacy
        privacyOps = targetOp.findChildren(type=COMP, tags=['private'])

        for eachPrivateOp in privacyOps:
            print('private Op ', eachPrivateOp)

            # if the private flag is on, make all privacy ops private
            if self.OwnerOp.par.Makeprivate.eval():
                privacyKey = self.OwnerOp.par.Password.eval()
                privacyDev = self.OwnerOp.par.Developer.eval()
                privacyEmail = self.OwnerOp.par.Developeremail.eval()
                eachPrivateOp.addPrivacy(privacyKey,
                                         developerName=privacyDev,
                                         developerEmail=privacyEmail)
            else:
                pass
        pass

    def Destroy_ops(self, ops_to_destroy):

        for each in ops_to_destroy:
            msg = f"destroying op {each.path}"
            self._log_release_event(msg=msg)
            each.destroy()

        return ops_to_destroy

    def Disable_external_file(self, ops_to_prep):

        for each in ops_to_prep:
            try:
                # remove path par for ext
                each.par.file = ''
                # turn off loading on start
                each.par.loadonstart = False
                msg = f"disabling external file for op {each.path}"
                self._log_release_event(msg=msg)

            except:
                msg = f'Skipping Op {each.path}'
                self._log_release_event(msg=msg)

        return ops_to_prep

    def _log_release_event(self, msg: str) -> None:
        automation_msg = {
            "sender": f'TD - {self.Tox_Name.eval()}', "payload": msg}
        print(msg)
        log_file = f"{self.Save_dir.eval()}/log.txt"
        try:
            with open(log_file, "a") as file:
                file.write(f"TD {self.Tox_Name.eval()} | {msg}\n")
        except Exception as e:
            pass

    def _force_quit(self):
        msg = f"Quitting TouchDesigner"
        self._log_release_event(msg=msg)
        project.quit(force=True)

    def Open_github_link(self):
        webbrowser.open_new_tab(self.GithubLink)
        return self.GithubLink
