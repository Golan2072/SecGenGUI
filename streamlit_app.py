import map
import stargen
import streamlit as st
import pandas as pd


def sector_gen():
    xylocation = [0, 0]
    subsector_dict = {}
    for column in range(0, 9):
        subsector_dict[column] = {}
        for row in range(0, 11):
            xylocation[0] = column
            xylocation[1] = row
            if stargen.dice(1, 6) >= 4:
                subsector_dict[column][row] = stargen.World(xylocation)
                subsector_dict[column][row].generate_world()
            else:
                subsector_dict[column][row] = False
    return subsector_dict


if __name__ == "__main__":
    subsector = sector_gen()
    subsector_list = []
    for column in range (1, 9):
        for row in range (1, 11):
            if subsector[column][row] is not False:
                subsector_list.append({"Hex": subsector[column][row].location_string, "Name": subsector[column][row].name, "UWP": subsector[column][row].uwp_string, "GG": subsector[column][row].gas_giant, "Base": subsector[column][row].base, "Trade Codes": subsector[column][row].trade_string})
            else:
                pass
    index=list(range(len(subsector_list)))
    subsector_data = pd.DataFrame(subsector_list, index = index)
    st.table(subsector_data)

