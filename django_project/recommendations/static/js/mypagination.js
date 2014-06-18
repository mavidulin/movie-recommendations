// we divide pages in sets. Each set contains 5 pages.
// We count number of first page in each set (first_page_number).
// we count number of sets (used to restrict use of next button).

//==================IN TEMPLATE IN SCRIPT DEFINE FOLLOWING VARS =============

// number_of_pages_in_set = 5 // define number of pages to be in one set
// number_of_pages = {{ page_obj.paginator.num_pages }}
// current_page_number = {{ page_obj.number }}

//==================END DEFINE==============================================

//=======AFTER DEFINING DATA CALL THIS SCRIPT====================
//=======<script src='/static/js/maypagination.js'></script>=====

active_pages_set = Math.ceil(current_page_number/number_of_pages_in_set)
current_pages_set = active_pages_set // used later for 'next' and 'prev'
first_page_number = 1+(number_of_pages_in_set*(active_pages_set-1)) // number of first page in current page set
number_pages_sets = Math.ceil(number_of_pages/number_of_pages_in_set)

show_pages();

function show_pages() {
    $('.pagination').empty()
    // append 'previous' button
    $('.pagination').append('<li id="prevButton"><span>&laquo;</span></li>');

    // append pages to current set
    page = first_page_number
    for (page; page < first_page_number+number_of_pages_in_set; page++) {
        if (page <= number_of_pages) {
            $('.pagination').append('<li id="page'+page+'"><a href="?page='+page+'">'+page+'</a></li>');
        }
    }

    // append 'next' button
    $('.pagination').append('<li id="nextButton"><span>&raquo;</span></li>');

    // click event listeners
    $('#prevButton').on('click', show_prev_set);
    $('#nextButton').on('click', show_next_set);

    // add active class
    $('#page'+current_page_number).addClass('active');
}

function show_prev_set() {
    if (current_pages_set>1) {
            current_pages_set -= 1
            first_page_number -= number_of_pages_in_set
    }
    show_pages();
}
function show_next_set() {
     if (current_pages_set<number_pages_sets) {
            current_pages_set += 1
            first_page_number += number_of_pages_in_set
    }
    show_pages();
}

