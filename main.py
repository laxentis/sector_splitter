from esefile import ESEFile

if __name__ == '__main__':
    ese = ESEFile('sector.ese')
    print("Positions")
    for pos in ese.Positions:
        print(f"{str(pos):>64}\tVIS: {len(pos.vis_points)}")
    print("Radars")
    for rad in ese.Radars:
        print(f"{rad}")
    ese.write_positions()
    ese.write_visibility_points()
    ese.write_radars()
    ese.write_labels()
