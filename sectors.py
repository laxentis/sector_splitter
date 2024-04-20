class Sector:
    def __init__(self, name: str, lower_limit: int, upper_limit: int, note: str, sector_type: str,
                 owners: str, alt_owner: str, active: str, guests: str, dep_apt: str, arr_apt: str,
                 add_display: str, minimum_safe_altitude_warning: int, definition: str, in_use: str = 'yes'):
        """
        Create a sector object
        :param name: Sector name
        :param lower_limit: Lower limit in feet
        :param upper_limit: Upper limit in feet
        :param note: Additional notes
        :param sector_type: Type of sector. Should be 'GND', 'TWR', 'APP', 'FIN', 'CTR' or 'OTH'.
        :param owners: Position names of owners of the sector in order of precedence.
        :param alt_owner: Alternative owner configurations
        :param active: Conditions for sector activation
        :param guests: Guest controllers that do not raise renegade alerts
        :param dep_apt: Departure airports the sector activates
        :param arr_apt: Arrival airports the sector activates
        :param add_display: Additional display lines definitions
        :param minimum_safe_altitude_warning: Minimum Safe Altitude Warning in feet
        :param definition: Sector definition, a sequence of DynPoints
        :param in_use: 'yes' or 'no', defaults to 'yes'
        """
        self.name = name
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.note = note
        self.sector_type = sector_type
        self.owners = owners
        self.alt_owner = alt_owner
        self.active = active
        self.guests = guests
        self.dep_apt = dep_apt
        self.arr_apt = arr_apt
        self.add_display = add_display
        self.minimum_safe_altitude_warning = minimum_safe_altitude_warning
        self.definition = definition
        self.in_use = True if in_use == 'yes' else False
