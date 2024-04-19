import csv

from utils import Coordinates, LatLong


class Position:
    def __init__(self, name: str, callsign: str, frequency: float, identifier: str, middle_letter: str,
                 prefix: str, suffix: str, ssr_start: str, ssr_end: str, vis_points=None):
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
    def from_string(string):
        string = string.split(':')
        name = string[0]
        callsign = string[1]
        frequency = string[2]
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
    def __init__(self, name: str, position: LatLong, p_range, p_alt, p_cone, s_range, s_alt, s_cone, c_range, c_alt, c_cone):
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
    def __init__(self, group: str, text: str, position: LatLong):
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


class ESEFile:
    Positions = set()
    Radars = set()
    Labels = set()
    file = None

    def __init__(self, file):
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
                self.Labels.add(Label.from_string(line))
            line = self.file.readline()


    def write_positions(self):
        with open("output/positions.csv", 'w', newline='', encoding='utf-8') as positions_file:
            positions_writer = csv.writer(positions_file)
            positions_writer.writerow(["Name", "Callsign", "Frequency", "Identifier", "Middle Letter", "Prefix",
                                       "Suffix", "SSR Start", "SSR End"])
            for position in self.Positions:
                positions_writer.writerow([position.name, position.callsign, position.frequency, position.identifier,
                                           position.middle_letter, position.prefix, position.suffix, position.ssr_start,
                                           position.ssr_end])

    def write_visibility_points(self):
        with open('output/visibility_points.csv', 'w', newline='', encoding='utf-8') as visibility_points_file:
            writer = csv.writer(visibility_points_file)
            writer.writerow(["Name", "Y", "X"])
            for position in self.Positions:
                for visibility_point in position.vis_points:
                    writer.writerow([position.name, visibility_point.lat, visibility_point.lng])

    def write_radars(self):
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
        with open('output/labels.csv', 'w', newline='', encoding='utf-8') as label_file:
            writer = csv.writer(label_file)
            writer.writerow(['Y', 'X', 'Group', 'Text'])
            for label in self.Labels:
                writer.writerow([label.position.lat, label.position.lng, label.group, label.text])
