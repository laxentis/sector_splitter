import csv
from typing import TextIO

from utils import Coordinates, LatLong


class Position:
    """Class representing an ATC position"""
    def __init__(self, name: str, callsign: str, frequency: float, identifier: str, middle_letter: str,
                 prefix: str, suffix: str, ssr_start: str, ssr_end: str, vis_points=None):
        """
        Create an ATC position
        :param name: Name of the ATC position, e.g. EPWW_N_CTR
        :param callsign: Radio-telephony callsign of the position
        :param frequency: Radio frequency of the position in MHz
        :param identifier: Identifier of the position, e.g. NWW
        :param middle_letter: Middle letter discriminating this position, e.g. N
        :param prefix: Prefix of the position, e.g. EPWW
        :param suffix: Suffix of the position, e.g. CTR
        :param ssr_start: Start of squawk range
        :param ssr_end: End of squawk range
        :param vis_points: Array of visibility points (optional)
        """
        if vis_points is None:
            vis_points = []
        self.name = name
        self.callsign = callsign
        self.frequency = frequency
        self.identifier = identifier
        self.middle_letter = middle_letter
        self.prefix = prefix
        self.suffix = suffix
        self.ssr_start = str(ssr_start)
        self.ssr_end = str(ssr_end)
        self.vis_points = vis_points

    @staticmethod
    def from_string(string: str):
        """Create ATC position from ESE file formatted string"""
        string = string.split(':')
        name = string[0]
        callsign = string[1]
        frequency = float(string[2])
        identifier = string[3]
        middle_letter = string[4]
        prefix = string[5]
        suffix = string[6]
        ssr_start = string[9]
        ssr_end = string[10]
        vis_points = []
        if len(string) > 12:
            lat = Coordinates(string[11])
            lon = Coordinates(string[12])
            vis_points.append(LatLong(lat, lon))
        if len(string) > 14:
            lat = Coordinates(string[13])
            lon = Coordinates(string[14])
            vis_points.append(LatLong(lat, lon))
        if len(string) > 16:
            lat = Coordinates(string[15])
            lon = Coordinates(string[16])
            vis_points.append(LatLong(lat, lon))
        if len(string) > 18:
            lat = Coordinates(string[17])
            lon = Coordinates(string[18])
            vis_points.append(LatLong(lat, lon))

        return Position(name, callsign, frequency, identifier, middle_letter, prefix, suffix, ssr_start, ssr_end,
                        vis_points)

    def __str__(self):
        return f"{self.callsign} ({self.name} - {self.frequency})"


class Radar:
    """Class representing a radar station"""
    def __init__(self, name: str, position: LatLong,
                 p_range: int, p_alt: int, p_cone: int,
                 s_range: int, s_alt: int, s_cone: int,
                 c_range: int, c_alt: int, c_cone: int):
        """
        Create a radar station
        :param name: Name of the radar station
        :param position: Position of the radar station
        :param p_range: PSR range in Nautical Miles
        :param p_alt: Altitude of the PSR antenna in feet
        :param p_cone: PSR cone of silence in feet per Nautical Mile
        :param s_range: S-mode range in Nautical Miles
        :param s_alt: Altitude of the S-mode antenna in feet
        :param s_cone: S-mode cone of silence in feet per Nautical Mile
        :param c_range: C-mode range in Nautical Miles
        :param c_alt: Altitude of the C-mode antenna in feet
        :param c_cone: C-mode cone of silence in feet per Nautical Mile
        """
        self.name = name
        self.position = position
        self.p_range = p_range
        self.p_alt = p_alt
        self.p_cone = p_cone
        self.s_range = s_range
        self.s_alt = s_alt
        self.s_cone = s_cone
        self.c_range = c_range
        self.c_alt = c_alt
        self.c_cone = c_cone

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def from_string(string):
        """Create radar station from ESE formatted string"""
        string = string.split(':')
        name = string[1]
        lat = Coordinates(string[2])
        lng = Coordinates(string[3])
        position = LatLong(lat, lng)
        p_range = string[4]
        p_alt = string[5]
        p_cone = string[6]
        s_range = string[7]
        s_alt = string[8]
        s_cone = string[9]
        c_range = string[10]
        c_alt = string[11]
        c_cone = string[12]
        return Radar(name, position, p_range, p_alt, p_cone, s_range, s_alt, s_cone, c_range, c_alt, c_cone)


class Label:
    """Class representing a text label"""
    def __init__(self, group: str, text: str, position: LatLong):
        """
        Create a text label
        :param group: Group to store the label at
        :param text: Text of the label
        :param position: Position of the label
        """
        self.group = group
        self.text = text
        self.position = position

    def __str__(self):
        return f"{self.text}"

    @staticmethod
    def from_string(string: str):
        string = string.split(':')
        lat = Coordinates(string[0])
        lng = Coordinates(string[1])
        position = LatLong(lat, lng)
        group = string[2]
        text = string[3]
        return Label(group, text, position)


