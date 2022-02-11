
import logging
import re

from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.normalise')


class NormaliseAlert(PluginBase):

    def pre_receive(self, alert):

        LOG.info("Normalising alert...")

        # format alert text
        alert.text = '%s: %s says %s on %s' % (alert.severity.upper(), alert.group, alert.event, alert.resource)

        # supply different default values if missing
        if not alert.group or alert.group == 'Misc':
            alert.group = 'Unknown'
        if not alert.value or alert.value == 'n/a':
            alert.value = '--'
        if not alert.customer or alert.customer == 'n/a' or alert.customer == 'alerta-mco':
            alert.customer = 'MCO'

        # normalise group
        if re.search("exportermissing|exporter_down|cloudprober_down|ExporterFlapping|Cloudprober_Down",alert.event,re.IGNORECASE):
            alert.group = 'Monitoring'
        elif re.search("disk|inode",alert.event,re.IGNORECASE):
            alert.group = 'Filesystem'
        elif re.search("Blackbox_exporter_Lattency|docker|supervisor",alert.event,re.IGNORECASE):
            alert.group = 'Service'
        elif re.search("DB_Oracle_Not_Responding",alert.event,re.IGNORECASE):
            alert.group = 'DB'
        elif re.search("idrac",alert.event,re.IGNORECASE):
            alert.group = 'Hardware'

        # normalise resource
        baseurl = re.match("http[s]?://([^/?/$|^:?]+)",alert.resource)
        ip = re.match("([0-9\.]+)",alert.resource)
        if baseurl:
            alert.resource = baseurl.group(0)
        elif ip:
            alert.resource = ip.group(0)


        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
