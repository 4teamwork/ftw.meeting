from ftw.upgrade import UpgradeStep


class UpdateMeetingItemView(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.meeting.upgrades:1400')
