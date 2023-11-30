from io import StringIO
import streamlit as st
import csv

import terray_db.log.models as log


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


# functions for yes and no check boxes
def yes(question_num):
    checkbox_yes = st.checkbox("Yes 🤩", key=f"yes-{question_num}")
    return checkbox_yes


def no(question_num):
    checkbox_no = st.checkbox("No 😔", key=f"no-{question_num}")
    return checkbox_no


# main function to start collecting data into dict and display questions with check boxes using the yes/no functions
def collect_data():

    # counter for "yes" and "no" check box to have unique key args
    yes_counter = 0
    no_counter = 0

    # empty list for data collection
    data = {
        "questions": {},
        "stalls": {},
    }

    # series of loops through list of questions defined above to display question and yes/no check box
    # microscope section
    st.header("Microscope: ")

    for m_question in MICROSCOPE_QUESTIONS_DICT:

        question = st.write(MICROSCOPE_QUESTIONS_DICT[m_question])

        if yes(yes_counter):
            data["questions"][m_question] = True
            st.write("Yay :)")

        elif no(no_counter):
            data["questions"][m_question] = False
            st.write("Awe :(")

        yes_counter += 1
        no_counter += 1

    # nacho plate section
    st.header("Nacho Plates: ")

    for n_question in NACHO_QUESTIONS_DICT:

        question = st.write(NACHO_QUESTIONS_DICT[n_question])

        if yes(yes_counter):
            data["questions"][n_question] = True
            st.write("Yay :)")

        elif no(no_counter):
            data["questions"][n_question] = False
            st.write("Awe :(")

        yes_counter += 1
        no_counter += 1

    # flow cell section
    st.header("Flow cell: ")

    for f_question in FLOW_CELL_QUESTIONS_DICT:

        question = st.write(FLOW_CELL_QUESTIONS_DICT[f_question])

        if yes(yes_counter):
            data["questions"][f_question] = True
            st.write("Yay :)")

        elif no(no_counter):
            data["questions"][f_question] = False
            st.write("Awe :(")

        yes_counter += 1
        no_counter += 1

    # leaks sections
    st.header("Leaks: ")

    for l_question in LEAK_QUESTIONS_DICT:

        question = st.write(LEAK_QUESTIONS_DICT[l_question])

        if yes(yes_counter):
            data["questions"][l_question] = True
            st.write("Yay :)")

        elif no(no_counter):
            data["questions"][l_question] = False
            st.write("Awe :(")

        yes_counter += 1
        no_counter += 1

    # registration section
    st.header("Registration: ")

    for r_question in REG_QUESTIONS_DICT:

        question = st.write(REG_QUESTIONS_DICT[r_question])

        if yes(yes_counter):
            data["questions"][r_question] = True
            st.write("Yay :)")

        elif no(no_counter):
            data["questions"][r_question] = False
            st.write("Awe :(")

        yes_counter += 1
        no_counter += 1

    st.header("Additional Info")
    general_notes = st.text_area("General Notes: ")
    data["notes"] = general_notes

    return data


# format data dict to take in abreviated question and user answer as csv formatted string
def format_data(data):

    csv_data = StringIO()
    writer = csv.writer(csv_data)

    for key, value in data.items():
        writer.writerow([key, value])

    return csv_data.getvalue()


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
    # get working with decodeing updates ultra to pull microscope names?
    microscope = st.selectbox(
        "Please select the microscope number: ",
        ("D01", "D02", "D03", "D04", "D05", "D06", "D07", "D09", "D10", "D11", "D12"),
        # index=None,
        # placeholder="Choose an option"
    )

    # display microscope name
    st.write(microscope)

    # prompt for experiment ids
    # get working with decoding updates ultra to pull all lgs
    experiment_id = st.text_input(
        "Please enter each experiment ID separated by a comma ( ,): "
    )

    # try casting nums after split to integers for experiment id validation, if not int provide invalid id
    temp_list = []
    for num in experiment_id.split(","):
        num_stripped = num.strip()

        try:
            temp_num = int(num_stripped)
            temp_list.append(temp_num)
            # check if experiment id occurs more than once in temp list
            if temp_list.count(temp_num) > 1:
                st.error(
                    f"Invalid experiment ID: {num}. Please only enter unique experiment IDs."
                )
            elif len(num_stripped) != 7:
                st.error(
                    f"Invalid experiment ID: {num}. Please enter an ID of correct format (300XXXX)."
                )
        except ValueError:
            if experiment_id:
                st.error(
                    f" Invalid experiment ID: {num}. Please enter only integers separated by a comma (,)."
                )

        experiment_id_list = temp_list

    # display experiment ids
    st.write(experiment_id_list)

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
    data["experiment_id"] = experiment_id_list
    data["reviewer"] = reviewer.title()
    data["date"] = date.isoformat()
    data["stalls"]["num_stalls"] = run_stall
    data["stalls"]["stall_reason"] = stall_reason

    data_string = format_data(data)

    # temp for debugging - remove later
    st.write(data)

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