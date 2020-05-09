// If topping in selected pizza display toppings options
toppings = document.getElementById("toppings");

// https://www.geeksforgeeks.org/hide-or-show-elements-in-html-using-display-property/
toppings.style.display = "none";

let selectedPizza = document.getElementById('selectedpizza')

selectedPizza.onchange = (event) => {
    // https://stackoverflow.com/questions/38519791/how-to-get-data-attribute-of-option-tag-in-javascript
    // let piztype = event.target.options[event.target.selectedIndex].dataset.piztype;
    let piztype = selectedPizza.options[selectedPizza.selectedIndex].dataset.piztype
    console.log(piztype);

    // Reset all boxes to unchecked
    let boxes = document.getElementsByClassName('top');
    for (let i=0; i<boxes.length; i++) {
        boxes[i].checked = false;
    }

    // Only display toppings selection if user selected toppings type
    if (piztype.includes('Topping')) {
        var limit = parseInt(piztype[0]);
        console.log(limit)
        toppings.style.display = "block";
    }
    else {
        toppings.style.display = "none";
    }    
};

// Set max limit for number of checked checkboxes depending on number of toppings selected
$('input[class=top]').on('change', function (event) {
    let piztype = selectedPizza.options[selectedPizza.selectedIndex].dataset.piztype
    let limit = parseInt(piztype[0])
    console.log(limit);
    console.log('now', $('input[type=checkbox]:checked').length)
    if ($('input[type=checkbox]:checked').length > limit) {
        console.log("UNDO");
        // this.checked = false;
        $(this).prop('checked', false);
        console.log('checked:', this.checked);
        console.log($('input[type=checkbox]:checked').length);
        // alert("allowed");
    }
});


// If addition is NOT "Extra Cheese", hide it as it only applies to a specific sub
additions = document.querySelectorAll(".subadds");
addBoxes = document.querySelectorAll(".add-item");

toggleEachBox(additions, addBoxes, true);

let selectedSub = document.getElementById('selectedsub')

selectedSub.onchange = (event) => {
    // Get at all options of the select element. How do we know which one to focus on?
    // Use the index of selected option (selectedSub.selectedIndex) to get at selected option element
    // Get the option element's type using .dataset.subtype
    let option = selectedSub.options[selectedSub.selectedIndex]
    let subtype = option.dataset.subtype
    console.log(subtype);

    // Reset all boxes to unchecked
    let boxes = document.getElementsByClassName('subadds');
    for (let i=0; i<boxes.length; i++) {
        boxes[i].checked = false;
    }

    // Only display specific additions if user selected specific sub (Steak + Cheese)
    if (subtype === ('Steak + Cheese')) {
        toggleEachBox(additions, addBoxes, false);
    }
    else {
        toggleEachBox(additions, addBoxes, true);
    }
};

// https://stackoverflow.com/questions/3010840/loop-through-an-array-in-javascript
function toggleEachBox(boxInputs, addBoxes, boolean) {
    for (let i=0; i<boxInputs.length; i++) {
        if (boxInputs[i].dataset.exclude !== "Extra Cheese") {
            addBoxes[i].disabled = boolean;
        }
    }
}
