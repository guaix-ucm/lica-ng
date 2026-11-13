# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
class LicaSqaError(Exception):
    """LICA SQLAlchemy Error"""

    def __str__(self):
        msg = self.__doc__
        return f"{msg}: {self.args[0]}." if self.args else f"{msg}."


class DatabaseNotFoundError(LicaSqaError):
    """Database not found"""
