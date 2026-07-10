import streamlit as st
import random

# --------------------------------------------------
# Divide and Conquer Algorithm
# --------------------------------------------------
def min_max_dc(arr, low, high):
    # Returns (minimum, maximum, comparisons)

    if low == high:
        return arr[low], arr[low], 0

    if high == low + 1:
        if arr[low] < arr[high]:
            return arr[low], arr[high], 1
        else:
            return arr[high], arr[low], 1

    mid = (low + high) // 2

    lmin, lmax, lcomp = min_max_dc(arr, low, mid)
    rmin, rmax, rcomp = min_max_dc(arr, mid + 1, high)

    comparisons = lcomp + rcomp + 2

    overall_min = lmin if lmin < rmin else rmin
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max, comparisons


# --------------------------------------------------
# Naive Algorithm
# --------------------------------------------------
def min_max_naive(arr):
    mn = mx = arr[0]
    comparisons = 0

    for x in arr[1:]:

        comparisons += 1
        if x < mn:
            mn = x

        comparisons += 1
        if x > mx:
            mx = x

    return mn, mx, comparisons


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.set_page_config(
    page_title="Min-Max using Divide & Conquer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Divide and Conquer - Minimum & Maximum Finder")

st.write(
    "Enter array elements separated by commas."
)

default_array = "3,1,7,4,9,2,8,5,6,0"

user_input = st.text_area(
    "Input Array",
    value=default_array,
    height=120
)

if st.button("Find Minimum and Maximum"):

    try:

        arr = [int(x.strip()) for x in user_input.split(",")]

        if len(arr) == 0:
            st.error("Array cannot be empty.")
            st.stop()

        minimum, maximum, dc_comparisons = min_max_dc(
            arr, 0, len(arr) - 1
        )

        _, _, naive_comparisons = min_max_naive(arr)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Minimum", minimum)
        col2.metric("Maximum", maximum)
        col3.metric("D&C Comparisons", dc_comparisons)
        col4.metric("Naive Comparisons", naive_comparisons)

        st.success("Computation Completed Successfully!")

    except:
        st.error("Please enter valid integers separated by commas.")


st.divider()

st.header("Performance Analysis")

sizes = [10, 100, 1000, 10000]

results = []

for size in sizes:

    arr = [random.randint(1, 10000) for _ in range(size)]

    _, _, dc = min_max_dc(arr, 0, len(arr) - 1)

    _, _, naive = min_max_naive(arr)

    formula = (3 * size) // 2 - 2

    results.append({
        "Array Size": size,
        "D&C Comparisons": dc,
        "Naive Comparisons": naive,
        "Formula (3n/2 - 2)": formula
    })

st.table(results)

st.divider()

st.subheader("Time Complexity")

st.markdown("""
- **Divide & Conquer:** **O(n)**
- **Naive Method:** **O(n)**
""")

st.subheader("Space Complexity")

st.markdown("""
- **Divide & Conquer:** **O(log n)**
- **Naive Method:** **O(1)**
""")