class DynPoint:
    """Class representing a GNG dynamic point"""
    def __init__(self, name: str, position: LatLong):
        """
        Create a dynamic point
        :param name: Name of the point, e.g. EPWW913
        :param position: Geographic position of the point
        """
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.name}"


class ESEFile:
    Positions: set[Position] = set()
    Radars: set[Radar] = set()
    Labels: set[Label] = set()
    DynPoints: set[DynPoint] = set()
    file: TextIO = None

    def __init__(self, file):
        """
        Open file for parsing
        :param file: Path to ESE file
        """
        self.file = open(file, encoding='utf-8')
        self._parse()

    def __del__(self):
        self.file.close()

    def _parse(self):
        line = self.file.readline()
        while line:
            line = line.strip()
            if line == "[POSITIONS]":
                self._parse_positions()
            # SIDs and STARS
            # STAR
            # SID
            # AIRSPACE
            # COPX
            # RADAR
            if line == "[RADAR]":
                self._parse_radars()
            # LABELS
            if line == "[FREETEXT]":
                self._parse_labels()
            line = self.file.readline()

    def _parse_positions(self):
        line = self.file.readline().strip()
        while line:
            line = line.strip()
            if not line:
                break
            self.Positions.add(Position.from_string(line))
            line = self.file.readline()

    def _parse_radars(self):
        line = self.file.readline().strip()
        while line:
            line = line.strip()
            if not line:
                break
            self.Radars.add(Radar.from_string(line))
            line = self.file.readline()

    def _parse_labels(self):
        line = self.file.readline().strip()
        while line:
            line = line.strip()
            if not line:
                break
            if line[0] != ';':
                label = Label.from_string(line)
                if label.group == 'DynPoints':
                    self.DynPoints.add(DynPoint(label.text, label.position))
                else:
                    self.Labels.add(label)
            line = self.file.readline()

    def write_positions(self):
        """Write ATC positions to a CSV file"""
        with open("output/positions.csv", 'w', newline='', encoding='utf-8') as positions_file:
            positions_writer = csv.writer(positions_file)
            positions_writer.writerow(["Name", "Callsign", "Frequency", "Identifier", "Middle Letter", "Prefix",
                                       "Suffix", "SSR Start", "SSR End"])
            for position in self.Positions:
                positions_writer.writerow([position.name, position.callsign, position.frequency, position.identifier,
                                           position.middle_letter, position.prefix, position.suffix, position.ssr_start,
                                           position.ssr_end])

    def write_visibility_points(self):
        """Write ATC visibility centers to a CSV file"""
        with open('output/visibility_points.csv', 'w', newline='', encoding='utf-8') as visibility_points_file:
            writer = csv.writer(visibility_points_file)
            writer.writerow(["Name", "Y", "X"])
            for position in self.Positions:
                for visibility_point in position.vis_points:
                    writer.writerow([position.name, visibility_point.lat, visibility_point.lng])

    def write_radars(self):
        """Write radar stations to a CSV file"""
        with open('output/radars.csv', 'w', newline='', encoding='utf-8') as radar_file:
            writer = csv.writer(radar_file)
            writer.writerow(["Name", "Y", "X",
                             "P range", "P altitude", "P cone slope",
                             "S range", "S altitude", "S cone slope",
                             "C range", "C altitude", "C cone slope"])
            for radar in self.Radars:
                writer.writerow([radar.name, radar.position.lat, radar.position.lng,
                                 radar.p_range, radar.p_alt, radar.p_cone,
                                 radar.c_range, radar.c_alt, radar.c_cone,
                                 radar.s_range, radar.s_alt, radar.s_cone,])

    def write_labels(self):
        """Write text labels to a CSV file"""
        with open('output/labels.csv', 'w', newline='', encoding='utf-8') as label_file:
            writer = csv.writer(label_file)
            writer.writerow(['Y', 'X', 'Group', 'Text'])
            for label in self.Labels:
                writer.writerow([label.position.lat, label.position.lng, label.group, label.text])

    def write_dynpoints(self):
        """Write Dynamic Points to a CSV file"""
        with open('output/dynpoints.csv', 'w', newline='', encoding='utf-8') as dynpoints_file:
            writer = csv.writer(dynpoints_file)
            writer.writerow(['Y', 'X', 'Name'])
            for point in self.DynPoints:
                writer.writerow([point.position.lat, point.position.lng, point.name])
