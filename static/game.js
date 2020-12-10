/*
* Scripts for game.html
*/

// When user clicks "Reset", reset all buttons and form items to their original state
function reset() {
    // Reset form
    document.getElementById("submit_tossup").reset()
    // Hide bonus buttons
    document.getElementById("bonus-container").style.display = "none"
    // Hide score buttons
    for (e of document.getElementsByClassName("score-buttons")) {
        e.style.visibility = "hidden"
    }
    // Untoggle all Bootstrap buttons
    for (e of document.getElementsByClassName("btn")) {
        e.removeAttribute("disabled")
        e.classList.remove("active")
        e.removeAttribute("aria-pressed")
    }
}

// When a player's button is clicked, toggle their button, show their score buttons,
// and disable the buttons of all other team members, since there can be only one score event
// per team per tossup
function playerButtonClicked(element) {
    // Toggle Bootstrap buttons
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    // Show player's score buttons
    p_id = element.parentElement.id
    document.getElementById(p_id + "-buttons").style.visibility = "visible"

    // Disable player's team's player buttons
    button_divs = element.parentElement.parentElement.getElementsByClassName("player-buttons")
    for (e of button_divs) {
        if (e.id != p_id) {
            e.getElementsByClassName("player-button")[0].disabled = "true"
        }
    }
}

// Respond to user clicking a power button (a yellow "15" button)
function power(element) {
    // Show bonus buttons
    document.getElementById("bonus-container").style.display = "flex"

    // Toggle Bootstrap button
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    // Set hidden form values to reflect this player has scored 15 points
    p_id = element.parentElement.parentElement.id
    document.getElementById("scoring-player").value = p_id
    document.getElementById("score").value = element.getAttribute("score")
    
    // Disable other team's buttons since once a player has powered the other team
    // can no longer buzz on this tossup
    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "btn")

    // Disable this player's 10 and -5 buttons
    b_group = element.parentElement
    b_group.getElementsByClassName("ten")[0].disabled = "true"
    b_group.getElementsByClassName("neg")[0].disabled = "true"
}

// Respond to user clicking green 10 point (tossup) button
function score(element) {
    // Show bonus buttons
    document.getElementById("bonus-container").style.display = "flex"

    // Toggle Bootstrap button
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    // Set hidden form values to reflect this player has scored 10 points
    p_id = element.parentElement.parentElement.id
    document.getElementById("scoring-player").value = p_id
    document.getElementById("score").value = element.getAttribute("score")

    // Disable other team's buttons since once a player has powered the other team
    // can no longer buzz on this tossup
    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "btn")

    // Disable this player's 15 and -5 buttons
    b_group = element.parentElement
    b_group.getElementsByClassName("power")[0].disabled = "true"
    b_group.getElementsByClassName("neg")[0].disabled = "true"
}

// Respond to user clicking neg button (red -5 button) 
function neg(element) {
    // Toggle Bootstrap button
    element.classList.add("active")
    element.setAttribute("aria-pressed", "true")

    // Set hidden form values to reflect this player is the negging player and scored -5 points
    p_id = element.parentElement.parentElement.id
    document.getElementById("negging-player").value = p_id
    document.getElementById("neg-score").value = element.getAttribute("score")

    // Disable other team's neg buttons since only one neg can occur per tossup
    team_div = element.parentElement.parentElement.parentElement.id
    disableOtherTeamButtons(team_div, "neg")

    // Disable this players 15 and 10 buttons
    b_group = element.parentElement
    b_group.getElementsByClassName("power")[0].disabled = "true"
    b_group.getElementsByClassName("ten")[0].disabled = "true"
}

// Given the id of the `<div>` containing a team's buttons, disable the buttons
// with the given class name for the other team
function disableOtherTeamButtons(team_div, c_name) {
    if (team_div === "left-buttons") {
        for (e of document.getElementById("right-buttons").getElementsByClassName(c_name)) {
            if (!e.classList.contains("active")) {
                e.disabled = "true"
            }
        }
    }
    else if (team_div === "right-buttons") {
        for (e of document.getElementById("left-buttons").getElementsByClassName(c_name)) {
            if (!e.classList.contains("active")) {
                e.disabled = "true"
            }
        }
    }
}

// Function used by bonus buttons so they act as psuedo-checkboxes, toggling the checkboxes
// of the hidden form
function toggleCheckbox(id) {
    checkbox = document.getElementById(id)

    if (checkbox.checked === true) {
        checkbox.checked = false
    }
    else checkbox.checked = true
}


if (Number(document.getElementById("tossup").innerText) >= 21 && document.getElementById("left-score").innerText != document.getElementById("right-score").innerText) {
    alert("20 tossups are complete! Continue?")
}

// From https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
// Prevents form submission on refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
