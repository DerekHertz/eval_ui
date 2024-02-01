import streamlit as st
import numpy as np
from typing import Union

import ..._db.log.models as log
from ..._core.db import exp
from ..._notebooks.utils.decoding_updates_ultra import (
    get_recent_experiments,
    get_chips_for_lg,
    get_chip_libaries,
)

SCOPES = [f"TIGERD{x}" for x in range(1, 13)] + [None]

# question dict for downstream formatting
MICROSCOPE_QUESTIONS_DICT = {
    "objective_in_immersion": "Is the objective still in immersion water (within 1 hour of idling)?",
    "drip_line_close": "Is the drip line <2mm from the objective?",
    "caps_closed": "Are any of the bottle caps loose?",
    "fluidic_lines_submerged": "Are the fluidic lines in each buffer source bottle (PBT, 40% Formamide, 90% Formamide, DI) submerged?",
    "fluidic_lines_tension": "Are any of the fluidic lines under tension?",
    "fluidic_lines_damaged": "Are any of the autosampler/waste lines connected to the 4-way valves kinked or damaged?",
    "waste_lines_secure": "Are the waste lines secured in the plastic clip on the shoulder of the microscope?",
}

# nacho dict for downstream formatting
NACHO_QUESTIONS_DICT = {
    "nacho_flat": "Is the Nacho plate sitting flat in the correct orientation (A1 is A1)?",
    "puncture_center": "Are all puncture marks on the 3 Nacho plates in the center of the wells?",
    "hybs_pulled": "Were all hybs sufficiently pulled?",
}

# flow cell dict for downstream formatting
FLOW_CELL_QUESTIONS_DICT = {
    "valves_open": "Are all necessary 4-way valves open?",
    "valves_need_tightening": "Do any of the handles on thee 4-way valves need tightening?",
    "inlet_outlet_damaged": "Are any of the inlet or outlet lines from the 4-way valve to beneath the flow cell kinked or appear damaged?",
    "black_gasket_protrude": "Is there any black gasketing protruding into the optical window on each set?",
    "glass_crack": "Does there appear to be any fracture in the glass for each set in use?",
    "dust_ontop": "Is there a significant amount of dust on the optical window or flow cell top? (if the flow cell has not been sitting idle for an extend period)",
    "screws_down": "Do all necessary screws appear recessed?",
    "gaps_ontop": "Are there any spaces/gaps between the metal flow cell top and the flow cell?",
}

# leak dict for downstream formatting
LEAK_QUESTIONS_DICT = {
    "fluid_on_ranger": "Is there a significant amount of fluid on the tiger ranger?",
    "immersion_spilled": "Has the immersion DI 'spilled' off the flow cell top?",
    "air_table_level": "Is the air table/bread board level?",
    "drips_underneath_FC": "Are there any drips hanging from the bottom of the flow cell? (pay attention to inlet and outlet lines)",
    "liquid_on_valves": "Is there any liquid on the outside housing of the 4-way valves?",
    "valve_lines_tight": "Are all the fluidic lines screwed into the 4-way valves finger tight?",
    "leak_detectable": "After cleaning/drying the setup and running the PBT flush, is a leak detecable?",
}

# registration dict for downstream formatting
REG_QUESTIONS_DICT = {
    "images_transferred": "Did all images automatically transfer? If not run Ubuntu",
    "correct_hybs": "Were the correct hybs run and imaged?",
    "correct_chips": "Were all chips listed correctly in decode registration ultra? Ensure QR codes are updated",
    "imaging_runs_updated": "Are all expected imaging runs registered?",
    "photometry_updated": "Are all the available photometries registered/updated?",
}

# function for yes and no radio button
def yes_no_radio_button(question: str) -> Union[bool, None]:
    """Create yes/no radio button and return True/False or None if neither selected"""
    radio_response = st.radio(question, ["None", "Yes 🤩", "No 😔"])

    if radio_response is None:
        st.warning("Please select an option.")
        return None

    if radio_response == "Yes 🤩":
        st.write("🫡")
        return True
    elif radio_response == "No 😔":
        st.write("🫨")
        return False
    elif radio_response == "None":
        return None


