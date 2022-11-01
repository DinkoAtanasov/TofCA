
from configparser import ConfigParser


class CfgParser(ConfigParser):
    """
    ConfigParser with a custom dictionary conversion method.
    """

    def as_dict(self) -> dict:
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

    def dict_to_parser(self, d) -> None:
        """
        Convert modified settings from dictionary to ConfigParser variables.
        Dict of dicts, i.e. {Section1:{field:value, ...}, Section2:{field:value,...}}
        :return:
        """
        self.read_dict(d)
