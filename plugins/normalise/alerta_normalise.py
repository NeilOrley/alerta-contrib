
import logging

from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.normalise')

class NormaliseAlert(PluginBase):

    def pre_receive(self, alert):

        LOG.info("Normalising alert...")

        # prepend severity to alert text
        #alert.text = '%s: %s' % (alert.severity.upper(), alert.text)

        # supply different default values if missing
        if not alert.group or alert.group == 'Misc':
            alert.group = 'Unknown'
        if not alert.value or alert.value == 'n/a':
            alert.value = '--'
        if not alert.customer or alert.customer == 'n/a' or alert.customer == 'alerta-mco':
            alert.customer = 'MCO'


        # normalise resource
        baseurl = re.match("http[s]?://([^/?/$|^:?]+)",alert.resource)
        ip = re.match("([0-9\.]+)",alert.resource)
        if baseurl:
            alert.resource = baseurl.group(0)
        elif ip:
            alert.resource = ip.group(0)


        return alert

    def post_receive(self, alert):

        # normalise resource
        baseurl = re.match("http[s]?://([^/?/$|^:?]+)",alert.resource)
        ip = re.match("([0-9\.]+)",alert.resource)
        if baseurl:
            alert.resource = baseurl.group(0)
        elif ip:
            alert.resource = ip.group(0)

        return alert

    def status_change(self, alert, status, text):
        return