# main function to start collecting data into dict and display questions with check boxes using the yes/no functions
def collect_data():

    # empty list for data collection
    data = {
        "questions": {},
        "stalls": {},
    }

    # series of loops through list of questions defined above to display question and yes/no check box
    # microscope section
    st.header("Microscope: ")

    for name, text in MICROSCOPE_QUESTIONS_DICT.items():
        response = yes_no_radio_button(text)
        if response is not None:
            data["questions"][name] = response

    # nacho plate section
    st.header("Nacho Plates: ")

    for name, text in NACHO_QUESTIONS_DICT.items():
        response = yes_no_radio_button(text)
        if response is not None:
            data["questions"][name] = response

    # flow cell section
    st.header("Flow cell: ")

    for name, text in FLOW_CELL_QUESTIONS_DICT.items():
        response = yes_no_radio_button(text)
        if response is not None:
            data["questions"][name] = response

    # leaks sections
    st.header("Leaks: ")

    for name, text in LEAK_QUESTIONS_DICT.items():
        response = yes_no_radio_button(text)
        if response is not None:
            data["questions"][name] = response

    # registration section
    st.header("Registration: ")

    for name, text in REG_QUESTIONS_DICT.items():
        response = yes_no_radio_button(text)
        if response is not None:
            data["questions"][name] = response

    st.header("Additional Info")
    general_notes = st.text_area("General Notes: ")
    data["notes"] = general_notes

    return data


# ============================================= UI =============================================


def main():
    st.title("Decoding Microscope Evaluation Checklist")

    # prompt for decoders name
    decoder = st.text_input("Please enter the decoder's name: ")

    # display decoders name
    st.write(decoder)

    # prompt for ranger/flow cell information
    ranger = st.number_input("Please enter the ranger ID number: ", min_value=1, step=1)

    flow_cell_top = st.text_input("Please enter the flow cell top ID letter: ")

    if len(flow_cell_top) > 1:
        st.error("Please enter only one ID letter")

    # dropdown for microscope name
    microscope = st.selectbox(
        "Please select the microscope number: ", SCOPES, index=len(SCOPES) - 1
    )

    # display microscope name
    st.write(microscope)

    lg_id_options = get_recent_experiments()
    # prompt for experiment ids using get_recent_experiments() function
    experiment_id = st.multiselect("Please select each experiment ID: ", lg_id_options)

    # Get the chips associated to lg
    chip_list = [get_chips_for_lg(exp_lgid) for exp_lgid in experiment_id]
    chip_list = [i for x in chip_list for i in x]
    chip_to_library = get_chip_libaries(chip_list)
    libraries = set(chip_to_library.values())

    # display a dictionary of chip names associated to given experiment id and subset names
    if experiment_id:
        st.write("Library/libraries: ")
        st.write(chip_to_library)

    # prompt for who is doing the eval
    reviewer = st.text_input("Please write who is reviewing the setup: ")

    # date selection for experiment start date
    date = st.date_input("Please choose the experiment start date: ")

    # count of how many stalls (if any)
    run_stall = st.number_input(
        "Did the run stall? How many times?: ", min_value=0, step=1
    )

    # drop down selection with common errors
    stall_reason = st.multiselect(
        "Why did the run stall? (select for each stall)",
        [
            "Microsoft/computer update",
            "Camera acquisition error",
            "Out of focus",
            "Cracked glass",
            "Network loss",
            "Power outage",
            "Chip spacing",
            "Autosampler timeout",
            "Circular Buffer Overflow",
            "Other (specify below)",
        ],
        # max_selections=run_stall
    )

    other_stall = st.text_input("Other: ")

    # Collect yes/no answers for the eval itself
    data = collect_data()
    # Add the extra information we collected earlier
    data["decoder"] = decoder.title()
    data["ranger"] = ranger
    data["flow cell top"] = flow_cell_top.upper()
    data["microscope"] = microscope
    data["experiment_id"] = experiment_id
    data["reviewer"] = reviewer.title()
    data["date"] = date.isoformat()
    data["stalls"]["num_stalls"] = run_stall
    data["stalls"]["stall_reason"] = stall_reason
    data["stalls"]["other"] = other_stall

    # conditional to check if experiment ids were entered
    if not experiment_id:
        st.warning("Please enter an experiment ID")
    elif not microscope:
        st.warning("Please enter an microscope")
    else:
        if st.button("Submit this microscope evaluation"):
            experiment_ids = data.pop("experiment_id")
            # Insert into the MicroscopeEvaluation table
            eval_object = log.MicroscopeEvaluation(
                decoder=data.pop("decoder"),
                microscope=data.pop("microscope"),
                reviewer=data.pop("reviewer"),
                eval_metadata=data,
            )
            eval_object.save()
            # Insert into the ExperimentEval link table
            for experiment_id in experiment_ids:
                exp_eval = log.ExperimentEval(
                    experiment_id=experiment_id,
                    microscope_evaluation=eval_object,
                )
                exp_eval.save()
            st.success("Microscope evaluation submitted")
            st.balloons()

    st.header(
        "Please proceed to job submission once everything is complete/registered/updated 🥳"
    )
