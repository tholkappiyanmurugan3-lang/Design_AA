import streamlit as st
import math

st.set_page_config(
    page_title="Bin Packing Visualizer",
    page_icon="📦",
    layout="wide"
)


# ---------------- Algorithms ---------------- #

def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:
        placed = False

        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    return first_fit(sorted(items, reverse=True), capacity)


def best_fit_decreasing(items, capacity=1.0):
    items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):
            if space >= item and (space - item) < best_space:
                best_space = space - item
                best_idx = i

        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------- UI ---------------- #

st.title("📦 Bin Packing Algorithm Visualizer")

st.write("Compare **First Fit**, **First Fit Decreasing**, and **Best Fit Decreasing**.")

capacity = st.number_input(
    "Bin Capacity",
    min_value=0.5,
    value=1.0,
    step=0.1
)

default_items = "0.5,0.7,0.3,0.9,0.2,0.6,0.8,0.4,0.1,0.5"

text = st.text_input(
    "Enter item sizes (comma separated)",
    default_items
)

try:
    items = [float(x.strip()) for x in text.split(",")]

    if st.button("Run Algorithms"):

        lower_bound = math.ceil(sum(items) / capacity)

        ff = first_fit(items, capacity)
        ffd = first_fit_decreasing(items, capacity)
        bfd = best_fit_decreasing(items, capacity)

        st.subheader("Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Lower Bound", lower_bound)
        c2.metric("FF", len(ff))
        c3.metric("FFD", len(ffd))
        c4.metric("BFD", len(bfd))

        def show_bins(title, bins):

            st.subheader(title)

            for i, b in enumerate(bins, start=1):

                used = sum(b)

                st.write(
                    f"**Bin {i}** : {b} | Used = {used:.2f}"
                )

                st.progress(min(used / capacity, 1.0))

        col1, col2, col3 = st.columns(3)

        with col1:
            show_bins("First Fit", ff)

        with col2:
            show_bins("First Fit Decreasing", ffd)

        with col3:
            show_bins("Best Fit Decreasing", bfd)

except:
    st.error("Please enter valid numbers separated by commas.")
