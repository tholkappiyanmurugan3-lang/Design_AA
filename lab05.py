import streamlit as st
import random

comparison_count = 0


# ------------------------------
# Divide and Conquer Min-Max
# ------------------------------
def min_max_dc(arr, low, high):
    global comparison_count

    if low == high:
        return arr[low], arr[low]

    if high == low + 1:
        comparison_count += 1

        if arr[low] < arr[high]:
            return arr[low], arr[high]

        return arr[high], arr[low]

    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


# ------------------------------
# Naive Method
# ------------------------------
def min_max_naive(arr):

    mn = mx = arr[0]
    comps = 0

    for x in arr[1:]:

        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(
    page_title="Min-Max using Divide & Conquer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Divide and Conquer - Min & Max Finder")

st.write("Enter array elements separated by commas.")

default_array = "3,1,7,4,9,2,8,5,6,0"

user_input = st.text_area(
    "Input Array",
    value=default_array,
    height=120
)

if st.button("Find Min and Max"):

    try:
        arr = [int(x.strip()) for x in user_input.split(",")]

        if len(arr) == 0:
            st.error("Array cannot be empty.")
            st.stop()

        global comparison_count
        comparison_count = 0

        mn, mx = min_max_dc(arr, 0, len(arr) - 1)
        dc_comps = comparison_count

        _, _, naive_comps = min_max_naive(arr)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Minimum", mn)
        col2.metric("Maximum", mx)
        col3.metric("D&C Comparisons", dc_comps)
        col4.metric("Naive Comparisons", naive_comps)

    except:
        st.error("Please enter valid integers separated by commas.")


st.divider()

st.header("Performance Analysis")

sizes = [10, 100, 1000, 10000]

table = []

for size in sizes:

    arr = [random.randint(1, 10000) for _ in range(size)]

    comparison_count = 0

    mn, mx = min_max_dc(arr, 0, len(arr) - 1)

    dc = comparison_count

    _, _, naive = min_max_naive(arr)

    formula = (3 * size) // 2 - 2

    table.append({
        "Array Size": size,
        "D&C Comparisons": dc,
        "Naive Comparisons": naive,
        "Formula (3n/2-2)": formula
    })

st.table(table)

st.info("""
Time Complexity

• Divide & Conquer : O(n)

• Naive Method : O(n)

Space Complexity

• Divide & Conquer : O(log n)

• Naive Method : O(1)
""")
