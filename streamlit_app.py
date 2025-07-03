import map
import stargen
import streamlit as st


def sector_gen():
    xylocation = [0, 0]
    subsector_dict = {}
    for column in range(0, 8):
        subsector_dict[column] = {}
        for row in range(0, 11):
            xylocation = [column, row]
            if stargen.dice(1, 6) >= 4:
                subsector_dict[column][row] = stargen.World(xylocation)
                subsector_dict[column][row].generate_world()
            else:
                subsector_dict[column][row] = False
    return subsector_dict


if __name__ == "__main__":
    subsector = sector_gen()
    subsector_list = []
    for column in range (1, 8):
        for row in range (1, 11):
            if subsector[column][row]:
                subsector_list.append({"Hex": subsector[column][row].location_string, "Name": subsector[column][row].name, "UWP": subsector[column][row].uwp_string, "GG": subsector[column][row].gas_giant, "Base": subsector[column][row].base, "Trade Codes": subsector[column][row].trade_string})
            else:
                pass      
    sorted_subsector_list= sorted(subsector_list, key=lambda x: x['Hex'])
    st.set_page_config(page_title="Classic Traveller Subsector Generator")
    tab1, tab2 = st.tabs(["Subsector Data", "Subsector Map"])
    with tab1:
        st.title("Classic Traveller RPG")
        st.title("Subsector Data")
        st.table(sorted_subsector_list)
    with tab2:
        st.title("Classic Traveller RPG")
        st.title("Star Map")
        map.render_map(subsector_list)
